"""Wire DTOs for the realtime hubs, in MessagePack-CSharp array form.

The game's serializer writes ``[MessagePackObject]`` types as **arrays indexed by
``[Key(n)]``**, not as maps: a gap becomes ``nil`` and the length is
``max(key) + 1``. ``MultiLiveUser`` therefore always goes out as 14 elements even
when the last few are nil.

Layouts come from the client's serialized realtime types and are cross-checked against a
live capture in ``realtime/tests``. Field ORDER matters: getting one wrong shifts every
following value and the client misreads silently.
"""

from __future__ import annotations

from typing import Any, Optional


# --------------------------------------------------------------------------- #
# Enums (values from the client)
# --------------------------------------------------------------------------- #
class MultiLiveHallType:
    None_ = 0
    Sirius = 11
    Eden = 12
    Gingaza = 13
    Denki = 14
    DenkiReprint = 15
    TeamChallenge = 21


class MultiLiveUserStatus:
    Joined = 0
    SelectedMusic = 1
    SelectedDifficulty = 2
    ReadyGame = 3
    BeforeGameCalculate = 4
    PlayingGame = 5
    ExitGame = 6
    Disconnected = 7


class MultiLiveJoinErrorCodes:
    None_ = 0
    ReachedMaxMember = 1
    RoomClosed = 2
    NotFoundHall = 3
    NotSubscribeMatchMakingServer = 4
    UserCanceled = 5
    Restricting = 6


class ClearLamps:
    """ClearLamps enum -- the capture shows 0/1, with 1 = cleared."""

    None_ = 0
    Clear = 1


# --------------------------------------------------------------------------- #
# DTO helpers
# --------------------------------------------------------------------------- #
def _arr(size: int) -> list:
    """An array of ``size`` nils, the shape MessagePack-CSharp writes."""
    return [None] * size


def _fill(arr: list, key: int, value: Any) -> list:
    if 0 <= key < len(arr):
        arr[key] = value
    return arr


# --------------------------------------------------------------------------- #
# MultiLiveCharacter -- 11 elements (Key 0..10)
# --------------------------------------------------------------------------- #
def multi_live_character(
    *,
    m_character_id: int = 0,
    talent_stage: int = 0,
    m_name_color_id: Optional[int] = None,
    m_name_plate_id: Optional[int] = None,
    m_trophy_id1: Optional[int] = None,
    m_trophy_id2: Optional[int] = None,
    m_trophy_id3: Optional[int] = None,
    display_awakening_status: bool = False,
    m_nameplate_detail_id: Optional[int] = None,
    total_status: int = 0,
    m_name_base_color_id: int = 0,
) -> list:
    """``MultiLiveCharacter``: the player's full on-screen appearance.

    Eleven elements, NOT twelve -- the capture sends exactly 11 and the type stops
    at ``Key(10)``. This is what the client sends when joining and what the server
    fans out in ``OnJoin``, which is why a guest's appearance is only visible to
    others if the server actually carries it.
    """
    a = _arr(11)
    _fill(a, 0, m_character_id)
    _fill(a, 1, talent_stage)
    _fill(a, 2, m_name_color_id)
    _fill(a, 3, m_name_plate_id)
    _fill(a, 4, m_trophy_id1)
    _fill(a, 5, m_trophy_id2)
    _fill(a, 6, m_trophy_id3)
    _fill(a, 7, display_awakening_status)
    _fill(a, 8, m_nameplate_detail_id)
    _fill(a, 9, total_status)
    _fill(a, 10, m_name_base_color_id)
    return a


# --------------------------------------------------------------------------- #
# MultiLiveUser -- 14 elements (Key 0..13)
# --------------------------------------------------------------------------- #
def multi_live_user(
    *,
    member_id: int,
    user_name: str = "",
    is_random_music: bool = False,
    selected_music_id: int = 0,
    status: int = MultiLiveUserStatus.Joined,
    leader_character: Optional[list] = None,
    user_name_plate_color_id: int = 0,
    difficulty: int = 0,
    clear_lamp: int = 0,
    score: int = 0,
    hash_user_id: str = "",
    is_exit_game: bool = False,
    is_afk: bool = False,
    is_ready_decide_member: bool = False,
) -> list:
    """``MultiLiveUser``: one room member as the client renders them."""
    a = _arr(14)
    _fill(a, 0, member_id)
    _fill(a, 1, user_name)
    _fill(a, 2, is_random_music)
    _fill(a, 3, selected_music_id)
    _fill(a, 4, status)
    _fill(
        a,
        5,
        leader_character if leader_character is not None else multi_live_character(),
    )
    _fill(a, 6, user_name_plate_color_id)
    _fill(a, 7, difficulty)
    _fill(a, 8, clear_lamp)
    _fill(a, 9, score)
    _fill(a, 10, hash_user_id)
    _fill(a, 11, is_exit_game)
    _fill(a, 12, is_afk)
    _fill(a, 13, is_ready_decide_member)
    return a


