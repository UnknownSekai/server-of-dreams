from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Circles", tags=["Circles"])


# /api/Circles?circleId=
@router.post("/", response_model=CircleInformationResult, name="Circles_GetCircle")
async def circles_get_circle(circleId: str) -> CircleInformationResult:
    return CircleInformationResult()


# /api/Circles
@router.get(
    "/", response_model=list[CircleInformationResult], name="Circles_GetCircles"
)
async def circles_get_circles() -> list[CircleInformationResult]:
    return []


# /api/Circles/AuthorityChange
@router.post(
    "/AuthorityChange",
    response_model=CircleAuthorityResult,
    name="Circles_AuthorityChangeCircle",
)
async def circles_authority_change_circle(
    body: CircleAuthorityChangePayload,
) -> CircleAuthorityResult:
    return CircleAuthorityResult()


# /api/Circles/Condition
@router.post(
    "/Condition",
    response_model=list[CircleInformationResult],
    name="Circles_GetCirclesConditionSearch",
)
async def circles_get_circles_condition_search(
    body: CirclePayload,
) -> list[CircleInformationResult]:
    return []


# /api/Circles/Create
@router.post("/Create", response_model=CreateCircleResult, name="Circles_CreateCircle")
async def circles_create_circle(body: CirclePayload) -> CreateCircleResult:
    return CreateCircleResult()


# /api/Circles/DonateSupportCompany
@router.post(
    "/DonateSupportCompany",
    response_model=DonateSupportCompanyResult,
    name="Circles_DonateSupportCompany",
)
async def circles_donate_support_company(
    body: DonateSupportLevelLimitPayload,
) -> DonateSupportCompanyResult:
    return DonateSupportCompanyResult()


# /api/Circles/Edit
@router.post("/Edit", response_model=CircleResult, name="Circles_EditCircle")
async def circles_edit_circle(body: CirclePayload) -> CircleResult:
    return CircleResult()


# /api/Circles/EditCircleBanner
@router.post(
    "/EditCircleBanner", response_model=BooleanResult, name="Circles_EditCircleBanner"
)
async def circles_edit_circle_banner(body: BannerPayload) -> BooleanResult:
    return BooleanResult()


# /api/Circles/Expulsion?circleId=
@router.post("/Expulsion", response_model=CircleResult, name="Circles_ExpulsionCircle")
async def circles_expulsion_circle(circleId: str, expulsionUserId: str) -> CircleResult:
    return CircleResult()


# /api/Circles/GetSupportAndTheaterLevelInformation
@router.get(
    "/GetSupportAndTheaterLevelInformation",
    response_model=SupportCompanyInformation,
    name="Circles_GetSupportAndTheaterLevelInformation",
)
async def circles_get_support_and_theater_level_information() -> (
    SupportCompanyInformation
):
    return SupportCompanyInformation()


# /api/Circles/Invited
@router.get(
    "/Invited",
    response_model=list[CircleInformationResult],
    name="Circles_GetInvitedCircles",
)
async def circles_get_invited_circles() -> list[CircleInformationResult]:
    return []


# /api/Circles/Join?circleId=
@router.post("/Join", response_model=CircleResult, name="Circles_JoinCircle")
async def circles_join_circle(circleId: str) -> CircleResult:
    return CircleResult()


# /api/Circles/JoinPreRequest?circleId=
@router.post(
    "/JoinPreRequest", response_model=CircleResult, name="Circles_SendCirclePreRequest"
)
async def circles_send_circle_pre_request(circleId: str) -> CircleResult:
    return CircleResult()


# /api/Circles/JoinRequest?circleId=
@router.post(
    "/JoinRequest", response_model=CircleResult, name="Circles_SendCirclenRequest"
)
async def circles_send_circlen_request(circleId: str) -> CircleResult:
    return CircleResult()


# /api/Circles/MemberInfo?circleId=
@router.get(
    "/MemberInfo",
    response_model=CircleMemberInfoResult,
    name="Circles_CircleMemberInfo",
)
async def circles_circle_member_info(circleId: str) -> CircleMemberInfoResult:
    return CircleMemberInfoResult()


