from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Events"])


# /api/Events/TrialPartyEvent/EditParty
@router.post(
    "/api/Events/TrialPartyEvent/EditParty", name="Events_EditTrialPartyEventParty"
)
async def events_edit_trial_party_event_party(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, EditTrialPartyEventStagePartyPayload)
    return respond(BooleanResult())


# /api/Events/CharacterPoint/GetCharacterBorderRanking/{characterPointEventMasterId}
@router.get(
    "/api/Events/CharacterPoint/GetCharacterBorderRanking/{characterPointEventMasterId}",
    name="Events_GetCharacterPointCharacterBorderRanking",
)
async def events_get_character_point_character_border_ranking(
    request: Request, characterPointEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CharacterPointEventRankingResult())


# /api/Events/CharacterPoint/GetCharacterNearRanking/{characterPointEventMasterId}
@router.get(
    "/api/Events/CharacterPoint/GetCharacterNearRanking/{characterPointEventMasterId}",
    name="Events_GetCharacterPointCharacterNearRanking",
)
async def events_get_character_point_character_near_ranking(
    request: Request, characterPointEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CharacterPointEventRankingResult())


# /api/Events/CharacterPoint/GetCharacterTopRanking/{characterPointEventMasterId}
@router.get(
    "/api/Events/CharacterPoint/GetCharacterTopRanking/{characterPointEventMasterId}",
    name="Events_GetCharacterPointCharacterTopRanking",
)
async def events_get_character_point_character_top_ranking(
    request: Request, characterPointEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CharacterPointEventRankingResult())


# /api/Events/CharacterPoint/GetInformation/{characterPointEventMasterId}
@router.get(
    "/api/Events/CharacterPoint/GetInformation/{characterPointEventMasterId}",
    name="Events_GetCharacterPointEventInformation",
)
async def events_get_character_point_event_information(
    request: Request, characterPointEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CharacterPointEventInformationResult())


# /api/Events/CharacterPoint/GetOverallTopRanking/{characterPointEventMasterId}
@router.get(
    "/api/Events/CharacterPoint/GetOverallTopRanking/{characterPointEventMasterId}",
    name="Events_GetCharacterPointOverallTopRanking",
)
async def events_get_character_point_overall_top_ranking(
    request: Request, characterPointEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CharacterPointEventRankingResult())


# /api/Events/CircleEvent/Raking/Border/{circleEventMasterId}
@router.get(
    "/api/Events/CircleEvent/Raking/Border/{circleEventMasterId}",
    name="Events_GetCircleEventBorderRanking",
)
async def events_get_circle_event_border_ranking(
    request: Request, circleEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleEventRanking())


# /api/Events/CircleEvent/Raking/Circle/{circleEventMasterId}
@router.get(
    "/api/Events/CircleEvent/Raking/Circle/{circleEventMasterId}",
    name="Events_GetCircleEventCircleRanking",
)
async def events_get_circle_event_circle_ranking(
    request: Request, circleEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleEventRanking())


# /api/Events/CircleEvent/Information/{circleEventMasterId}
@router.get(
    "/api/Events/CircleEvent/Information/{circleEventMasterId}",
    name="Events_GetCircleEventInformation",
)
async def events_get_circle_event_information(
    request: Request, circleEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleEventInformationResult())


# /api/Events/CircleEvent/Raking/Near/{circleEventMasterId}
@router.get(
    "/api/Events/CircleEvent/Raking/Near/{circleEventMasterId}",
    name="Events_GetCircleEventNearRanking",
)
async def events_get_circle_event_near_ranking(
    request: Request, circleEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleEventRanking())