# --------------------------------------------------------------------------- #
# Results
# --------------------------------------------------------------------------- #
def multi_live_create_private_hall_result(
    *,
    is_succeeded: bool,
    hall_id: str = "",
    member_id: int = 0,
    private_hall_key_code: int = 0,
    restriction_finished_at=None,
) -> list:
    """``MultiLiveCreatePrivateHallResult`` -- 5 elements.

    The capture's reply is ``[true, "<32 hex>", 1, 113367, null]``: hall id, the
    caller's member id (1 = host), and the key code friends type to join.
    """
    a = _arr(5)
    _fill(a, 0, is_succeeded)
    _fill(a, 1, hall_id)
    _fill(a, 2, member_id)
    _fill(a, 3, private_hall_key_code)
    _fill(a, 4, restriction_finished_at)
    return a


def multi_live_join_result(
    *,
    error_code: int = MultiLiveJoinErrorCodes.None_,
    hall_id=None,
    member_id: int = 0,
    key_code: int = 0,
    live_setting_master_id: int = 0,
    restriction_finished_at=None,
) -> list:
    """``MultiLiveJoinResult`` -- 6 elements.

    Returned by every join path AND by ``ContinuePlayAsync``; the capture's
    continue-play reply reuses the original hall id and member id.

    ``hall_id`` is ``None`` for a public join: the capture shows a nil there, since
    public rooms are addressed server-side and only private halls expose an id.
    """
    a = _arr(6)
    _fill(a, 0, error_code)
    _fill(a, 1, hall_id)
    _fill(a, 2, member_id)
    _fill(a, 3, key_code)
    _fill(a, 4, live_setting_master_id)
    _fill(a, 5, restriction_finished_at)
    return a


def multi_live_fetch_users_result(
    *,
    host_member_id: int = 0,
    users: Optional[list] = None,
    can_open_hall: bool = False,
) -> list:
    """``MultiLiveFetchUsersResult`` -- 3 elements: host id, roster, can-open flag."""
    a = _arr(3)
    _fill(a, 0, host_member_id)
    _fill(a, 1, list(users or []))
    _fill(a, 2, can_open_hall)
    return a


# --------------------------------------------------------------------------- #
# Argument readers (client -> server)
# --------------------------------------------------------------------------- #
def read_join_public_hall(args) -> dict:
    """``JoinPublicHallAsync(liveSettingMasterId, userName, userNamePlateColorId, leaderCharacter)``."""
    args = _as_list(args)
    return {
        "live_setting_master_id": _at(args, 0, 0),
        "user_name": _at(args, 1, ""),
        "user_name_plate_color_id": _at(args, 2, 0),
        "leader_character": _at(args, 3, None),
    }


def read_create_private_hall(args) -> dict:
    """``CreatePrivateHallAsync(multiLiveHallType, liveSettingMasterId, userName, userNamePlateColorId, leaderCharacter)``."""
    args = _as_list(args)
    return {
        "multi_live_hall_type": _at(args, 0, 0),
        "live_setting_master_id": _at(args, 1, 0),
        "user_name": _at(args, 2, ""),
        "user_name_plate_color_id": _at(args, 3, 0),
        "leader_character": _at(args, 4, None),
    }


def read_join_with_key_code(args) -> dict:
    """``JoinPrivateHallWithKeyCodeAsync(keyCode, userName, userNamePlateColorId, leaderCharacter)``."""
    args = _as_list(args)
    return {
        "key_code": _at(args, 0, 0),
        "user_name": _at(args, 1, ""),
        "user_name_plate_color_id": _at(args, 2, 0),
        "leader_character": _at(args, 3, None),
    }


