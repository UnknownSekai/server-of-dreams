"""Handlers for the realtime StreamingHubs.

Each handler takes ``(session, args)`` and returns the value to send back:

* ``None`` or a list  -- the response body (void methods answer with nil);
* :data:`UNHANDLED`   -- no such method here, the dispatcher replies UNIMPLEMENTED;
* :class:`HubError`   -- an error response carrying a gRPC status.

Every request gets a response -- the capture shows even void methods answered with
``[MessageId, MethodId, nil]`` -- and state changes are ALSO fanned out to the room
as receiver callbacks, including to the member who caused them, because that
broadcast is what the client's UI renders from.

The sequence implemented here is the one a captured live session produced::

    CreatePrivateHallAsync / JoinPublicHallAsync / JoinPrivateHallWithKeyCodeAsync
      -> MultiLiveJoinResult (+ OnJoin to the room)
    FetchUsersAsync -> MultiLiveFetchUsersResult (host id, roster, can-open)
    ReadyForDecideMember -> OnReadyDecideMember
    DecideMemberAsync (host only) -> OnReadyGroup + OnGoGame
    SelectMusicAsync -> OnSelectMusic;  SelectDifficultyAsync -> OnSelectDifficulty
    ReadyGameAsync / BeforeGameCalculateAsync / StartGameAsync -> OnPlayGame
    SyncInGameStatusAsync -> OnSyncInGameStatus (~3 s timer, fan-out)
    ExitGameAsync -> OnSyncGameResult + OnExitGameAnyOne
    EntryFinalResultAsync -> OnExitAllGames
    ContinuePlayAsync -> a fresh MultiLiveJoinResult for the same hall
"""

from __future__ import annotations

import logging
import random
import time
from typing import Any, Optional

import msgpack

from helpers.user_hash import unhash_id
from realtime import dtos as D
from realtime.state import MAX_MEMBERS, HubRegistry, HubSession, Room

logger = logging.getLogger("sod.realtime")

# gRPC status codes
GRPC_UNKNOWN = 2
GRPC_UNIMPLEMENTED = 12
GRPC_INTERNAL = 13


class _Unhandled:
    """Sentinel: this hub has no handler for the method."""

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "UNHANDLED"


UNHANDLED = _Unhandled()


class HubError:
    """A gRPC error response."""

    __slots__ = ("status", "detail", "message")

    def __init__(self, status: int, detail: str = "", message: str = ""):
        self.status = status
        self.detail = detail
        self.message = message


