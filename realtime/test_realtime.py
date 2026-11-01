"""End-to-end test for the realtime hub channel, over a real HTTP/2 connection.

Runs the service on an ephemeral port in cleartext and speaks to it exactly as the
game does: open ``/<Hub>/Connect``, send ``[0, 0]`` to connect, then drive a whole
two-player multi-live session and assert the replies and broadcasts.

Run: ``.venv/bin/python -m realtime.test_realtime``
"""

from __future__ import annotations

import asyncio
import base64
import json
import sys

import h2.config
import h2.connection
import h2.events
import msgpack

sys.path.insert(0, "/root/server-of-dreams")

from helpers.user_hash import hash_id, unhash_id  # noqa: E402
from realtime import dtos as D  # noqa: E402
from realtime import framing as F  # noqa: E402
from realtime import methods as M  # noqa: E402
from realtime.dispatcher import RealtimeService  # noqa: E402
from realtime.hub import _as_user_id  # noqa: E402

PASS = 0
FAIL = 0


def check(label: str, condition: bool, extra: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label} {extra}")


class HubClient:
    """A minimal MagicOnion StreamingHub client over one h2 connection."""

    def __init__(self, hub: str, token: str = "tok1"):
        self.hub = hub
        self.token = token
        self.conn = h2.connection.H2Connection(
            config=h2.config.H2Configuration(client_side=True, header_encoding="latin1")
        )
        self.conn.local_settings.initial_window_size = 4 * 1024 * 1024
        self.stream_id = 1
        self.message_id = 0
        self.reader = None
        self.writer = None
        self.received: list = []
        self.responses: dict[int, list] = {}
        self._buf = b""
        self._grpc_buf = b""

    async def connect(self, port: int) -> None:
        self.reader, self.writer = await asyncio.open_connection("127.0.0.1", port)
        self.conn.initiate_connection()
        await self._flush()
        self.conn.send_headers(
            self.stream_id,
            [
                (":method", "POST"),
                (":scheme", "http"),
                (":authority", "localhost"),
                (":path", f"/{self.hub}/Connect"),
                ("content-type", "application/grpc"),
                ("te", "trailers"),
                ("authorization", f"Bearer {self.token}"),
            ],
        )
        await self._flush()
        # The client's connect request is method id 0 with no arguments.
        await self.send_request(0, None, expect_response=False)
        # Drain the handshake so the server's marker and headers are consumed.
        await self.drain(timeout=1.0)

    async def _flush(self) -> None:
        data = self.conn.data_to_send()
        if data:
            self.writer.write(data)
            await self.writer.drain()

    async def send_request(
        self, method_id: int, args, *, expect_response: bool = True
    ) -> int:
        self.message_id += 1
        payload = msgpack.packb([self.message_id, method_id, args])
        self.conn.send_data(self.stream_id, F.wrap_grpc_frame(payload))
        await self._flush()
        return self.message_id

    async def drain(self, timeout: float = 0.6) -> None:
        """Read whatever arrives within ``timeout`` and decode it."""
        end = asyncio.get_event_loop().time() + timeout
        while True:
            remaining = end - asyncio.get_event_loop().time()
            if remaining <= 0:
                break
            try:
                data = await asyncio.wait_for(
                    self.reader.read(65536), timeout=remaining
                )
            except asyncio.TimeoutError:
                break
            if not data:
                break
            self._buf += data
            # h2 bookkeeping (settings ack, window updates) must still be fed, and
            # only the DATA payloads are gRPC frames -- the rest of the buffer is
            # HTTP/2 framing, so it must not reach the gRPC parser.
            for ev in self.conn.receive_data(data):
                if isinstance(ev, h2.events.DataReceived):
                    self.conn.acknowledge_received_data(
                        ev.flow_controlled_length, ev.stream_id
                    )
                    self._grpc_buf += bytes(ev.data)
            await self._flush()
            self._consume_buffer()

    def _consume_buffer(self) -> None:
        """Pull complete gRPC frames out of the DATA payloads.

        A read can split a frame across two reads, so the tail is kept for the next
        call rather than being dropped.
        """
        while True:
            if len(self._grpc_buf) < 5:
                return
            length = int.from_bytes(self._grpc_buf[1:5], "big")
            if len(self._grpc_buf) < 5 + length:
                return
            payload = self._grpc_buf[5 : 5 + length]
            self._grpc_buf = self._grpc_buf[5 + length :]
            self._on_payload(payload)

    def _on_payload(self, payload: bytes) -> None:
        obj = msgpack.unpackb(payload, raw=False, strict_map_key=False)
        self.received.append(obj)
        if isinstance(obj, list) and len(obj) == 3 and obj[0] != -1:
            self.responses[obj[0]] = obj[2]

    async def call(self, method: str, args, *, timeout: float = 1.2):
        mid = M.method_id(method, self.hub)
        msg_id = await self.send_request(mid, args)
        end = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < end:
            if msg_id in self.responses:
                return self.responses.pop(msg_id)
            await self.drain(timeout=0.15)
        return None

    def broadcasts(self, method: str) -> list:
        mid = M.method_id(method, self.hub)
        return [
            o[1]
            for o in self.received
            if isinstance(o, list) and len(o) == 2 and o[0] == mid
        ]

    def close(self) -> None:
        try:
            self.writer.close()
        except Exception:
            pass