def read_join_from_invite(args) -> dict:
    """``JoinPrivateHallFromInviteAsync(hallId, userName, userNamePlateColorId, leaderCharacter)``.

    The capture shows the first argument is the hall id STRING, not a key code --
    the two join paths take different first arguments despite similar names.
    """
    args = _as_list(args)
    return {
        "hall_id": _at(args, 0, ""),
        "user_name": _at(args, 1, ""),
        "user_name_plate_color_id": _at(args, 2, 0),
        "leader_character": _at(args, 3, None),
    }


def read_select_music(args) -> dict:
    """``SelectMusicAsync(musicId, isRandom, isAFK)``."""
    args = _as_list(args)
    return {
        "music_id": _at(args, 0, 0),
        "is_random": _at(args, 1, False),
        "is_afk": _at(args, 2, False),
    }


def read_select_difficulty(args) -> dict:
    """``SelectDifficultyAsync(difficulty, isAFK)``."""
    args = _as_list(args)
    return {"difficulty": _at(args, 0, 0), "is_afk": _at(args, 1, False)}


def read_exit_game(args) -> dict:
    """``ExitGameAsync(score, clearLamp, timingCounts, maxCombo)``.

    ``timingCounts`` is an ``IReadOnlyDictionary<TimingTypes, int>`` and arrives as
    a msgpack MAP keyed by the enum's numeric value as a STRING -- e.g.
    ``{"1": 2, "2": 9, ...}``. It must stay a map on the way out.
    """
    args = _as_list(args)
    return {
        "score": _at(args, 0, 0),
        "clear_lamp": _at(args, 1, 0),
        "timing_counts": _at(args, 2, {}) or {},
        "max_combo": _at(args, 3, 0),
    }


def read_sync_in_game_status(args) -> dict:
    """``SyncInGameStatusAsync(comboCount, comboType, life)`` -- the ~3 s timer frame."""
    args = _as_list(args)
    return {
        "combo_count": _at(args, 0, 0),
        "combo_type": _at(args, 1, 0),
        "life": _at(args, 2, 0),
    }


def read_notify_friends(args) -> dict:
    """``NotifyFriendsAsync(friendUserIds, mainCharacterId, displayAwakeningStatus, playerRank, trophyMasterId1..3, iconFrameMasterId)``."""
    args = _as_list(args)
    return {
        "friend_user_ids": _at(args, 0, []) or [],
        "main_character_id": _at(args, 1, 0),
        "display_awakening_status": _at(args, 2, False),
        "player_rank": _at(args, 3, 0),
        "trophy_master_id1": _at(args, 4, None),
        "trophy_master_id2": _at(args, 5, None),
        "trophy_master_id3": _at(args, 6, None),
        "icon_frame_master_id": _at(args, 7, 0),
    }


def read_notify_circle_member(args) -> dict:
    """``NotifyCircleMemberAsync(mainCharacterId, displayAwakeningStatus, mIconFrameMasterId)``."""
    args = _as_list(args)
    return {
        "main_character_id": _at(args, 0, 0),
        "display_awakening_status": _at(args, 1, False),
        "m_icon_frame_master_id": _at(args, 2, 0),
    }


def read_try_send_chat(args) -> dict:
    """``TrySendChatAsync(payload)`` -> ``CircleChatPayload``.

    Capture: ``["tes", null, "良太", 150050, true, null, 190003]`` -- text, stamp id,
    user name, main character id, something, optional, icon frame id.
    """
    payload = _at(_as_list(args), 0, None)
    p = _as_list(payload)
    return {
        "text": _at(p, 0, None),
        "stamp_id": _at(p, 1, None),
        "user_name": _at(p, 2, ""),
        "main_character_id": _at(p, 3, 0),
        "flag4": _at(p, 4, False),
        "flag5": _at(p, 5, None),
        "icon_frame_master_id": _at(p, 6, 0),
    }


