"""Realtime hub state: sessions, rooms, seats and the broadcast fan-out.

The distinction that matters here is **seat vs connection**. A captured session
reconnects to the hub WITHOUT joining again and keeps its place in the room, so a
member cannot be tied to the socket that occupies it. Hence:

* :class:`RoomMember` is a SEAT: identity plus the last known state, and it outlives
  the connection. While disconnected its state is kept as a snapshot so a reconnect
  restores the roster exactly as the other players saw it.
* :class:`HubSession` is one CONNECTION. It holds the live state the handlers mutate
  and is bound to at most one seat.

Rules that come from the capture rather than guesswork:

* the creator of a private hall becomes member id **1** and is the host;
* later joiners get 2, 3, ... and appear to everyone as an ``OnJoin`` broadcast;
* every state change is echoed to the whole room, INCLUDING the member who caused
  it -- the client's own UI renders from the broadcast, not from its own call.
"""

from __future__ import annotations

import itertools
import logging
import secrets
import time
from typing import Any, Callable, Optional

from helpers.user_hash import hash_id

from realtime import dtos as D
from realtime import framing as F
from realtime import methods as M

logger = logging.getLogger("sod.realtime")

MAX_MEMBERS = 4

# How long an empty room survives before it is discarded.
#
# Not zero: the capture shows a client reconnecting and finding its seat still there, so
# tearing a hall down the instant the last socket closes would destroy it on a network
# blip. Not forever either, or abandoned halls would accumulate and be offered by
# ``find_public_room`` long after everyone left.
ROOM_GRACE_SECONDS = 120.0


class RoomMember:
    """A seat in a hall: identity plus state, independent of any connection."""

    __slots__ = ("member_id", "user_id", "hash_user_id", "session", "snapshot")

    def __init__(self, member_id: int, user_id: Optional[int], hash_user_id: str):
        self.member_id = member_id
        self.user_id = user_id
        self.hash_user_id = hash_user_id
        self.session: Optional["HubSession"] = None
        # The last state seen while connected, as a MultiLiveUser array. Kept so a
        # disconnected member still shows up in the roster with the right name, song
        # and score rather than as a blank row.
        self.snapshot: Optional[list] = None

    @property
    def connected(self) -> bool:
        return self.session is not None

    def to_user(self) -> list:
        if self.session is not None:
            return self.session.to_user(self.member_id)
        if self.snapshot is not None:
            return list(self.snapshot)
        return D.multi_live_user(
            member_id=self.member_id, hash_user_id=self.hash_user_id
        )

    def capture(self) -> None:
        """Freeze the current state so it survives a disconnect."""
        if self.session is not None:
            self.snapshot = self.session.to_user(self.member_id)


