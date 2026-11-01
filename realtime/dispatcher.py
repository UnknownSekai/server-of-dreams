"""Binds decoded frames to hub handlers, and owns the server's realtime service.

One :class:`RealtimeService` per process: it holds the registry (rooms and
sessions), the per-hub handlers and the transport. ``sod_router`` is the FastAPI
side, so an ASGI app can start and stop the service with its own lifespan.

Authentication: the hub connection identifies its user ONLY through the
``authorization`` header, which carries the same session token the REST API
issues. An invalid token is refused with UNAUTHENTICATED rather than silently
treated as a guest, because a guest seat would corrupt the roster.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from realtime import framing as F
from realtime import methods as M
from realtime.hub import (
    UNHANDLED,
    CircleHubHandler,
    CommonHubHandler,
    HubError,
    MultiLiveHubHandler,
)
from realtime.state import HubRegistry, HubSession
from realtime.transport import RealtimeServer

logger = logging.getLogger("sod.realtime")

GRPC_UNAUTHENTICATED = 16
GRPC_UNIMPLEMENTED = 12
GRPC_INTERNAL = 13


class RealtimeService:
    """The realtime channel: rooms, handlers and the HTTP/2 server."""

    def __init__(
        self,
        *,
        host: str = "0.0.0.0",
        port: int = 8443,
        certfile: Optional[str] = None,
        keyfile: Optional[str] = None,
        decode_token=None,
    ):
        self.registry = HubRegistry()
        self.multi_live = MultiLiveHubHandler(self.registry)
        self.circle = CircleHubHandler(self.registry)
        self.common = CommonHubHandler(self.registry)
        self.handlers = {
            "IMultiLiveHub": self.multi_live,
            "ICircleHub": self.circle,
            "ICommonHub": self.common,
        }
        self.decode_token = decode_token
        self.server = RealtimeServer(
            dispatcher=self.dispatch,
            session_factory=self.make_session,
            host=host,
            port=port,
            certfile=certfile,
            keyfile=keyfile,
        )
        # Stats, useful for a /status endpoint and for tests.
        self.frames_in = 0
        self.frames_out = 0

    # -- lifecycle --------------------------------------------------------- #
    async def start(self) -> None:
        await self.server.start()

    async def stop(self) -> None:
        await self.server.stop()

    # -- session factory --------------------------------------------------- #
    def make_session(self, hub: str, path: str, send, token: str) -> HubSession:
        """Build a session for a freshly opened hub stream and authenticate it."""
        session = HubSession(hub, path, send)
        user_id = None
        if self.decode_token is not None and token:
            user_id = self.decode_token(token)
        if user_id is None:
            logger.warning("hub %s opened with no valid token; refusing", hub)
            session.closed = True
            session.on_close = None
            return session
        session.user_id = user_id
        session.hash_user_id = self.registry.hash_for(user_id)
        session.on_close = lambda: self.registry.unregister(session)
        self.registry.register(session)
        logger.info("hub %s session opened for user %s", hub, user_id)
        return session

    # -- dispatch ---------------------------------------------------------- #
    def dispatch(self, hub: str, method: str, session: HubSession, msg) -> bool:
        """Route one decoded request. Returns True when it was handled."""
        self.frames_in += 1
        if session.closed or session.user_id is None:
            if msg.message_id is not None:
                session.send_error(
                    msg.message_id,
                    GRPC_UNAUTHENTICATED,
                    "invalid or missing session token",
                )
            return True

        handler = self.handlers.get(hub)
        if handler is None:
            return False
        logger.info(
            "dispatch %s.%s (user=%s, member=%s, msg_id=%s)",
            hub,
            method,
            session.user_id,
            session.member_id,
            msg.message_id,
        )
        try:
            result = handler.handle(method, session, msg.args)
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("handler %s.%s failed", hub, method)
            if msg.message_id is not None:
                session.send_error(msg.message_id, GRPC_INTERNAL, repr(exc))
            return True

        if result is UNHANDLED:
            return False
        if msg.message_id is None:
            # Fire-and-forget: the client does not expect an answer.
            return True
        if isinstance(result, HubError):
            session.send_error(
                msg.message_id, result.status, result.detail, result.message
            )
            return True
        session.respond(msg.message_id, M.fnv1a32(method), result)
        self.frames_out += 1
        return True


# --------------------------------------------------------------------------- #
# ASGI integration
# --------------------------------------------------------------------------- #
class RealtimeRouter:
    """Starts and stops the realtime service with the ASGI app's lifespan.

    Kept separate from the FastAPI routes on purpose: the realtime channel is a
    different protocol on a different port, and mixing its lifecycle into the HTTP
    app would make either one harder to test.
    """

    def __init__(self, service: RealtimeService):
        self.service = service

    @property
    def router(self):
        from fastapi import APIRouter

        api = APIRouter()

        @api.get("/realtime/status", include_in_schema=False)
        async def _status() -> dict:
            return {
                "rooms": len(self.service.registry.rooms),
                "sessions": len(self.service.registry.sessions),
                "frames_in": self.service.frames_in,
                "frames_out": self.service.frames_out,
            }

        return api


def build_service(config, decode_token) -> RealtimeService:
    """Build the service from ``config.yml``.

    The realtime section is optional: with no cert configured the channel still
    starts, in cleartext, which is what a local test against a plain h2 client
    needs.
    """
    section = config.get("realtime") or {}
    if not isinstance(section, dict):
        # A typed settings object (helpers.config.RealtimeSettings).
        section = section.model_dump()
    return RealtimeService(
        host=str(section.get("host", "0.0.0.0")),
        port=int(section.get("port", 8443)),
        certfile=section.get("certfile") or None,
        keyfile=section.get("keyfile") or None,
        decode_token=decode_token,
    )


__all__ = ["RealtimeRouter", "RealtimeService", "build_service"]