# --------------------------------------------------------------------------- #
# Circle chat / activity log wire DTOs
# --------------------------------------------------------------------------- #
def circle_chat(
    *,
    chat_id: int,
    hash_user_id: str,
    text=None,
    stamp_id=None,
    timestamp=None,
    kind: int = 0,
    user_name: str = "",
    main_character_id: int = 0,
    flag8: bool = False,
    flag9=None,
    icon_frame_master_id: int = 0,
) -> list:
    """``CircleChat`` as the server sends it in ``OnReceiveChat`` / ``GetChatsAsync``.

    Eleven elements, exactly as captured::

        [chatId, hashUserId, text, stampId, timestamp, kind, userName,
         mainCharacterId, flag8, flag9, iconFrameMasterId]

    ``timestamp`` must be a ``msgpack.Timestamp``: the capture shows real Unix
    seconds, not .NET ticks.
    """
    a = _arr(11)
    _fill(a, 0, chat_id)
    _fill(a, 1, hash_user_id)
    _fill(a, 2, text)
    _fill(a, 3, stamp_id)
    _fill(a, 4, timestamp)
    _fill(a, 5, kind)
    _fill(a, 6, user_name)
    _fill(a, 7, main_character_id)
    _fill(a, 8, flag8)
    _fill(a, 9, flag9)
    _fill(a, 10, icon_frame_master_id)
    return a


def circle_activity_log(
    *,
    hash_user_id: str,
    user_name: str,
    main_character_id: int,
    display_awakening_status: bool,
    log_type: int,
    value: str,
    log_id: int,
    timestamp=None,
) -> list:
    """``CircleActivityLog`` as ``GetActivityLogsAsync`` returns it.

    Eight elements, from the captured reply::

        [hashUserId, userName, mainCharacterId, displayAwakeningStatus, type,
         value, logId, timestamp]
    """
    a = _arr(8)
    _fill(a, 0, hash_user_id)
    _fill(a, 1, user_name)
    _fill(a, 2, main_character_id)
    _fill(a, 3, display_awakening_status)
    _fill(a, 4, log_type)
    _fill(a, 5, value)
    _fill(a, 6, log_id)
    _fill(a, 7, timestamp)
    return a


def multi_live_invitation(
    *,
    invite_id: str,
    user_name: str,
    character_master_id: int,
    display_awakening_status: bool = False,
    player_rank: int = 0,
    trophy_master_id1=None,
    trophy_master_id2=None,
    trophy_master_id3=None,
    multi_live_type: int = 1,
    hall_id: str = "",
    member_count: int = 1,
    invited_at=None,
    icon_frame_master_id: int = 0,
) -> list:
    """``MultiLiveInvitation`` -- 13 elements, as ``GetMultiLiveInvitationsFromFriendAsync``
    returns them and as ``OnNotifyInviteMultiLiveFromFriend`` pushes them.

    Captured example::

        ['1790220333755-0', '花', 150050, True, 205, 110209, 110272, 210071023,
         1, 'd2b9a97effad441abc40d644907f253d', 1,
         Timestamp(seconds=1790252733, nanoseconds=755000000), 190003]

    ``invite_id`` is a string, not a number -- ``"<unixMillis>-<index>"`` in the
    capture. It is what the client echoes back when accepting, so it must stay stable.
    """
    a = _arr(13)
    _fill(a, 0, invite_id)
    _fill(a, 1, user_name)
    _fill(a, 2, character_master_id)
    _fill(a, 3, display_awakening_status)
    _fill(a, 4, player_rank)
    _fill(a, 5, trophy_master_id1)
    _fill(a, 6, trophy_master_id2)
    _fill(a, 7, trophy_master_id3)
    _fill(a, 8, multi_live_type)
    _fill(a, 9, hall_id)
    _fill(a, 10, member_count)
    _fill(a, 11, invited_at)
    _fill(a, 12, icon_frame_master_id)
    return a


# --------------------------------------------------------------------------- #
# Internal
# --------------------------------------------------------------------------- #
def _as_list(v) -> list:
    if isinstance(v, (list, tuple)):
        return list(v)
    if v is None:
        return []
    return [v]


def _at(seq, index: int, default=None):
    try:
        return seq[index]
    except (IndexError, TypeError):
        return default


__all__ = [
    "ClearLamps",
    "MultiLiveHallType",
    "MultiLiveJoinErrorCodes",
    "MultiLiveUserStatus",
    "circle_activity_log",
    "circle_chat",
    "multi_live_character",
    "multi_live_invitation",
    "multi_live_create_private_hall_result",
    "multi_live_fetch_users_result",
    "multi_live_join_result",
    "multi_live_user",
    "read_create_private_hall",
    "read_exit_game",
    "read_join_from_invite",
    "read_join_public_hall",
    "read_join_with_key_code",
    "read_notify_circle_member",
    "read_notify_friends",
    "read_select_difficulty",
    "read_select_music",
    "read_sync_in_game_status",
    "read_try_send_chat",
]