# --------------------------------------------------------------------------- #
# MultiLive
# --------------------------------------------------------------------------- #
class MultiLiveHubHandler:
    """Implements ``IMultiLiveHub`` against :class:`HubRegistry`."""

    def __init__(self, registry: HubRegistry):
        self.registry = registry

    # -- dispatch ---------------------------------------------------------- #
    def handle(self, method: str, session: HubSession, args) -> Any:
        fn = _MULTI_LIVE_ROUTES.get(method)
        if fn is None:
            return UNHANDLED
        return fn(self, session, args)

    def _detach(self, session: HubSession) -> None:
        """Leave whatever room the session is currently in.

        Needed because ``Connect`` carries no arguments, so a reconnecting client is
        rebound to the seat it already holds. When that same client then creates or
        joins a DIFFERENT hall -- which the capture shows, a player moving from one
        room to the next -- the old seat must be released first, or the client would
        end up in two rooms and the old room would never close.
        """
        room = self.registry.room_of(session)
        if room is None:
            return
        member = room.remove_member(session.member_id or -1, session=session)
        if member is not None:
            self.registry.broadcast_to_room(room, "OnLeaveAnyOne", member.member_id)
            logger.info(
                "member %s left room %s to move elsewhere",
                member.member_id,
                room.hall_id,
            )
        # The old room is left for the grace period rather than deleted, so a client
        # that comes back to it still finds its seat.
        self.registry.reap_empty_rooms()

    # -- join paths -------------------------------------------------------- #
    def create_private_hall(self, session: HubSession, args):
        p = D.read_create_private_hall(args)
        self._detach(session)
        hall_type = _scalar(p["multi_live_hall_type"], D.MultiLiveHallType.Gingaza)
        room = self.registry.create_room(
            p["live_setting_master_id"], hall_type, private=True
        )
        member = room.add_member(session)
        _apply_profile(session, p)
        logger.info(
            "room %s created by member %s (hallType=%s liveSetting=%s)",
            room.hall_id,
            member.member_id,
            hall_type,
            p["live_setting_master_id"],
        )
        return D.multi_live_create_private_hall_result(
            is_succeeded=True,
            hall_id=room.hall_id,
            member_id=member.member_id,
            private_hall_key_code=room.key_code,
            restriction_finished_at=None,
        )

    def join_public_hall(self, session: HubSession, args):
        p = D.read_join_public_hall(args)
        room = self.registry.find_public_room(p["live_setting_master_id"])
        return self._join(session, room, p, public=True)

    def join_private_hall_with_key_code(self, session: HubSession, args):
        p = D.read_join_with_key_code(args)
        room = self.registry.room_by_key_code(p["key_code"])
        if room is None:
            logger.info("key code %s did not match a room", p["key_code"])
            return D.multi_live_join_result(
                error_code=D.MultiLiveJoinErrorCodes.NotFoundHall
            )
        return self._join(session, room, p, key_code=room.key_code)

    def join_private_hall_from_invite(self, session: HubSession, args):
        p = D.read_join_from_invite(args)
        room = self.registry.rooms.get(p["hall_id"])
        if room is None:
            logger.info("invite for unknown hall %s", p["hall_id"])
            return D.multi_live_join_result(
                error_code=D.MultiLiveJoinErrorCodes.NotFoundHall
            )
        return self._join(session, room, p, key_code=room.key_code)

    def _join(
        self,
        session: HubSession,
        room: Room,
        p: dict,
        *,
        public: bool = False,
        key_code: int = 0,
    ):
        # Re-joining a room the same account already sits in reuses the seat rather
        # than taking a second one, which is what a reconnect looks like.
        existing = room.member_for_user(session.user_id)
        if existing is not None:
            room.bind(existing, session)
            _apply_profile(session, p)
            logger.info(
                "user %s re-joined room %s into seat %s",
                session.user_id,
                room.hall_id,
                existing.member_id,
            )
            return D.multi_live_join_result(
                error_code=D.MultiLiveJoinErrorCodes.None_,
                hall_id=None if public else room.hall_id,
                member_id=existing.member_id,
                key_code=0 if public else (key_code or room.key_code),
                live_setting_master_id=room.live_setting_master_id,
                restriction_finished_at=None,
            )
        # A different hall means leaving the previous one first.
        if self.registry.room_of(session) is not room:
            self._detach(session)
        if len(room.members) >= MAX_MEMBERS:
            return D.multi_live_join_result(
                error_code=D.MultiLiveJoinErrorCodes.ReachedMaxMember
            )
        member = room.add_member(session)
        _apply_profile(session, p)
        # Joining a room whose game already started means sitting out the round.
        session.is_afk = room.game_started

        # Everyone else learns about the new member. The joiner learns about the
        # others from its own FetchUsersAsync, which is why it is excluded here.
        self.registry.broadcast_to_room(
            room, "OnJoin", session.to_user(member.member_id), exclude=member.member_id
        )
        logger.info(
            "member %s joined room %s (private=%s, %d in room)",
            member.member_id,
            room.hall_id,
            not public,
            len(room.members),
        )

        # When the room reaches full capacity (4 members), automatically advance
        # to music selection for both public and private rooms.
        if len(room.members) >= MAX_MEMBERS:
            logger.info(
                "room %s reached full capacity (%d members) -> auto deciding roster",
                room.hall_id,
                MAX_MEMBERS,
            )
            self._do_decide_member(room)

        return D.multi_live_join_result(
            error_code=D.MultiLiveJoinErrorCodes.None_,
            # A captured public join replies with a NIL hall id: public rooms are
            # addressed server-side, only private ones expose an id.
            hall_id=None if public else room.hall_id,
            member_id=member.member_id,
            key_code=0 if public else (key_code or room.key_code),
            live_setting_master_id=room.live_setting_master_id,
            restriction_finished_at=None,
        )

    # -- lobby ------------------------------------------------------------- #
    def fetch_users(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return D.multi_live_fetch_users_result()
        return room.fetch_users_result()

    def open_private_room(self, session: HubSession, args):
        """Make a private hall publicly joinable.

        The hall itself SURVIVES: the capture shows the same hall id in the
        ``FetchUsersAsync`` replies that follow this call, so the room is not
        replaced or re-keyed. What changes is that it becomes discoverable by
        ``JoinPublicHallAsync``; the key code stays valid, so friends who already have
        it can still join directly.
        """
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        room.is_private = False
        logger.info(
            "room %s opened to the public (hallType=%s stays, keyCode stays)",
            room.hall_id,
            room.hall_type,
        )
        return None

    def notify_circle_member(self, session: HubSession, args):
        """Invite the circle; the server acknowledges and records the intent."""
        p = D.read_notify_circle_member(args)
        logger.info("circle invite from member %s: %s", session.member_id, p)
        return None

    def notify_friends(self, session: HubSession, args):
        """Invite friends to the current hall.

        The capture shows the real server pushing ``OnNotifyInviteMultiLiveFromFriend``
        to the INVITEE, and the invitation appearing in the invitee's
        ``GetMultiLiveInvitationsFromFriendAsync`` on its next connection. Both are
        done here; the friend ids are matched against accounts by user id.
        """
        p = D.read_notify_friends(args)
        room = self._room(session)
        if room is None:
            logger.info("friend invite with no room from member %s", session.member_id)
            return None
        now = time.time()
        for raw_id in p["friend_user_ids"]:
            friend_id = _as_user_id(raw_id)
            if friend_id is None:
                continue
            invitation = D.multi_live_invitation(
                invite_id=f"{int(now * 1000)}-0",
                user_name=session.user_name,
                character_master_id=_character_id_of(session.leader_character),
                display_awakening_status=_awakening_of(session.leader_character),
                player_rank=0,
                multi_live_type=room.hall_type,
                hall_id=room.hall_id,
                member_count=len(room.members),
                invited_at=msgpack.Timestamp(int(now), 0),
                icon_frame_master_id=0,
            )
            self.registry.add_invitation(friend_id, invitation)
            # Push it live if that friend happens to be connected.
            for friend_session in self.registry.sessions_for_user(friend_id):
                friend_session.broadcast(
                    "OnNotifyInviteMultiLiveFromFriend", invitation
                )
            logger.info(
                "member %s invited user %s to room %s",
                session.member_id,
                friend_id,
                room.hall_id,
            )
        return None

    # -- member selection -------------------------------------------------- #
    def _do_decide_member(self, room: Room) -> None:
        """Commit the roster and move everyone on to music selection."""
        for _member_id, connected in room.active_sessions():
            connected.is_ready_decide_member = True
            connected.status = D.MultiLiveUserStatus.Joined
            connected.selected_music_id = 0
            connected.is_random_music = False
            connected.difficulty = 0
            connected.score = 0
            connected.clear_lamp = 0
            connected.is_exit_game = False
        room.selected_music_id = 0
        room.multi_live_id = 0
        room.game_started = False
        room._go_game_sent = False
        room._lot_music_sent = False
        room._exit_all_sent = False
        self.registry.broadcast_to_room(room, "OnReadyGroup", False)
        self.registry.broadcast_to_room(room, "OnGoGame", None)
        logger.info("room %s: decided the roster -> OnGoGame", room.hall_id)

    def ready_for_decide_member(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        session.is_ready_decide_member = bool(_scalar(args, False))
        self.registry.broadcast_to_room(
            room,
            "OnReadyDecideMember",
            [session.member_id, session.is_ready_decide_member],
        )

        # In a public room, when multiple members are present and all active connected
        # members have pressed 準備完了 (is_ready_decide_member=True), automatically
        # advance to music selection. If only 1 player is in the room, do not advance.
        if not room.is_private and session.is_ready_decide_member:
            active = list(room.active_sessions())
            if len(active) >= 2 and all(s.is_ready_decide_member for _mid, s in active):
                logger.info(
                    "public room %s: all %d members are ready -> auto deciding roster",
                    room.hall_id,
                    len(active),
                )
                self._do_decide_member(room)

        return None

    def decide_member(self, session: HubSession, args):
        """The host commits the roster and moves everyone on to music selection.

        Only the host can do this -- the client hides the button for everyone else
        -- so a non-host call is logged and ignored rather than answered with an
        error the UI would not know how to show.
        """
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        if session.member_id != room.host_member_id:
            logger.info(
                "member %s called DecideMember but host is %s",
                session.member_id,
                room.host_member_id,
            )
            return None
        self._do_decide_member(room)
        return None

    # -- music / difficulty ------------------------------------------------ #
    def select_music(self, session: HubSession, args):
        p = D.read_select_music(args)
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        session.selected_music_id = p["music_id"]
        session.is_random_music = p["is_random"]
        session.is_afk = p["is_afk"]
        session.status = D.MultiLiveUserStatus.SelectedMusic
        # The drawn song becomes the room's song: everyone plays the same chart.
        if not p["is_random"] and p["music_id"]:
            room.selected_music_id = p["music_id"]
        self.registry.broadcast_to_room(
            room, "OnSelectMusic", [session.member_id, p["music_id"], p["is_random"]]
        )
        self._try_lot_music(room, p.get("music_id"))
        return None

    def _try_lot_music(
        self, room: Room, fallback_music_id: Optional[int] = None
    ) -> None:
        if getattr(room, "_lot_music_sent", False):
            return
        active = list(room.active_sessions())
        if not active:
            return
        all_selected = all(
            (s.selected_music_id > 0 or s.is_random_music) for _mid, s in active
        )
        if not all_selected:
            return

        room._lot_music_sent = True
        picked_candidates = [
            s.selected_music_id
            for _mid, s in active
            if s.selected_music_id and not s.is_random_music
        ]
        if not picked_candidates:
            picked_candidates = [
                s.selected_music_id for _mid, s in active if s.selected_music_id
            ]
        lot_music_id = (
            random.choice(picked_candidates)
            if picked_candidates
            else room.selected_music_id
        )
        if not lot_music_id:
            lot_music_id = fallback_music_id or 10071
        room.selected_music_id = lot_music_id

        if not room.multi_live_id:
            # Generate unique multi_live_id timestamp-based
            room.multi_live_id = int(time.time() * 1000) % 2_000_000_000

        logger.info(
            "room %s: all members selected music -> OnLotMusic(musicId=%s, multiLiveId=%s)",
            room.hall_id,
            room.selected_music_id,
            room.multi_live_id,
        )
        self.registry.broadcast_to_room(
            room, "OnLotMusic", [room.selected_music_id, room.multi_live_id]
        )

    def select_stamp(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        stamp_id = _scalar(args, 0)
        self.registry.broadcast_to_room(
            room, "OnSelectStamp", [session.member_id, stamp_id]
        )
        return None

    def select_difficulty(self, session: HubSession, args):
        p = D.read_select_difficulty(args)
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        session.difficulty = p["difficulty"]
        session.is_afk = p["is_afk"]
        session.status = D.MultiLiveUserStatus.SelectedDifficulty
        self.registry.broadcast_to_room(
            room, "OnSelectDifficulty", [session.member_id, p["difficulty"]]
        )
        self._try_lot_music(room)

        # When all active connected members have selected difficulty, broadcast OnGoGame
        active = list(room.active_sessions())
        all_diff = bool(active) and all(s.difficulty > 0 for _mid, s in active)
        if all_diff and not getattr(room, "_go_game_sent", False):
            room._go_game_sent = True
            logger.info(
                "room %s: all members selected difficulty -> OnGoGame", room.hall_id
            )
            self.registry.broadcast_to_room(room, "OnGoGame", None)

        return None

    # -- game lifecycle ---------------------------------------------------- #
    def ready_game(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        session.status = D.MultiLiveUserStatus.ReadyGame
        logger.info("room %s: member %s ready_game", room.hall_id, session.member_id)

        active = list(room.active_sessions())
        all_ready = bool(active) and all(
            s.status == D.MultiLiveUserStatus.ReadyGame for _mid, s in active
        )
        if all_ready and not room.game_started:
            room.game_started = True
            for _member_id, connected in active:
                connected.status = D.MultiLiveUserStatus.PlayingGame
            logger.info(
                "room %s: all members ready -> broadcasting OnPlayGame", room.hall_id
            )
            self.registry.broadcast_to_room(room, "OnPlayGame", None)

        return None

    def before_game_calculate(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        session.status = D.MultiLiveUserStatus.BeforeGameCalculate
        self.registry.broadcast_to_room(room, "OnBeforeGameCalculate", None)
        return None

    def start_game(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        if not room.game_started:
            room.game_started = True
            for _member_id, connected in room.active_sessions():
                connected.status = D.MultiLiveUserStatus.PlayingGame
            self.registry.broadcast_to_room(room, "OnPlayGame", None)
            logger.info("room %s: game started", room.hall_id)
        return None

    def sync_in_game_status(self, session: HubSession, args):
        """The ~3 s timer frame: relay the sender's combo and life to the room.

        The sender receives its own state echoed back as well, which is what makes
        the client's own combo counter authoritative rather than derived.
        """
        p = D.read_sync_in_game_status(args)
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        self.registry.broadcast_to_room(
            room,
            "OnSyncInGameStatus",
            [session.member_id, p["combo_count"], p["combo_type"], p["life"]],
        )
        return None

    def exit_game(self, session: HubSession, args):
        p = D.read_exit_game(args)
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        session.score = p["score"]
        session.clear_lamp = p["clear_lamp"]
        session.is_exit_game = True
        session.status = D.MultiLiveUserStatus.ExitGame
        session.is_ready_decide_member = False
        self.registry.broadcast_to_room(
            room,
            "OnSyncGameResult",
            [session.member_id, p["timing_counts"], p["max_combo"]],
        )
        self.registry.broadcast_to_room(
            room,
            "OnExitGameAnyOne",
            [
                len(room.members),
                sum(1 for _mid, s in room.active_sessions() if s.is_exit_game),
            ],
        )
        active_sessions = list(room.active_sessions())
        all_exited = bool(active_sessions) and all(
            s.is_exit_game for _mid, s in active_sessions
        )
        if all_exited and not getattr(room, "_exit_all_sent", False):
            self._broadcast_exit_all_games(room)
        return None

    def _broadcast_exit_all_games(self, room: Room) -> None:
        room._exit_all_sent = True
        room.game_started = False
        for _mid, s in room.active_sessions():
            if s.status != D.MultiLiveUserStatus.Joined:
                s.is_ready_decide_member = False
                s.status = D.MultiLiveUserStatus.ExitGame

        # Calculate MVP member ID(s) based on highest live score
        max_score = -1
        mvp_ids: list[int] = []
        for _mid, s in room.active_sessions():
            mid = s.member_id or 1
            if s.score > max_score:
                max_score = s.score
                mvp_ids = [mid]
            elif s.score == max_score and max_score > 0:
                mvp_ids.append(mid)
        if not mvp_ids:
            mvp_ids = [room.host_member_id]

        fetch_result = room.fetch_users_result()
        is_team_challenge = (room.hall_type == 21) or (
            room.live_setting_master_id == 21
        )
        event_name = (
            "OnExitAllGamesForTeamChallenge" if is_team_challenge else "OnExitAllGames"
        )
        # Client signature: OnExitAllGames(int[] mvpMemberIds, MultiLiveFetchUsersResult multiLiveFetchUsersResult)
        self.registry.broadcast_to_room(room, event_name, [mvp_ids, fetch_result])
        logger.info(
            "room %s: final results shown (mvp: %s, users: %d)",
            room.hall_id,
            mvp_ids,
            len(fetch_result[1]) if len(fetch_result) > 1 else 0,
        )

    def entry_final_result(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        if not getattr(room, "_exit_all_sent", False):
            self._broadcast_exit_all_games(room)
        return None

    def continue_play(self, session: HubSession, args):
        """Play again in the same hall.

        The captured reply reuses the original hall id and member id, so the room
        is kept and only its per-game state is reset.
        """
        room = self._room(session)
        if room is None:
            return D.multi_live_join_result(
                error_code=D.MultiLiveJoinErrorCodes.NotFoundHall
            )
        room.game_started = False
        room.selected_music_id = 0
        room.multi_live_id = 0
        room._go_game_sent = False
        room._lot_music_sent = False

        # When continuing play, the room becomes private even if it was previously public
        room.is_private = True
        if not room.key_code:
            from realtime.state import _key_code_for

            is_team_challenge = (room.hall_type == 21) or (
                room.live_setting_master_id == 21
            )
            room.key_code = _key_code_for(
                room.hall_id, is_team_challenge=is_team_challenge
            )

        session.reset_for_new_game()
        self.registry.broadcast_to_room(
            room,
            "OnJoin",
            session.to_user(session.member_id),
            exclude=session.member_id,
        )
        # Notify the continuing session of other members who are already ready in the lobby
        for mid, s in room.active_sessions():
            if mid != session.member_id and s.is_ready_decide_member:
                session.broadcast("OnReadyDecideMember", [mid, True])
        return D.multi_live_join_result(
            error_code=D.MultiLiveJoinErrorCodes.None_,
            hall_id=room.hall_id,
            member_id=session.member_id or 0,
            key_code=room.key_code,
            live_setting_master_id=room.live_setting_master_id,
            restriction_finished_at=None,
        )

    # -- team challenge ---------------------------------------------------- #
    def select_goal_difficulty_for_team_challenge(self, session: HubSession, args):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        difficulty = _scalar(args, 0)
        logger.info(
            "team challenge goal difficulty %s from member %s",
            difficulty,
            session.member_id,
        )
        return None

    def select_music_difficulty_and_party_for_team_challenge(
        self, session: HubSession, args
    ):
        room = self._room(session)
        if room is None:
            return HubError(GRPC_UNKNOWN, "not in a room")
        self.registry.broadcast_to_room(
            room,
            "OnSelectDifficultyAndPartyForTeamChallenge",
            [session.member_id, args],
        )
        return None

    # -- helper ------------------------------------------------------------ #
    def _room(self, session: HubSession) -> Optional[Room]:
        return self.registry.room_of(session)


_MULTI_LIVE_ROUTES = {
    "CreatePrivateHallAsync": MultiLiveHubHandler.create_private_hall,
    "JoinPublicHallAsync": MultiLiveHubHandler.join_public_hall,
    "JoinPrivateHallWithKeyCodeAsync": MultiLiveHubHandler.join_private_hall_with_key_code,
    "JoinPrivateHallFromInviteAsync": MultiLiveHubHandler.join_private_hall_from_invite,
    "FetchUsersAsync": MultiLiveHubHandler.fetch_users,
    "OpenPrivateRoomAsync": MultiLiveHubHandler.open_private_room,
    "NotifyCircleMemberAsync": MultiLiveHubHandler.notify_circle_member,
    "NotifyFriendsAsync": MultiLiveHubHandler.notify_friends,
    "ReadyForDecideMember": MultiLiveHubHandler.ready_for_decide_member,
    "DecideMemberAsync": MultiLiveHubHandler.decide_member,
    "SelectMusicAsync": MultiLiveHubHandler.select_music,
    "SelectStampAsync": MultiLiveHubHandler.select_stamp,
    "SelectDifficultyAsync": MultiLiveHubHandler.select_difficulty,
    "ReadyGameAsync": MultiLiveHubHandler.ready_game,
    "BeforeGameCalculateAsync": MultiLiveHubHandler.before_game_calculate,
    "StartGameAsync": MultiLiveHubHandler.start_game,
    "SyncInGameStatusAsync": MultiLiveHubHandler.sync_in_game_status,
    "ExitGameAsync": MultiLiveHubHandler.exit_game,
    "EntryFinalResultAsync": MultiLiveHubHandler.entry_final_result,
    "ContinuePlayAsync": MultiLiveHubHandler.continue_play,
    "SelectGoalDifficultyForTeamChallengeAsync": MultiLiveHubHandler.select_goal_difficulty_for_team_challenge,
    "SelectMusicDifficultyAndPartyForTeamChallengeAsync": MultiLiveHubHandler.select_music_difficulty_and_party_for_team_challenge,
}


# --------------------------------------------------------------------------- #
# Circle
# --------------------------------------------------------------------------- #
class CircleHubHandler:
    """Implements ``ICircleHub`` -- circle chat and activity logs.

    Chat history lives in memory. The real server persists it; persisting here
    would need a schema this repo has not defined for chat, and an in-process
    history is enough to make chat work between connected members.
    """

    def __init__(self, registry: HubRegistry):
        self.registry = registry
        # Wire-shaped entries, so GetChatsAsync can hand back exactly what
        # OnReceiveChat broadcast -- no second serialisation path to keep in sync.
        self.chats: list[list] = []
        self.activity_logs: list[list] = []
        self.read_watermark: int = 0

    def handle(self, method: str, session: HubSession, args) -> Any:
        fn = _CIRCLE_ROUTES.get(method)
        if fn is None:
            return UNHANDLED
        return fn(self, session, args)

    # -- ICircleHub.JoinAsync ---------------------------------------------- #
    def join(self, session: HubSession, args):
        """Join the circle's realtime channel.

        The client expects the read watermark right after joining, which is what
        lets it decide how much unread chat to highlight.
        """
        session.broadcast("OnJoin", None)
        session.broadcast(
            "OnReceiveReadChat", [self.read_watermark, self.read_watermark]
        )
        logger.info("circle session joined by user %s", session.user_id)
        return None

    def try_send_chat(self, session: HubSession, args):
        p = D.read_try_send_chat(args)
        chat_id = _next_chat_id()
        now = int(time.time())
        payload = D.circle_chat(
            chat_id=chat_id,
            hash_user_id=session.hash_user_id,
            text=p["text"],
            stamp_id=p["stamp_id"],
            timestamp=msgpack.Timestamp(now, 0),
            kind=0,
            user_name=p["user_name"],
            main_character_id=p["main_character_id"],
            flag8=bool(p["flag4"]),
            flag9=p["flag5"],
            icon_frame_master_id=p["icon_frame_master_id"],
        )
        self.chats.append(payload)
        # Broadcast FIRST so the sender receives its own message the same way it
        # receives everyone else's; the client renders from the broadcast.
        for member in self.registry.circle_sessions():
            member.broadcast("OnReceiveChat", payload)
        # 0 = success; the client checks it before clearing its input box.
        return [0]

    def get_chats(self, session: HubSession, args):
        """The recent history, newest-last, in the same shape as ``OnReceiveChat``."""
        return [list(chat) for chat in self.chats[-50:]]

    def get_read_chat(self, session: HubSession, args):
        return {"last_read_chat_id": self.read_watermark}

    def save_read_chat(self, session: HubSession, args):
        last = _scalar(args, 0)
        try:
            self.read_watermark = int(last)
        except (TypeError, ValueError):
            return None
        for member in self.registry.circle_sessions():
            member.broadcast(
                "OnReceiveReadChat", [self.read_watermark, self.read_watermark]
            )
        return None

    def delete_chat(self, session: HubSession, args):
        chat_id = _scalar(args, 0)
        self.chats = [c for c in self.chats if c[0] != chat_id]
        for member in self.registry.circle_sessions():
            member.broadcast("OnDeleteChat", chat_id)
        return None

    def get_activity_logs(self, session: HubSession, args):
        """The circle's activity log, newest first.

        Empty until the server records any activity: the capture's reply is an array of
        8-element entries, and an empty array is a valid page that keeps the client's
        log tab from hanging.
        """
        return [list(entry) for entry in self.activity_logs]


_CIRCLE_ROUTES = {
    "JoinAsync": CircleHubHandler.join,
    "TrySendChatAsync": CircleHubHandler.try_send_chat,
    "GetChatsAsync": CircleHubHandler.get_chats,
    "GetReadChatAsync": CircleHubHandler.get_read_chat,
    "SaveReadChatAsync": CircleHubHandler.save_read_chat,
    "DeleteChatAsync": CircleHubHandler.delete_chat,
    "GetActivityLogsAsync": CircleHubHandler.get_activity_logs,
}


# --------------------------------------------------------------------------- #
# Common
# --------------------------------------------------------------------------- #
class CommonHubHandler:
    """Implements ``ICommonHub`` -- friend invitations for multi-live."""

    def __init__(self, registry: HubRegistry):
        self.registry = registry

    def handle(self, method: str, session: HubSession, args) -> Any:
        fn = _COMMON_ROUTES.get(method)
        if fn is None:
            return UNHANDLED
        return fn(self, session, args)

    def join(self, session: HubSession, args):
        session.broadcast("OnJoin", None)
        return None

    def get_multi_live_invitations_from_friend(self, session: HubSession, args):
        """Pending invitations for this account.

        The captured reply is an array of 13-element ``MultiLiveInvitation`` entries, and
        it is collected fresh each time the client joins -- which is why the registry
        keeps them beyond the connection that created them. The list is consumed: an
        invitation is delivered once, so a stale hall is not offered forever.
        """
        if session.user_id is None:
            return []
        return self.registry.take_invitations(session.user_id)


_COMMON_ROUTES = {
    "JoinAsync": CommonHubHandler.join,
    "GetMultiLiveInvitationsFromFriendAsync": CommonHubHandler.get_multi_live_invitations_from_friend,
}


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #
def _apply_profile(session: HubSession, p: dict) -> None:
    """Copy the identity fields a join/create request carries onto the session."""
    name = p.get("user_name")
    if name:
        session.user_name = name
    plate = p.get("user_name_plate_color_id")
    if plate:
        session.user_name_plate_color_id = plate
    character = p.get("leader_character")
    if character is not None:
        session.leader_character = character


def _scalar(value, default=None):
    """Unwrap a single-argument payload.

    MagicOnion packs one argument as the bare value and several as an array, so a
    ``bool`` argument arrives as ``True`` rather than ``[True]``.
    """
    if isinstance(value, (list, tuple)):
        return value[0] if value else default
    if value is None:
        return default
    return value


def _as_user_id(raw) -> Optional[int]:
    """Resolve a friend identifier the client sent into a userId.

    The client identifies a friend by their ``hashUserId`` -- the obfuscated 10-digit form
    ``helpers/user_hash.hash_id`` produces, which the capture confirms is what travels in
    this channel. So the value is run through ``unhash_id``, the game's own inverse, rather
    than parsed as a plain int: a bare ``int()`` never matches an account, and it silently
    accepts garbage. A plain int is still honoured for callers that already hold a userId.
    """
    if isinstance(raw, int):
        return raw
    if not isinstance(raw, str):
        return None
    if raw.isdigit() and len(raw) != 10:  # already a userId, not a hash
        return int(raw)
    return unhash_id(raw)


def _character_id_of(leader_character) -> int:
    """``MultiLiveCharacter`` key 0 -- the character shown for the inviter."""
    if isinstance(leader_character, (list, tuple)) and leader_character:
        value = leader_character[0]
        if isinstance(value, int):
            return value
    return 0


def _awakening_of(leader_character) -> bool:
    """``MultiLiveCharacter`` key 7 -- whether the awakened art is displayed."""
    if isinstance(leader_character, (list, tuple)) and len(leader_character) > 7:
        return bool(leader_character[7])
    return False


_chat_counter = [0]


def _next_chat_id() -> int:
    _chat_counter[0] += 1
    return 1_700_000_000_000 + _chat_counter[0]


__all__ = [
    "CircleHubHandler",
    "CommonHubHandler",
    "HubError",
    "MultiLiveHubHandler",
    "UNHANDLED",
]