# /api/Events/GetConcoursInformation?concoursMasterId=
@router.get("/api/Events/GetConcoursInformation", name="Events_GetConcoursInformation")
async def events_get_concours_information(
    request: Request, concoursMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(ConcoursInfomationResult())


# /api/Events/GetEventBorderRanking?mEventId=
@router.post("/api/Events/GetEventBorderRanking", name="Events_GetEventBorderRanking")
async def events_get_event_border_ranking(
    request: Request, mEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetEventCampBorderRanking?eventMasterId=
@router.post(
    "/api/Events/GetEventCampBorderRanking", name="Events_GetEventCampBorderRanking"
)
async def events_get_event_camp_border_ranking(
    request: Request, eventMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetEventCampMyRanking?eventMasterId=
@router.get("/api/Events/GetEventCampMyRanking", name="Events_GetEventCampMyRanking")
async def events_get_event_camp_my_ranking(
    request: Request, eventMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(StoryEventCampInfo())


# /api/Events/GetEventCampTopRanking?eventMasterId=
@router.post("/api/Events/GetEventCampTopRanking", name="Events_GetEventCampTopRanking")
async def events_get_event_camp_top_ranking(
    request: Request, eventMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetEventCircleRanking?mEventId=
@router.post("/api/Events/GetEventCircleRanking", name="Events_GetEventCircleRanking")
async def events_get_event_circle_ranking(
    request: Request, mEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetEventFriendRanking?mEventId=
@router.post("/api/Events/GetEventFriendRanking", name="Events_GetEventFriendRanking")
async def events_get_event_friend_ranking(
    request: Request, mEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetEventMyRanking?mEventId=
@router.post("/api/Events/GetEventMyRanking", name="Events_GetEventMyRanking")
async def events_get_event_my_ranking(request: Request, mEventId: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRanking())


# /api/Events/GetEventNearRanking?mEventId=
@router.post("/api/Events/GetEventNearRanking", name="Events_GetEventNearRanking")
async def events_get_event_near_ranking(
    request: Request, mEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetEventTopRanking?mEventId=
@router.post("/api/Events/GetEventTopRanking", name="Events_GetEventTopRanking")
async def events_get_event_top_ranking(
    request: Request, mEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetStoryEventBorderRanking/{mStoryEventId}
@router.post(
    "/api/Events/GetStoryEventBorderRanking/{mStoryEventId}",
    name="Events_GetStoryEventBorderRanking",
)
async def events_get_story_event_border_ranking(request: Request, mStoryEventId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetStoryEventCampNearRanking?eventMasterId=
@router.post(
    "/api/Events/GetStoryEventCampNearRanking",
    name="Events_GetStoryEventCampNearRanking",
)
async def events_get_story_event_camp_near_ranking(
    request: Request, eventMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetStoryEventCircleMissionProgresses/{mStoryEventId}
@router.post(
    "/api/Events/GetStoryEventCircleMissionProgresses/{mStoryEventId}",
    name="Events_GetStoryEventCircleMissionProgresses",
)
async def events_get_story_event_circle_mission_progresses(
    request: Request, mStoryEventId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(StoryEventMissionCircleProgressResult())


# /api/Events/GetStoryEventCircleRanking?mStoryEventId=
@router.post(
    "/api/Events/GetStoryEventCircleRanking", name="Events_GetStoryEventCircleRanking"
)
async def events_get_story_event_circle_ranking(
    request: Request, mStoryEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetStoryEventFriendRanking?mStoryEventId=
@router.post(
    "/api/Events/GetStoryEventFriendRanking", name="Events_GetStoryEventFriendRanking"
)
async def events_get_story_event_friend_ranking(
    request: Request, mStoryEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetStoryEventHighScoreTopRanking/{mStoryEventId}
@router.post(
    "/api/Events/GetStoryEventHighScoreTopRanking/{mStoryEventId}",
    name="Events_GetStoryEventHighScoreTopRanking",
)
async def events_get_story_event_high_score_top_ranking(
    request: Request, mStoryEventId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawHighScoreRankingResult())


# /api/Events/GetStoryEventMyRanking/{mStoryEventId}
@router.post(
    "/api/Events/GetStoryEventMyRanking/{mStoryEventId}",
    name="Events_GetStoryEventMyRanking",
)
async def events_get_story_event_my_ranking(request: Request, mStoryEventId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRanking())


# /api/Events/GetStoryEventNearRanking/{mStoryEventId}
@router.post(
    "/api/Events/GetStoryEventNearRanking/{mStoryEventId}",
    name="Events_GetStoryEventNearRanking",
)
async def events_get_story_event_near_ranking(request: Request, mStoryEventId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetStoryEventTopRanking/{mStoryEventId}
@router.post(
    "/api/Events/GetStoryEventTopRanking/{mStoryEventId}",
    name="Events_GetStoryEventTopRanking",
)
async def events_get_story_event_top_ranking(request: Request, mStoryEventId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Events/GetTotalPointEventCircleRanking?mTotalPointEventId=
@router.post(
    "/api/Events/GetTotalPointEventCircleRanking",
    name="Events_GetTotalPointEventCircleRanking",
)
async def events_get_total_point_event_circle_ranking(
    request: Request, mTotalPointEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TotalPointEventRankingResult())


# /api/Events/GetTotalPointEventFriendRanking?mTotalPointEventId=
@router.post(
    "/api/Events/GetTotalPointEventFriendRanking",
    name="Events_GetTotalPointEventFriendRanking",
)
async def events_get_total_point_event_friend_ranking(
    request: Request, mTotalPointEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TotalPointEventRankingResult())


# /api/Events/GetTotalPointEventInformation?mTotalPointEventId=
@router.post(
    "/api/Events/GetTotalPointEventInformation",
    name="Events_GetTotalPointEventInformation",
)
async def events_get_total_point_event_information(
    request: Request, mTotalPointEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TotalPointEventInformationResult())


# /api/Events/GetTotalPointEventNearRanking?mTotalPointEventId=
@router.post(
    "/api/Events/GetTotalPointEventNearRanking",
    name="Events_GetTotalPointEventNearRanking",
)
async def events_get_total_point_event_near_ranking(
    request: Request, mTotalPointEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TotalPointEventRankingResult())


# /api/Events/GetTotalPointEventTopRanking?mTotalPointEventId=
@router.post(
    "/api/Events/GetTotalPointEventTopRanking",
    name="Events_GetTotalPointEventTopRanking",
)
async def events_get_total_point_event_top_ranking(
    request: Request, mTotalPointEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TotalPointEventRankingResult())


# /api/Events/TournamentQualifying/Information/{tournamentQualifyingMasterId}
@router.post(
    "/api/Events/TournamentQualifying/Information/{tournamentQualifyingMasterId}",
    name="Events_GetTournamentQualifyingInformation",
)
async def events_get_tournament_qualifying_information(
    request: Request, tournamentQualifyingMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TournamentQualifyingInformationResult())


# /api/Events/GrowStoryEventHighScoreBuffSetting/{mStoryEventId}/{mStoryEventHighScoreBuffSettingId}/{levelTo}
@router.post(
    "/api/Events/GrowStoryEventHighScoreBuffSetting/{mStoryEventId}/{mStoryEventHighScoreBuffSettingId}/{levelTo}",
    name="Events_GrowStoryEventHighScoreBuffSetting",
)
async def events_grow_story_event_high_score_buff_setting(
    request: Request,
    mStoryEventId: int,
    mStoryEventHighScoreBuffSettingId: int,
    levelTo: int,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/NoneStoryEvents/ReadTips/{mEventId}
@router.post(
    "/api/NoneStoryEvents/ReadTips/{mEventId}", name="Events_NoneStoryEventsReadTips"
)
async def events_none_story_events_read_tips(request: Request, mEventId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Events/CharacterPoint/ReadTips/{characterPointEventMasterId}
@router.post(
    "/api/Events/CharacterPoint/ReadTips/{characterPointEventMasterId}",
    name="Events_ReadCharacterPointEventTips",
)
async def events_read_character_point_event_tips(
    request: Request, characterPointEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Events/ReadSpecialEventTips?mSpecialEventId=
@router.post("/api/Events/ReadSpecialEventTips", name="Events_ReadSpecialEventTips")
async def events_read_special_event_tips(
    request: Request, mSpecialEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Events/ReadTips/{mStoryEventId}
@router.post("/api/Events/ReadTips/{mStoryEventId}", name="Events_ReadTips")
async def events_read_tips(request: Request, mStoryEventId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Events/CircleEvent/ReceiveCirclePointReward/{circleEventMasterId}
@router.post(
    "/api/Events/CircleEvent/ReceiveCirclePointReward/{circleEventMasterId}",
    name="Events_ReceiveCircleEventCirclePointReward",
)
async def events_receive_circle_event_circle_point_reward(
    request: Request, circleEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Events/ReceiveStoryEventCircleMissionAllRewards/{mStoryEventId}
@router.post(
    "/api/Events/ReceiveStoryEventCircleMissionAllRewards/{mStoryEventId}",
    name="Events_ReceiveStoryEventCircleMissionAllReward",
)
async def events_receive_story_event_circle_mission_all_reward(
    request: Request, mStoryEventId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Events/ReceiveStoryEventCircleMissionReward/{mStoryEventId}/{receiveMStoryEventCircleMissionRewardId}
@router.post(
    "/api/Events/ReceiveStoryEventCircleMissionReward/{mStoryEventId}/{receiveMStoryEventCircleMissionRewardId}",
    name="Events_ReceiveStoryEventCircleMissionReward",
)
async def events_receive_story_event_circle_mission_reward(
    request: Request, mStoryEventId: int, receiveMStoryEventCircleMissionRewardId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(ReceivedThing())


# /api/Events/ReceiveTotalPointEventReward?mTotalPointEventId=
@router.post(
    "/api/Events/ReceiveTotalPointEventReward",
    name="Events_ReceiveTotalPointEventReward",
)
async def events_receive_total_point_event_reward(
    request: Request, mTotalPointEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Events/CircleEvent/ResetMissionCount/{circleEventMasterId}
@router.post(
    "/api/Events/CircleEvent/ResetMissionCount/{circleEventMasterId}",
    name="Events_ResetCircleEventMisionCount",
)
async def events_reset_circle_event_mision_count(
    request: Request, circleEventMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Events/BoxGacha/Reset/{eventBoxGachaMasterId}
@router.post(
    "/api/Events/BoxGacha/Reset/{eventBoxGachaMasterId}",
    name="Events_ResetEventBoxGacha",
)
async def events_reset_event_box_gacha(request: Request, eventBoxGachaMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Events/BoxGacha/Roll/{eventBoxGachaDetailMasterId}
@router.post(
    "/api/Events/BoxGacha/Roll/{eventBoxGachaDetailMasterId}",
    name="Events_RollEventBoxGacha",
)
async def events_roll_event_box_gacha(
    request: Request, eventBoxGachaDetailMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(EventBoxGachaRollResult())


# /api/Events/DugongRun/{dugongRunCourseMasterId}/Clear/{clearType}
@router.post(
    "/api/Events/DugongRun/{dugongRunCourseMasterId}/Clear/{clearType}",
    name="Events_SaveDugongRunClearStatus",
)
async def events_save_dugong_run_clear_status(
    request: Request, dugongRunCourseMasterId: int, clearType: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Events/SelectCamp?eventMasterId=&campType=
@router.post("/api/Events/SelectCamp", name="Events_SelectCamp")
async def events_select_camp(
    request: Request,
    eventMasterId: Optional[int] = None,
    campType: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Events/CharacterPoint/SetCharacter/{characterPointEventMasterId}/{characterBaseMasterId}
@router.post(
    "/api/Events/CharacterPoint/SetCharacter/{characterPointEventMasterId}/{characterBaseMasterId}",
    name="Events_SetCharacterPointEventCharacter",
)
async def events_set_character_point_event_character(
    request: Request, characterPointEventMasterId: int, characterBaseMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