class Room:
    """A multi-live hall.

    ``host_member_id`` is 1 because the hall's creator always takes the first seat,
    which is what the capture shows for both the public and private paths.
    """

    def __init__(
        self,
        hall_id: str,
        live_setting_master_id: int,
        hall_type: int,
        *,
        private: bool = True,
    ):
        self.hall_id = hall_id
        self.live_setting_master_id = live_setting_master_id
        self.hall_type = hall_type
        self.is_private = private
        self.host_member_id = 1
        # The code a friend types to join a private hall. Derived from the hall id so
        # it is stable for the hall's whole life -- the real server's code is
        # unrelated to the id, but only stability matters to the client.
        is_team_challenge = (hall_type == 21) or (live_setting_master_id == 21)
        self.key_code = (
            _key_code_for(hall_id, is_team_challenge=is_team_challenge)
            if private
            else 0
        )
        self.members: dict[int, RoomMember] = {}
        self.selected_music_id: int = 0
        self.multi_live_id: int = 0
        self.game_started: bool = False
        self._go_game_sent: bool = False
        self._lot_music_sent: bool = False
        self._exit_all_sent: bool = False
        # When the last connection left, or None while someone is still connected.
        self.empty_since: Optional[float] = None

    def _find_free_member_id(self) -> int:
        """Find the lowest available slot number (1..MAX_MEMBERS)."""
        for mid in range(1, MAX_MEMBERS + 1):
            if mid not in self.members:
                return mid
        return len(self.members) + 1

    # -- seats ------------------------------------------------------------- #
    def add_member(self, session: "HubSession") -> RoomMember:
        member = RoomMember(
            self._find_free_member_id(), session.user_id, session.hash_user_id
        )
        self.members[member.member_id] = member
        self.bind(member, session)
        return member

    def bind(self, member: RoomMember, session: "HubSession") -> None:
        """Put a connection into a seat, restoring the seat's last known state."""
        session.member_id = member.member_id
        session.hall_id = self.hall_id
        session.member = member
        member.session = session
        self.empty_since = None
        if member.snapshot is not None:
            session.restore_from(member.snapshot)

    def unbind(self, session: "HubSession") -> Optional[RoomMember]:
        """Take a connection out of its seat, keeping the seat's state."""
        member = self.members.get(session.member_id or -1)
        if member is None or member.session is not session:
            return None
        member.capture()
        member.session = None
        if not self.has_connections:
            self.empty_since = time.monotonic()
        return member

    def remove_member(
        self, member_id: int, session: Optional["HubSession"] = None
    ) -> Optional[RoomMember]:
        """Permanently remove a member from the room's seats."""
        member = self.members.get(member_id)
        if member is None:
            return None
        # If another active session already took over this seat, do not remove it
        if (
            session is not None
            and member.session is not None
            and member.session is not session
        ):
            return None
        self.members.pop(member_id, None)
        if member.session is not None and (
            session is None or member.session is session
        ):
            member.session.hall_id = None
            member.session.member_id = None
            member.session.member = None
            member.session = None
        member.snapshot = None
        if not self.has_connections:
            self.empty_since = time.monotonic()
        if self.host_member_id == member_id:
            remaining = list(self.members.keys())
            self.host_member_id = min(remaining) if remaining else 1
        return member

    def member_for_user(self, user_id: Optional[int]) -> Optional[RoomMember]:
        if user_id is None:
            return None
        for member in self.members.values():
            if member.user_id == user_id:
                return member
        return None

    # -- roster ------------------------------------------------------------ #
    @property
    def has_connections(self) -> bool:
        return any(m.connected for m in self.members.values())

    @property
    def can_open_hall(self) -> bool:
        """Whether the client may convert this private room to a public one.

        Team challenge halls are exempt: they are not part of the public matchmaking
        pool, so ``ChangeInteractableButtonInPrivateRoom`` never enables the button.
        """
        return self.hall_type != D.MultiLiveHallType.TeamChallenge

    def users(self) -> list[list]:
        return [m.to_user() for m in self.members.values()]

    def fetch_users_result(self) -> list:
        return D.multi_live_fetch_users_result(
            host_member_id=self.host_member_id,
            users=self.users(),
            can_open_hall=self.can_open_hall,
        )

    def active_sessions(self) -> list[tuple[int, "HubSession"]]:
        """``(member_id, session)`` for every connected member."""
        return [
            (m.member_id, m.session)
            for m in self.members.values()
            if m.session is not None
        ]


class HubSession:
    """One client's hub connection.

    ``send`` is injected by the transport so this class holds no socket, which keeps
    the state machine testable without a network.
    """

    def __init__(self, hub: str, path: str, send: Callable[[bytes], None]):
        self.hub = hub
        self.path = path
        self._send = send
        self.user_id: Optional[int] = None
        self.user_name: str = ""
        self.hash_user_id: str = ""
        self.leader_character: Optional[list] = None
        self.user_name_plate_color_id: int = 0
        # Seat
        self.hall_id: Optional[str] = None
        self.member_id: Optional[int] = None
        self.member: Optional[RoomMember] = None
        # Per-member in-game state (mirrors MultiLiveUser keys 2..13)
        self.is_random_music = False
        self.selected_music_id = 0
        self.status = D.MultiLiveUserStatus.Joined
        self.difficulty = 0
        self.clear_lamp = 0
        self.score = 0
        self.is_exit_game = False
        self.is_afk = False
        self.is_ready_decide_member = False
        self.closed = False

    # -- wire -------------------------------------------------------------- #
    def to_user(self, member_id: Optional[int] = None) -> list:
        """This connection as a ``MultiLiveUser`` array for the roster."""
        return D.multi_live_user(
            member_id=member_id if member_id is not None else (self.member_id or 0),
            user_name=self.user_name,
            is_random_music=self.is_random_music,
            selected_music_id=self.selected_music_id,
            status=self.status,
            leader_character=self.leader_character,
            user_name_plate_color_id=self.user_name_plate_color_id,
            difficulty=self.difficulty,
            clear_lamp=self.clear_lamp,
            score=self.score,
            hash_user_id=self.hash_user_id,
            is_exit_game=self.is_exit_game,
            is_afk=self.is_afk,
            is_ready_decide_member=self.is_ready_decide_member,
        )

    def restore_from(self, user: list) -> None:
        """Restore state from a ``MultiLiveUser`` array (a seat's snapshot).

        Used when a client reconnects into a seat it already holds, so the roster
        other players see does not change just because a socket was replaced.
        """
        if not isinstance(user, (list, tuple)) or len(user) < 14:
            return
        self.user_name = user[1] or self.user_name
        self.is_random_music = bool(user[2])
        self.selected_music_id = user[3] or 0
        self.status = user[4] or D.MultiLiveUserStatus.Joined
        self.leader_character = user[5] or self.leader_character
        self.user_name_plate_color_id = user[6] or 0
        self.difficulty = user[7] or 0
        self.clear_lamp = user[8] or 0
        self.score = user[9] or 0
        self.is_exit_game = bool(user[11])
        self.is_afk = bool(user[12])
        self.is_ready_decide_member = bool(user[13])

    def reset_for_new_game(self) -> None:
        """Clear per-game state, keeping identity and seat.

        Used by ``ContinuePlayAsync``: the captured reply reuses the same hall id and
        member id, so the member stays seated but the previous round's score, song and
        readiness must not leak into the next one.
        """
        self.is_random_music = False
        self.selected_music_id = 0
        self.status = D.MultiLiveUserStatus.Joined
        self.difficulty = 0
        self.clear_lamp = 0
        self.score = 0
        self.is_exit_game = False
        self.is_afk = False
        self.is_ready_decide_member = False

    def send_frame(self, payload: bytes) -> None:
        if self.closed:
            return
        self._send(payload)

    def respond(self, message_id: int, method_id: int, result) -> None:
        self.send_frame(F.write_response(message_id, method_id, result))

    def send_error(
        self, message_id: int, status: int, detail: str, message: str = ""
    ) -> None:
        self.send_frame(F.write_error(message_id, status, detail, message))

    def broadcast(self, method_name: str, args) -> None:
        """Send a receiver callback to this client."""
        mid = M.method_id(method_name, self.hub)
        if mid is None:
            logger.warning("no method id for broadcast %s on %s", method_name, self.hub)
            return
        self.send_frame(F.write_broadcast(mid, args))