# /api/Circles/MyCircleInfo
@router.post(
    "/MyCircleInfo",
    response_model=MyCircleInformationResult,
    name="Circles_GetMyCircle",
)
async def circles_get_my_circle() -> MyCircleInformationResult:
    return MyCircleInformationResult()


# /api/Circles/Ranking/Daily
@router.get(
    "/Ranking/Daily",
    response_model=RawRankingResult,
    name="Circles_GetCircleSupportPointDailyRanking",
)
async def circles_get_circle_support_point_daily_ranking() -> RawRankingResult:
    return RawRankingResult()


# /api/Circles/Ranking/Monthly
@router.get(
    "/Ranking/Monthly",
    response_model=RawRankingResult,
    name="Circles_GetCircleSupportPointMonthlyRanking",
)
async def circles_get_circle_support_point_monthly_ranking() -> RawRankingResult:
    return RawRankingResult()


# /api/Circles/Ranking/Weekly
@router.get(
    "/Ranking/Weekly",
    response_model=RawRankingResult,
    name="Circles_GetCircleSupportPointWeeklyRanking",
)
async def circles_get_circle_support_point_weekly_ranking() -> RawRankingResult:
    return RawRankingResult()


# /api/Circles/ReceiveTheaterStamina
@router.post(
    "/ReceiveTheaterStamina",
    response_model=BooleanResult,
    name="Circles_ReceiveCircleTheaterStamina",
)
async def circles_receive_circle_theater_stamina() -> BooleanResult:
    return BooleanResult()


# /api/Circles/RecommendUsers?circleId=
@router.post(
    "/RecommendUsers",
    response_model=CircleSearchResult,
    name="Circles_RecommendInviteUser",
)
async def circles_recommend_invite_user(circleId: str) -> CircleSearchResult:
    return CircleSearchResult()


# /api/Circles/Release?circleId=
@router.post("/Release", response_model=CircleResult, name="Circles_ReleaseCircle")
async def circles_release_circle(circleId: str) -> CircleResult:
    return CircleResult()


# /api/Circles/Resignation?circleId=
@router.post(
    "/Resignation", response_model=CircleResult, name="Circles_ResignationCircle"
)
async def circles_resignation_circle(circleId: str) -> CircleResult:
    return CircleResult()


# /api/Circles/Search?circleName=
@router.get(
    "/Search",
    response_model=list[CircleInformationResult],
    name="Circles_GetCirclesNameSearch",
)
async def circles_get_circles_name_search(
    circleName: str,
) -> list[CircleInformationResult]:
    return []


# /api/Circles/Search/Friend
@router.post(
    "/Search/Friend", response_model=CircleSearchResult, name="Circles_SearchFriend"
)
async def circles_search_friend() -> CircleSearchResult:
    return CircleSearchResult()


# /api/Circles/Search/Inviting
@router.post(
    "/Search/Inviting", response_model=CircleSearchResult, name="Circles_SearchInviting"
)
async def circles_search_inviting() -> CircleSearchResult:
    return CircleSearchResult()


# /api/Circles/Search/Request?circleId=
@router.post(
    "/Search/Request",
    response_model=CircleSearchResult,
    name="Circles_SearchRequestCircle",
)
async def circles_search_request_circle(circleId: str) -> CircleSearchResult:
    return CircleSearchResult()


# /api/Circles/SearchUser?targetUserId=
@router.post(
    "/SearchUser",
    response_model=CircleSearchIdResult,
    name="Circles_SearchUserIdCircle",
)
async def circles_search_user_id_circle(targetUserId: str) -> CircleSearchIdResult:
    return CircleSearchIdResult()


# /api/Circles/SendInvite?targetUserId=
@router.post(
    "/SendInvite", response_model=CircleInviteResult, name="Circles_SendCircleInvite"
)
async def circles_send_circle_invite(targetUserId: str) -> CircleInviteResult:
    return CircleInviteResult()
