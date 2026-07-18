from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Circles", tags=["Circles"])


# /api/Circles?circleId=
@router.post("/", name="Circles_GetCircle")
async def circles_get_circle(request: Request):
    return respond(CircleInformationResult())


# /api/Circles
@router.get("/", name="Circles_GetCircles")
async def circles_get_circles(request: Request):
    return respond([])


# /api/Circles/AuthorityChange
@router.post("/AuthorityChange", name="Circles_AuthorityChangeCircle")
async def circles_authority_change_circle(request: Request):
    payload = await read_request(request, "CircleAuthorityChangePayload")
    return respond(CircleAuthorityResult())


# /api/Circles/Condition
@router.post("/Condition", name="Circles_GetCirclesConditionSearch")
async def circles_get_circles_condition_search(request: Request):
    payload = await read_request(request, "CirclePayload")
    return respond([])


# /api/Circles/Create
@router.post("/Create", name="Circles_CreateCircle")
async def circles_create_circle(request: Request):
    payload = await read_request(request, "CirclePayload")
    return respond(CreateCircleResult())


# /api/Circles/DonateSupportCompany
@router.post("/DonateSupportCompany", name="Circles_DonateSupportCompany")
async def circles_donate_support_company(request: Request):
    payload = await read_request(request, "DonateSupportLevelLimitPayload")
    return respond(DonateSupportCompanyResult())


# /api/Circles/Edit
@router.post("/Edit", name="Circles_EditCircle")
async def circles_edit_circle(request: Request):
    payload = await read_request(request, "CirclePayload")
    return respond(CircleResult())


# /api/Circles/EditCircleBanner
@router.post("/EditCircleBanner", name="Circles_EditCircleBanner")
async def circles_edit_circle_banner(request: Request):
    payload = await read_request(request, "BannerPayload")
    return respond(BooleanResult())


# /api/Circles/Expulsion?circleId=
@router.post("/Expulsion", name="Circles_ExpulsionCircle")
async def circles_expulsion_circle(request: Request):
    return respond(CircleResult())


# /api/Circles/GetSupportAndTheaterLevelInformation
@router.get(
    "/GetSupportAndTheaterLevelInformation",
    name="Circles_GetSupportAndTheaterLevelInformation",
)
async def circles_get_support_and_theater_level_information(request: Request):
    return respond(SupportCompanyInformation())


# /api/Circles/Invited
@router.get("/Invited", name="Circles_GetInvitedCircles")
async def circles_get_invited_circles(request: Request):
    return respond([])


# /api/Circles/Join?circleId=
@router.post("/Join", name="Circles_JoinCircle")
async def circles_join_circle(request: Request):
    return respond(CircleResult())


# /api/Circles/JoinPreRequest?circleId=
@router.post("/JoinPreRequest", name="Circles_SendCirclePreRequest")
async def circles_send_circle_pre_request(request: Request):
    return respond(CircleResult())


# /api/Circles/JoinRequest?circleId=
@router.post("/JoinRequest", name="Circles_SendCirclenRequest")
async def circles_send_circlen_request(request: Request):
    return respond(CircleResult())


# /api/Circles/MemberInfo?circleId=
@router.get("/MemberInfo", name="Circles_CircleMemberInfo")
async def circles_circle_member_info(request: Request):
    return respond(CircleMemberInfoResult())


# /api/Circles/MyCircleInfo
@router.post("/MyCircleInfo", name="Circles_GetMyCircle")
async def circles_get_my_circle(request: Request):
    return respond(MyCircleInformationResult())


# /api/Circles/Ranking/Daily
@router.get("/Ranking/Daily", name="Circles_GetCircleSupportPointDailyRanking")
async def circles_get_circle_support_point_daily_ranking(request: Request):
    return respond(RawRankingResult())


# /api/Circles/Ranking/Monthly
@router.get("/Ranking/Monthly", name="Circles_GetCircleSupportPointMonthlyRanking")
async def circles_get_circle_support_point_monthly_ranking(request: Request):
    return respond(RawRankingResult())


# /api/Circles/Ranking/Weekly
@router.get("/Ranking/Weekly", name="Circles_GetCircleSupportPointWeeklyRanking")
async def circles_get_circle_support_point_weekly_ranking(request: Request):
    return respond(RawRankingResult())


# /api/Circles/ReceiveTheaterStamina
@router.post("/ReceiveTheaterStamina", name="Circles_ReceiveCircleTheaterStamina")
async def circles_receive_circle_theater_stamina(request: Request):
    return respond(BooleanResult())


# /api/Circles/RecommendUsers?circleId=
@router.post("/RecommendUsers", name="Circles_RecommendInviteUser")
async def circles_recommend_invite_user(request: Request):
    return respond(CircleSearchResult())


# /api/Circles/Release?circleId=
@router.post("/Release", name="Circles_ReleaseCircle")
async def circles_release_circle(request: Request):
    return respond(CircleResult())


# /api/Circles/Resignation?circleId=
@router.post("/Resignation", name="Circles_ResignationCircle")
async def circles_resignation_circle(request: Request):
    return respond(CircleResult())


# /api/Circles/Search?circleName=
@router.get("/Search", name="Circles_GetCirclesNameSearch")
async def circles_get_circles_name_search(request: Request):
    return respond([])


# /api/Circles/Search/Friend
@router.post("/Search/Friend", name="Circles_SearchFriend")
async def circles_search_friend(request: Request):
    return respond(CircleSearchResult())


# /api/Circles/Search/Inviting
@router.post("/Search/Inviting", name="Circles_SearchInviting")
async def circles_search_inviting(request: Request):
    return respond(CircleSearchResult())


# /api/Circles/Search/Request?circleId=
@router.post("/Search/Request", name="Circles_SearchRequestCircle")
async def circles_search_request_circle(request: Request):
    return respond(CircleSearchResult())


# /api/Circles/SearchUser?targetUserId=
@router.post("/SearchUser", name="Circles_SearchUserIdCircle")
async def circles_search_user_id_circle(request: Request):
    return respond(CircleSearchIdResult())


# /api/Circles/SendInvite?targetUserId=
@router.post("/SendInvite", name="Circles_SendCircleInvite")
async def circles_send_circle_invite(request: Request):
    return respond(CircleInviteResult())