class HubRegistry:
    """All live connections and rooms.

    Rooms are keyed by hall id. A public join creates a room on demand, which is what
    the real server does: there is no lobby list in this protocol, the client simply
    asks to join and either gets a seat or an error code.
    """

    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {}
        self.sessions: set[HubSession] = set()
        # userId -> hashUserId, so roster entries can be matched to accounts.
        self.hash_by_user: dict[int, str] = {}
        # userId -> pending multi-live invitations, newest last. Kept in the registry
        # because an invitation outlives the connection that created it: it is delivered
        # on the invitee's NEXT connection, which is exactly how the capture shows
        # invitations being collected on join.
        self.invitations: dict[int, list[list]] = {}

    # -- invitations ------------------------------------------------------- #
    def add_invitation(self, user_id: int, invitation: list) -> None:
        pending = self.invitations.setdefault(user_id, [])
        # One live invitation per hall: re-inviting the same hall should refresh, not
        # pile up duplicates the client would render as several identical rows.
        hall_id = invitation[9] if len(invitation) > 9 else None
        pending[:] = [i for i in pending if len(i) <= 9 or i[9] != hall_id]
        pending.append(invitation)

    def take_invitations(self, user_id: int) -> list[list]:
        """Return and clear a user's pending invitations."""
        return self.invitations.pop(user_id, [])

    def sessions_for_user(
        self, user_id: int, hub: Optional[str] = None
    ) -> list[HubSession]:
        """Every live connection belonging to an account, optionally for one hub."""
        return [
            s
            for s in self.sessions
            if s.user_id == user_id and (hub is None or s.hub == hub)
        ]

    # -- connections ------------------------------------------------------- #
    def register(self, session: HubSession) -> None:
        self.sessions.add(session)
        # A client that reconnects keeps the seat it already held. The capture shows
        # this: a new hub connection issues room-scoped calls without joining again.
        #
        # Only the multi-live hub owns seats. An ICircleHub or ICommonHub connection
        # for the same account must NOT take over the seat: doing so would leave the
        # room bound to a connection that has nothing to do with it, and closing that
        # unrelated connection would then tear the room down.
        if session.hub != "IMultiLiveHub":
            return
        for room in self.rooms.values():
            member = room.member_for_user(session.user_id)
            if member is None:
                continue
            room.bind(member, session)
            logger.info(
                "user %s reconnected into seat %s of room %s",
                session.user_id,
                member.member_id,
                room.hall_id,
            )
            return

    def unregister(self, session: HubSession) -> None:
        self.sessions.discard(session)
        session.closed = True
        room = self.room_of(session)
        if room is None:
            return
        member_id = session.member_id or -1
        # If the game is actively in progress, unbind the session so a quick reconnect
        # can restore the seat mid-game. If not in game (lobby, result screen, etc.),
        # the member has left the room and is removed permanently.
        if room.game_started:
            member = room.unbind(session)
        else:
            member = room.remove_member(member_id, session=session)
        if member is None:
            return
        self.broadcast_to_room(room, "OnLeaveAnyOne", member.member_id)
        self.reap_empty_rooms()

    def room_of(self, session: HubSession) -> Optional[Room]:
        if session.hall_id is None:
            return None
        return self.rooms.get(session.hall_id)

    def circle_sessions(self) -> list[HubSession]:
        """Every connected ``ICircleHub`` session, for chat fan-out."""
        return [s for s in self.sessions if s.hub == "ICircleHub"]

    # -- rooms ------------------------------------------------------------- #
    def create_room(
        self, live_setting_master_id: int, hall_type: int, *, private: bool = True
    ) -> Room:
        hall_id = secrets.token_hex(16)
        room = Room(hall_id, live_setting_master_id, hall_type, private=private)
        self.rooms[hall_id] = room
        return room

    def find_public_room(self, live_setting_master_id: int) -> Room:
        """Join an existing public room with space, else create one.

        Matching is on the live setting and a room that has already started its game
        is not offered, because joining mid-song would drop the newcomer into a chart
        already in progress.
        """
        for room in self.rooms.values():
            if (
                not room.is_private
                and room.live_setting_master_id == live_setting_master_id
                and not room.game_started
                and len(room.members) < MAX_MEMBERS
            ):
                return room
        return self.create_room(
            live_setting_master_id, D.MultiLiveHallType.Gingaza, private=False
        )

    def room_by_key_code(self, key_code: int) -> Optional[Room]:
        for room in self.rooms.values():
            if room.is_private and room.key_code == key_code:
                return room
        return None

    def room_by_user_id(self, user_id: int) -> Optional[Room]:
        """Find the room where user_id currently holds a seat."""
        for room in self.rooms.values():
            if any(m.user_id == user_id for m in room.members.values()):
                return room
        return None

    def room_by_multi_live_id(self, multi_live_id: int) -> Optional[Room]:
        """Find the room by its active multi_live_id."""
        if not multi_live_id:
            return None
        for room in self.rooms.values():
            if room.multi_live_id == multi_live_id:
                return room
        return None

    def reap_empty_rooms(self) -> None:
        """Discard rooms nobody has been connected to for the grace period.

        Called after a disconnect rather than on a timer: the registry has no
        background task, and a room only becomes reapable as a result of a disconnect,
        so checking then is sufficient and keeps this free of scheduling concerns.
        """
        now = time.monotonic()
        for hall_id, room in list(self.rooms.items()):
            if room.has_connections or room.empty_since is None:
                continue
            if now - room.empty_since >= ROOM_GRACE_SECONDS:
                self.rooms.pop(hall_id, None)
                logger.info("room %s closed (empty past the grace period)", hall_id)

    def broadcast_to_room(
        self, room: Room, method_name: str, args, *, exclude: Optional[int] = None
    ) -> None:
        """Fan a receiver callback out to every CONNECTED member of a room."""
        for member_id, session in room.active_sessions():
            if exclude is not None and member_id == exclude:
                continue
            session.broadcast(method_name, args)

    def hash_for(self, user_id: int) -> str:
        """The account's real ``hashUserId``, as the game computes it.

        sod already has the game's reversible obfuscation scheme in
        ``helpers/user_hash.hash_id`` -- and the capture proves the realtime channel sends
        exactly that form: every ``hashUserId`` in the capture round-trips back to a real
        userId through ``unhash_id``. Inventing a different format here would break the
        client's identity matching, which is why the real function is used rather than a
        locally derived string.
        """
        found = self.hash_by_user.get(user_id)
        if found:
            return found
        value = hash_id(user_id)
        self.hash_by_user[user_id] = value
        return value


def _key_code_for(hall_id: str, is_team_challenge: bool = False) -> int:
    """A stable key code derived from the hall id.

    The official client specifies:
    - MultiLivePrivateHallIdDigits = 6 (normal private rooms: 100_000 - 999_999)
    - TeamChallengeHallIdDigits = 8 (team challenge: 10_000_000 - 99_999_999)
    """
    raw = int(hall_id[:8], 16)
    if is_team_challenge:
        return 10_000_000 + (raw % 90_000_000)
    return 100_000 + (raw % 900_000)


__all__ = ["HubRegistry", "HubSession", "MAX_MEMBERS", "Room", "RoomMember"]
