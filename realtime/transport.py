"""The realtime transport: an HTTP/2 server that speaks MagicOnion StreamingHub.

The game reaches this over TLS on a host the client trusts. A StreamingHub call is
one long-lived bidirectional stream, so the rules are different from a normal
HTTP/2 handler:

* the response must start as soon as HEADERS arrive, **before** any request body,
  because the client sends ``end_stream=false`` with an empty body and waits;
* a request body may never arrive at all -- ``Connect`` is a stream, not a
  request/response pair;
* the server writes a marker frame first (see ``framing.MARKER_PAYLOAD``) so a
  reverse proxy flushes the headers instead of buffering;
* the stream stays open until the client goes away, and messages flow both ways
  for as long as it lives.

Implemented on ``h2`` directly rather than through an ASGI server: uvicorn would
buffer the body and reproduce exactly the hang that made this channel
uncapturable through mitmproxy.
"""

from __future__ import annotations

import asyncio
import logging
import ssl
from typing import Any, Callable, Optional

import h2.config
import h2.connection
import h2.events
import h2.exceptions

from realtime import framing as F
from realtime import methods as M

logger = logging.getLogger("sod.realtime")

# 8 MB. A StartMultiLive-class reply is large, and the 64 KB default window stalls
# a long transfer part-way through.
WINDOW = 8 * 1024 * 1024


def _text(value) -> str:
    """Header values arrive as str with ``header_encoding="latin1"``; be tolerant."""
    if isinstance(value, bytes):
        return value.decode("latin1")
    return str(value)


class HubStream:
    """One ``/<Hub>/Connect`` stream."""

    def __init__(self, connection: "HubConnection", stream_id: int, path: str):
        self.connection = connection
        self.stream_id = stream_id
        self.path = path
        self.hub = M.hub_for_path(path)
        self.session: Any = None
        # The request headers, kept because ``authorization`` carries the account
        # token -- the only place a hub connection identifies its user.
        self.headers: dict[str, str] = {}
        self.closed = False
        self._lock = asyncio.Lock()

    def header(self, name: str, default: str = "") -> str:
        return self.headers.get(name.lower(), default)

    @property
    def token(self) -> str:
        """The bearer token from ``authorization``, or an empty string."""
        value = self.header("authorization")
        if value.lower().startswith("bearer "):
            return value[7:].strip()
        return value.strip()

    # -- outbound ---------------------------------------------------------- #
    def send_payload(self, payload: bytes) -> None:
        """Queue one MagicOnion frame onto the stream."""
        if self.closed:
            return
        self.connection.send_data(self.stream_id, F.wrap_grpc_frame(payload))

    async def send_payload_async(self, payload: bytes) -> None:
        async with self._lock:
            self.send_payload(payload)

    # -- inbound ----------------------------------------------------------- #
    def on_data(self, data: bytes) -> list[bytes]:
        """Feed request bytes; return the decoded payloads found."""
        out: list[bytes] = []
        for _compressed, payload in F.split_grpc_frames(data):
            out.append(payload)
        return out

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            self.connection.end_stream(self.stream_id)
        except Exception:
            pass


class HubConnection:
    """One client TCP/TLS connection, which may carry several hub streams."""

    def __init__(self, on_stream: Callable[[HubStream], None]):
        config = h2.config.H2Configuration(client_side=False, header_encoding="latin1")
        self.conn = h2.connection.H2Connection(config=config)
        self.conn.local_settings.initial_window_size = WINDOW
        self.conn.max_outbound_frame_size = 16384
        self.on_stream = on_stream
        self.streams: dict[int, HubStream] = {}
        self._write: Optional[Callable[[bytes], None]] = None

    def set_writer(self, write: Callable[[bytes], None]) -> None:
        self._write = write

    def _flush(self) -> None:
        data = self.conn.data_to_send()
        if data and self._write:
            self._write(data)

    def init(self) -> None:
        self.conn.initiate_connection()
        self._flush()

    def send_data(self, stream_id: int, data: bytes) -> None:
        try:
            self.conn.send_data(stream_id, data)
        except h2.exceptions.StreamClosedError:
            # The client hung up between our check and this write; not an error.
            return
        self._flush()

    def send_headers(self, stream_id: int, headers, end_stream: bool = False) -> None:
        try:
            self.conn.send_headers(stream_id, headers, end_stream=end_stream)
        except h2.exceptions.StreamClosedError:
            return
        self._flush()

    def end_stream(self, stream_id: int) -> None:
        try:
            self.conn.end_stream(stream_id)
        except Exception:
            return
        self._flush()

    def receive(self, data: bytes):
        """Feed bytes from the socket; returns h2 events."""
        events = self.conn.receive_data(data)
        # Acknowledge flow control so a long in-game sync stream keeps flowing.
        for ev in events:
            if isinstance(ev, h2.events.DataReceived):
                try:
                    self.conn.acknowledge_received_data(
                        ev.flow_controlled_length, ev.stream_id
                    )
                except Exception:
                    pass
        self._flush()
        return events