async def settle(*clients, timeout: float = 0.4) -> None:
    """Drain pending traffic on each client.

    Broadcasts are pushed by the server, so a client that has not read since the
    action that caused them will not have seen them yet. Draining explicitly makes
    the assertions deterministic instead of racing the network.
    """
    for client in clients:
        await client.drain(timeout=timeout)


async def main() -> int:
    # Each client is a DIFFERENT account: seats are keyed by account, so sharing a
    # user id would make the second client reuse the first one's seat.
    service = RealtimeService(
        host="127.0.0.1",
        port=0,
        decode_token=lambda t: {"tok1": 10, "tok2": 11, "tok3": 12}.get(t),
    )
    await service.start()
    port = service.server._server.sockets[0].getsockname()[1]
    print(f"realtime test server on 127.0.0.1:{port}\n")

    host = HubClient("IMultiLiveHub", token="tok1")
    guest = HubClient("IMultiLiveHub", token="tok2")
    try:
        # --- connect ---------------------------------------------------- #
        print("connect")
        await host.connect(port)
        check(
            "server sent the anti-buffering marker",
            host.received and host.received[0] == [-1, 0, 12],
            f"got {host.received[:1]}",
        )
        check("host session registered", len(service.registry.sessions) == 1)

        # --- create a private hall -------------------------------------- #
        print("\ncreate private hall")
        res = await host.call(
            "CreatePrivateHallAsync",
            [
                13,
                13,
                "良太",
                110,
                [
                    150050,
                    5,
                    110,
                    105,
                    2007114,
                    110205,
                    210211026,
                    True,
                    None,
                    1439716,
                    180001,
                ],
            ],
        )
        check(
            "reply is a 5-element create result",
            isinstance(res, list) and len(res) == 5,
            f"got {res!r}",
        )
        check("is_succeeded", res and res[0] is True)
        check("member id 1 for the creator", res and res[2] == 1)
        check(
            "hall id is 32 hex chars",
            res and isinstance(res[1], str) and len(res[1]) == 32,
            f"got {res[1] if res else None!r}",
        )
        key_code = res[3] if res else 0
        hall_id = res[1] if res else ""
        # An int, not a fixed-width code: the capture shows both 6- and 8-digit codes.
        check(
            "key code is a number",
            isinstance(key_code, int) and 0 < key_code < 100_000_000,
        )

        # --- a guest joins by key code ---------------------------------- #
        print("\nguest joins with the key code")
        await guest.connect(port)
        gres = await guest.call(
            "JoinPrivateHallWithKeyCodeAsync",
            [
                key_code,
                "ゾメン",
                110,
                [150050, 5, 1, 2102, 202105, 0, 0, False, None, 0, 0],
            ],
        )
        check("join error code 0", gres and gres[0] == 0, f"got {gres!r}")
        check("guest is member 2", gres and gres[2] == 2)
        check("guest gets the same hall id", gres and gres[1] == hall_id)
        await settle(host)
        check(
            "host was told about the join (OnJoin)",
            len(host.broadcasts("OnJoin")) == 1,
            f"got {host.broadcasts('OnJoin')}",
        )
        joined = host.broadcasts("OnJoin")
        check(
            "OnJoin carries the guest's MultiLiveUser",
            joined and len(joined[0]) == 14,
            f"got {len(joined[0]) if joined else 0}",
        )
        check("OnJoin user name", joined and joined[0][1] == "ゾメン")
        check("OnJoin member id", joined and joined[0][0] == 2)

        # --- wrong key code is refused ---------------------------------- #
        print("\nwrong key code")
        stray = HubClient("IMultiLiveHub", token="tok3")
        await stray.connect(port)
        bad = await stray.call(
            "JoinPrivateHallWithKeyCodeAsync", [999999, "x", 110, None]
        )
        check("unknown hall -> NotFoundHall (3)", bad and bad[0] == 3, f"got {bad!r}")
        stray.close()

        # --- fetch users ------------------------------------------------ #
        print("\nfetch users")
        users = await host.call("FetchUsersAsync", None)
        check(
            "fetch result has 3 elements",
            isinstance(users, list) and len(users) == 3,
            f"got {users!r}",
        )
        check("host member id is 1", users and users[0] == 1)
        check("roster has 2 members", users and len(users[1]) == 2)
        check("can open hall is true", users and users[2] is True)

        # --- ready + decide --------------------------------------------- #
        print("\nready and decide")
        await guest.call("ReadyForDecideMember", True)
        await settle(host)
        check(
            "host saw OnReadyDecideMember",
            [2, True] in host.broadcasts("OnReadyDecideMember"),
            f"got {host.broadcasts('OnReadyDecideMember')}",
        )
        await host.call("DecideMemberAsync", None)
        check("OnGoGame broadcast", len(host.broadcasts("OnGoGame")) == 1)
        check("OnReadyGroup broadcast", len(host.broadcasts("OnReadyGroup")) == 1)

        # --- music and difficulty --------------------------------------- #
        print("\nmusic and difficulty")
        await host.call("SelectMusicAsync", [252, False, False])
        await settle(guest)
        check(
            "OnSelectMusic fan-out",
            [1, 252, False] in guest.broadcasts("OnSelectMusic"),
            f"got {guest.broadcasts('OnSelectMusic')}",
        )
        check(
            "Host alone selects music does not trigger OnLotMusic",
            len(host.broadcasts("OnLotMusic")) == 0,
        )

        await guest.call("SelectMusicAsync", [253, False, False])
        await settle(host, guest)
        check(
            "All members selected music triggers OnLotMusic",
            len(host.broadcasts("OnLotMusic")) == 1
            and len(guest.broadcasts("OnLotMusic")) == 1,
        )

        await host.call("SelectDifficultyAsync", [1, False])
        await settle(guest)
        check(
            "OnSelectDifficulty fan-out",
            [1, 1] in guest.broadcasts("OnSelectDifficulty"),
            f"got {guest.broadcasts('OnSelectDifficulty')}",
        )
        check(
            "Host alone selects difficulty does not broadcast OnGoGame yet",
            len(host.broadcasts("OnGoGame")) == 1,
        )  # only the 1 from decide_member

        await guest.call("SelectDifficultyAsync", [2, False])
        await settle(host, guest)
        check(
            "All members selected difficulty triggers OnGoGame to both",
            len(host.broadcasts("OnGoGame")) == 2
            and len(guest.broadcasts("OnGoGame")) == 2,
        )

        # --- game lifecycle --------------------------------------------- #
        print("\ngame lifecycle")
        await host.call("ReadyGameAsync", None)
        await guest.call("ReadyGameAsync", None)
        await host.call("BeforeGameCalculateAsync", None)
        await host.call("StartGameAsync", None)
        await settle(host, guest)
        check(
            "OnPlayGame broadcast to both",
            len(host.broadcasts("OnPlayGame")) == 1
            and len(guest.broadcasts("OnPlayGame")) == 1,
        )

        await host.call("SyncInGameStatusAsync", [123, 1, 2])
        await settle(guest)
        sync = guest.broadcasts("OnSyncInGameStatus")
        check(
            "OnSyncInGameStatus carries member/state",
            [1, 123, 1, 2] in sync,
            f"got {sync}",
        )

        await host.call("ExitGameAsync", [282546925, 1, {"1": 2, "2": 9}, 47])
        await settle(guest)
        check(
            "OnSyncGameResult fan-out",
            any(s[0] == 1 for s in guest.broadcasts("OnSyncGameResult")),
            f"got {guest.broadcasts('OnSyncGameResult')}",
        )
        check(
            "OnExitGameAnyOne fan-out", len(guest.broadcasts("OnExitGameAnyOne")) == 1
        )

        await host.call("EntryFinalResultAsync", None)
        await settle(guest)
        exit_broadcasts = guest.broadcasts("OnExitAllGames")
        check("OnExitAllGames carries the roster", len(exit_broadcasts) == 1)
        check(
            "OnExitAllGames carries [mvp_ids, fetch_result]",
            isinstance(exit_broadcasts[0], list)
            and len(exit_broadcasts[0]) == 2
            and isinstance(exit_broadcasts[0][0], list)
            and isinstance(exit_broadcasts[0][1], list),
        )

        # --- continue play ---------------------------------------------- #
        print("\ncontinue play")
        cont = await host.call("ContinuePlayAsync", None)
        check(
            "continue reuses the hall id", cont and cont[1] == hall_id, f"got {cont!r}"
        )
        check("continue keeps member id 1", cont and cont[2] == 1)
        check(
            "guest status not prematurely reset to Joined",
            service.registry.rooms[hall_id].members[2].session.status
            == D.MultiLiveUserStatus.ExitGame,
        )
        check(
            "guest is_ready_decide_member is False",
            not service.registry.rooms[hall_id]
            .members[2]
            .session.is_ready_decide_member,
        )

        # Host marks ready in lobby
        await host.call("ReadyForDecideMember", True)

        # Guest calls entry final result (e.g. from lingering result screen) and continue play
        await guest.call("EntryFinalResultAsync", None)
        check(
            "host status not overwritten back to ExitGame by guest's final result",
            service.registry.rooms[hall_id].members[1].session.status
            == D.MultiLiveUserStatus.Joined,
        )
        check(
            "host is_ready_decide_member preserved",
            service.registry.rooms[hall_id].members[1].session.is_ready_decide_member,
        )

        guest_cont = await guest.call("ContinuePlayAsync", None)
        check(
            "guest continue reuses the hall id", guest_cont and guest_cont[1] == hall_id
        )
        check(
            "guest status is now Joined",
            service.registry.rooms[hall_id].members[2].session.status
            == D.MultiLiveUserStatus.Joined,
        )
        check(
            "guest notified host is already ready (OnReadyDecideMember)",
            [1, True] in guest.broadcasts("OnReadyDecideMember"),
        )

        # --- leaving ----------------------------------------------------- #
        print("\nleaving")
        guest.close()
        await asyncio.sleep(0.4)
        await settle(host)
        check(
            "host told the guest left (OnLeaveAnyOne)",
            2 in host.broadcasts("OnLeaveAnyOne"),
            f"got {host.broadcasts('OnLeaveAnyOne')}",
        )
        check(
            "guest seat removed from room upon leaving",
            2 not in service.registry.rooms[hall_id].members,
        )

        # --- auth -------------------------------------------------------- #
        print("\nauthentication")
        bad_client = HubClient("IMultiLiveHub", token="nope")
        await bad_client.connect(port)
        r = await bad_client.call("FetchUsersAsync", None)
        check("bad token gets no usable reply", r is None, f"got {r!r}")
        bad_client.close()

        # --- circle hub -------------------------------------------------- #
        print("\ncircle hub")
        circle = HubClient("ICircleHub", token="tok1")
        await circle.connect(port)
        sent = await circle.call(
            "TrySendChatAsync", ["tes", None, "良太", 150050, True, None, 190003]
        )
        check("chat accepted (result [0])", sent == [0], f"got {sent!r}")
        chats = circle.broadcasts("OnReceiveChat")
        check(
            "OnReceiveChat has 11 elements",
            chats and len(chats[0]) == 11,
            f"got {len(chats[0]) if chats else 0}",
        )
        check("chat text relayed", chats and chats[0][2] == "tes")
        circle.close()

        # --- common hub -------------------------------------------------- #
        print("\ncommon hub")
        common = HubClient("ICommonHub", token="tok1")
        await common.connect(port)
        inv = await common.call("GetMultiLiveInvitationsFromFriendAsync", None)
        check("invitations reply is an empty list", inv == [], f"got {inv!r}")
        common.close()

        # --- friend invitation ------------------------------------------- #
        print("\nfriend invitation")
        # A third account joins the public hub so it can receive the invite push.
        friend = HubClient("ICommonHub", token="tok3")
        await friend.connect(port)
        invited = await host.call(
            "NotifyFriendsAsync",
            [["12"], 150050, True, 205, 110209, 110272, 210071023, 190003],
        )
        check("invite accepted", invited is None, f"got {invited!r}")
        await settle(friend)
        pushed = friend.broadcasts("OnNotifyInviteMultiLiveFromFriend")
        check("invitee got the push", len(pushed) == 1, f"got {len(pushed)}")
        check(
            "push is a 13-element MultiLiveInvitation",
            pushed and len(pushed[0]) == 13,
            f"got {len(pushed[0]) if pushed else 0}",
        )
        check(
            "invitation carries the hall id",
            pushed and pushed[0][9] == hall_id,
            f"got {pushed[0][9] if pushed else None!r}",
        )
        check(
            "invitation carries the inviter's name", pushed and pushed[0][1] == "良太"
        )
        check("invite id is a string", pushed and isinstance(pushed[0][0], str))
        # The invitee also sees it in the pull API on the next common-hub join.
        friend.close()
        await asyncio.sleep(0.3)
        friend2 = HubClient("ICommonHub", token="tok3")
        await friend2.connect(port)
        pending = await friend2.call("GetMultiLiveInvitationsFromFriendAsync", None)
        check(
            "invitation is returned by the pull API",
            isinstance(pending, list) and len(pending) == 1,
            f"got {pending!r}",
        )
        check("pulled invitation has 13 elements", pending and len(pending[0]) == 13)
        again = await friend2.call("GetMultiLiveInvitationsFromFriendAsync", None)
        check("invitations are consumed, not repeated", again == [], f"got {again!r}")
        friend2.close()

        # --- the roster carries the REAL hashUserId --------------------- #
        # Regression: the roster once carried a locally invented "0000000012" instead of
        # the game's own obfuscated id. The client matches accounts by that value, so a
        # made-up one breaks identity -- and, because invitations are addressed by it,
        # silently breaks friend invites too.
        print("\nhashUserId on the roster")
        roster = await host.call("FetchUsersAsync", None)
        members = roster[1] if isinstance(roster, list) and len(roster) > 1 else []
        check("roster has a member to inspect", bool(members), f"got {roster!r}")
        if members:
            got = members[0][10]
            check(
                "hashUserId is the game's hash of the member's user id",
                got == hash_id(10),
                f"got {got!r}, want {hash_id(10)!r}",
            )
            check(
                "hashUserId round-trips back to the user id",
                unhash_id(got) == 10,
                f"got {unhash_id(got)!r}",
            )
            check(
                "hashUserId is not a locally derived decimal id",
                got != f"{10:010d}",
                f"got {got!r}",
            )

        # An invite addressed by the real hash must resolve; a made-up one must not.
        check(
            "invite by real hashUserId resolves to the account",
            _as_user_id(hash_id(10)) == 10,
        )
        check(
            "invite by an invented decimal id is rejected",
            _as_user_id("0000000010") is None,
        )

        # --- seat survives a reconnect, and only multi-live owns it ------ #
        print("\nseat ownership and reconnects")
        # A reconnecting socket for the same account takes over the seat, and the OLD
        # socket closing afterwards must NOT tear the room down -- this is exactly what
        # the capture shows (a reconnect issuing room-scoped calls without joining).
        replacement = HubClient("IMultiLiveHub", token="tok1")
        await replacement.connect(port)
        await settle(host)
        check(
            "reconnect did not create a second room",
            len(service.registry.rooms) == 1,
            f"got {len(service.registry.rooms)}",
        )
        host.close()
        await asyncio.sleep(0.4)
        check(
            "room survives the old socket closing",
            len(service.registry.rooms) == 1,
            f"got {len(service.registry.rooms)}",
        )
        # A hub that does not own seats must not steal one.
        probe = HubClient("ICircleHub", token="tok1")
        await probe.connect(port)
        room = next(iter(service.registry.rooms.values()))
        check(
            "circle connection did not steal the seat",
            room.members[1].session is not None
            and room.members[1].session.hub == "IMultiLiveHub",
            f"seat bound to {getattr(room.members[1].session, 'hub', None)}",
        )
        probe.close()
        await asyncio.sleep(0.4)
        check(
            "closing the circle connection did not close the room",
            len(service.registry.rooms) == 1,
            f"got {len(service.registry.rooms)}",
        )
        host = replacement

        # --- the Connect frame is silent --------------------------------- #
        # Regression: the client's first frame on a hub stream is the reserved ``[0, 0]``
        # (Connect). Its id is 0, which is NOT a name hash, so it used to fall through to
        # "unknown method id" and get an ERROR frame back -- a shape the client has no
        # case for. The real server answers it with nothing at all, so any reply here is
        # wrong. Verified against the captured session: on /ICircleHub/Connect the client
        # sends [0, 0] after the marker and the real server stays silent.
        print("\nConnect frame")
        conn = HubClient("IMultiLiveHub", token="tok1")
        await conn.connect(port)
        # connect() already sent [0, 0]; re-send so the reply window is unambiguous.
        before = len(conn.received)
        await conn.send_request(0, None, expect_response=False)
        await conn.drain(timeout=0.5)
        after = [o for o in conn.received[before:] if o != [-1, 0, 12]]
        check(
            "Connect is answered with silence, not an error",
            after == [],
            f"got {after!r}",
        )
        # The stream must still be usable afterwards.
        hall = await conn.call(
            "CreatePrivateHallAsync",
            [
                13,
                13,
                "良太",
                110,
                [
                    150050,
                    5,
                    110,
                    105,
                    2007114,
                    110205,
                    210211026,
                    True,
                    None,
                    1439716,
                    180001,
                ],
            ],
        )
        check(
            "stream still works after Connect",
            isinstance(hall, list) and hall[0] is True,
            f"got {hall!r}",
        )
        # Leave no trace: the room this created would otherwise be counted by the
        # seat/reconnect checks below, which assert on the total number of rooms.
        await conn.call("ExitRoomAsync", None)
        conn.close()
        await asyncio.sleep(0.2)

        # --- unknown hub ------------------------------------------------- #
        print("\nunknown hub")
        unknown = HubClient("INopeHub", token="tok1")
        await unknown.connect(port)
        check(
            "unknown hub did not register a session",
            all(s.hub != "INopeHub" for s in service.registry.sessions),
        )
        unknown.close()

    finally:
        host.close()
        guest.close()
        await service.stop()

    print(f"\n{PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