class RealtimeServer:
    """Accepts hub connections and dispatches frames to the handlers.

    ``dispatcher`` is a callable ``(hub, method_name, session, args) -> bool``: it
    returns True when it handled the method. Keeping it injectable lets the state
    machine be tested without a socket, and keeps this module free of game logic.
    """

    def __init__(
        self,
        dispatcher: Callable[..., bool],
        session_factory: Callable[[str, str, Callable[[bytes], None], str], object],
        host: str = "0.0.0.0",
        port: int = 8443,
        certfile: Optional[str] = None,
        keyfile: Optional[str] = None,
    ):
        self.dispatcher = dispatcher
        self.session_factory = session_factory
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self._server: Optional[asyncio.AbstractServer] = None

    async def start(self) -> None:
        ctx = None
        if self.certfile and self.keyfile:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(self.certfile, self.keyfile)
            ctx.set_alpn_protocols(["h2"])
        self._server = await asyncio.start_server(
            self._handle_client, self.host, self.port, ssl=ctx
        )
        scheme = "https" if ctx else "http"
        logger.info("realtime listening on %s://%s:%s", scheme, self.host, self.port)

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

    # -- connection handling ----------------------------------------------- #
    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        peer = writer.get_extra_info("peername")
        connection = HubConnection(on_stream=lambda s: self._on_stream(s))
        connection.set_writer(lambda data: self._safe_write(writer, data))
        try:
            connection.init()
            while True:
                data = await reader.read(65536)
                if not data:
                    break
                for ev in connection.receive(data):
                    await self._on_event(connection, ev)
        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass
        except Exception as exc:  # pragma: no cover - transport level
            logger.warning("realtime connection error from %s: %r", peer, exc)
        finally:
            for stream in list(connection.streams.values()):
                stream.close()
                if stream.session is not None:
                    self._close_session(stream.session)
            try:
                writer.close()
            except Exception:
                pass

    @staticmethod
    def _safe_write(writer: asyncio.StreamWriter, data: bytes) -> None:
        try:
            writer.write(data)
        except Exception:
            pass

    def _on_stream(self, stream: HubStream) -> None:
        """Called by the connection when a hub stream opens."""
        if stream.hub is None:
            return
        stream.session = self.session_factory(
            stream.hub,
            stream.path,
            lambda payload: stream.send_payload(payload),
            stream.token,
        )

    def _close_session(self, session) -> None:
        hook = getattr(session, "on_close", None)
        if callable(hook):
            hook()

    async def _on_event(self, connection: HubConnection, ev) -> None:
        if isinstance(ev, h2.events.RequestReceived):
            await self._on_request(connection, ev)
        elif isinstance(ev, h2.events.DataReceived):
            await self._on_request_data(connection, ev)
        elif isinstance(ev, h2.events.StreamReset):
            stream = connection.streams.pop(ev.stream_id, None)
            if stream is not None:
                stream.close()
                if stream.session is not None:
                    self._close_session(stream.session)
        elif isinstance(ev, h2.events.WindowUpdated):
            connection._flush()

    async def _on_request(self, connection: HubConnection, ev) -> None:
        # h2 is configured with header_encoding="latin1", so headers arrive as str
        # already; decode only if a bytes pair shows up.
        pairs = [(_text(k), _text(v)) for k, v in ev.headers]
        headers = {k.lower(): v for k, v in pairs}
        path = headers.get(":path", "/")
        method = headers.get(":method", "")
        stream = HubStream(connection, ev.stream_id, path)
        stream.headers = headers
        connection.streams[ev.stream_id] = stream

        if stream.hub is None:
            # Not a hub path: answer 404 rather than hanging.
            connection.send_headers(
                ev.stream_id,
                [
                    (":status", "404"),
                    ("content-type", "application/grpc"),
                    ("grpc-status", "12"),
                    ("grpc-message", "unknown hub"),
                ],
                end_stream=True,
            )
            return

        logger.info("hub stream %s opened (%s %s)", ev.stream_id, method, path)
        self._on_stream(stream)

        # Response headers FIRST, with the version header the client requires --
        # it throws if the header is present and not "2", and refuses to proceed
        # if it is absent.
        connection.send_headers(
            ev.stream_id,
            [
                (":status", "200"),
                ("content-type", "application/grpc"),
                ("x-magiconion-streaminghub-version", "2"),
                ("grpc-accept-encoding", "identity"),
            ],
        )
        # Then the anti-buffering marker. The client drops it; a proxy needs it.
        stream.send_payload(F.MARKER_PAYLOAD)

        if ev.stream_ended:
            stream.close()

    async def _on_request_data(self, connection: HubConnection, ev) -> None:
        stream = connection.streams.get(ev.stream_id)
        if stream is None or stream.session is None:
            return
        for payload in stream.on_data(bytes(ev.data)):
            await self._dispatch(stream, payload)

    async def _dispatch(self, stream: HubStream, payload: bytes) -> None:
        try:
            msg = F.read_message(payload, "c2s")
        except Exception as exc:
            logger.warning("undecodable hub frame on %s: %r", stream.path, exc)
            return
        if msg.kind == "heartbeat":
            # Echo the client's timestamp back so its heartbeat timer resets.
            stream.send_payload(
                F.write_client_heartbeat_response(F.parse_client_heartbeat_time(msg))
            )
            return
        if msg.method_id is None:
            return
        # The reserved Connect frame. The real server does NOT answer it -- verified in
        # the captured session, where the client's ``[0, 0]`` on /ICircleHub/Connect gets
        # no reply at all. Answering with an error (which an unregistered id used to do)
        # sends a frame shape the client has no case for.
        if msg.method_id == M.CONNECT_METHOD_ID:
            logger.info("hub stream connected (%s)", stream.path)
            return
        name = M.method_name(msg.method_id, stream.hub)
        if name is None:
            if msg.message_id is not None and stream.session is not None:
                stream.session.send_error(
                    msg.message_id, 12, f"unknown method id {msg.method_id}"
                )
            return
        if stream.session is None:
            return
        handled = self.dispatcher(stream.hub or "", name, stream.session, msg)
        if not handled and msg.message_id is not None:
            stream.session.send_error(msg.message_id, 12, f"unhandled method {name}")


__all__ = ["HubConnection", "HubStream", "RealtimeServer"]
