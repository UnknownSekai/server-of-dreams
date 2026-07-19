from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Circles"])


# /api/Circles/ApproveInvite/{inviteId}
@router.post(
    "/api/Circles/ApproveInvite/{inviteId}", name="Circles_ApproveCircleInvite"
)
async def circles_approve_circle_invite(request: Request, inviteId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/ApproveRequest/{requestId}
@router.post(
    "/api/Circles/ApproveRequest/{requestId}", name="Circles_ApproveCircleRequest"
)
async def circles_approve_circle_request(request: Request, requestId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/AuthorityChange
@router.post("/api/Circles/AuthorityChange", name="Circles_AuthorityChangeCircle")
async def circles_authority_change_circle(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CircleAuthorityChangePayload)
    return respond(CircleAuthorityResult())


# /api/Circles/CancelInvite/{inviteId}
@router.post(
    "/api/Circles/CancelInvite/{inviteId}", name="Circles_CancelInviteCircleInvite"
)
async def circles_cancel_invite_circle_invite(request: Request, inviteId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/MemberInfo?circleId=
@router.get("/api/Circles/MemberInfo", name="Circles_CircleMemberInfo")
async def circles_circle_member_info(request: Request, circleId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleMemberInfoResult())


# /api/Circles/Create
@router.post("/api/Circles/Create", name="Circles_CreateCircle")
async def circles_create_circle(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CirclePayload)
    return respond(CreateCircleResult())


# /api/Circles/DonateSupportCompany
@router.post("/api/Circles/DonateSupportCompany", name="Circles_DonateSupportCompany")
async def circles_donate_support_company(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, DonateSupportLevelLimitPayload)
    return respond(DonateSupportCompanyResult())


# /api/Circles/Edit
@router.post("/api/Circles/Edit", name="Circles_EditCircle")
async def circles_edit_circle(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CirclePayload)
    return respond(CircleResult())


# /api/Circles/EditCircleBanner
@router.post("/api/Circles/EditCircleBanner", name="Circles_EditCircleBanner")
async def circles_edit_circle_banner(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, BannerPayload)
    return respond(BooleanResult())


# /api/Circles/Expulsion?circleId=&expulsionUserId=
@router.post("/api/Circles/Expulsion", name="Circles_ExpulsionCircle")
async def circles_expulsion_circle(
    request: Request,
    circleId: Optional[str] = None,
    expulsionUserId: Optional[str] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles?circleId=
@router.post("/api/Circles", name="Circles_GetCircle")
async def circles_get_circle(request: Request, circleId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleInformationResult())


# /api/Circles/Ranking/Daily
@router.get(
    "/api/Circles/Ranking/Daily", name="Circles_GetCircleSupportPointDailyRanking"
)
async def circles_get_circle_support_point_daily_ranking(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Circles/Ranking/Monthly
@router.get(
    "/api/Circles/Ranking/Monthly", name="Circles_GetCircleSupportPointMonthlyRanking"
)
async def circles_get_circle_support_point_monthly_ranking(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Circles/Ranking/Weekly
@router.get(
    "/api/Circles/Ranking/Weekly", name="Circles_GetCircleSupportPointWeeklyRanking"
)
async def circles_get_circle_support_point_weekly_ranking(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(RawRankingResult())


# /api/Circles
@router.get("/api/Circles", name="Circles_GetCircles")
async def circles_get_circles(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([CircleInformationResult()])


# /api/Circles/Condition
@router.post("/api/Circles/Condition", name="Circles_GetCirclesConditionSearch")
async def circles_get_circles_condition_search(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CirclePayload)
    return respond([CircleInformationResult()])


# /api/Circles/Search?circleName=
@router.get("/api/Circles/Search", name="Circles_GetCirclesNameSearch")
async def circles_get_circles_name_search(
    request: Request, circleName: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([CircleInformationResult()])


# /api/Circles/Invited
@router.get("/api/Circles/Invited", name="Circles_GetInvitedCircles")
async def circles_get_invited_circles(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([CircleInformationResult()])


# /api/Circles/MyCircleInfo
@router.post("/api/Circles/MyCircleInfo", name="Circles_GetMyCircle")
async def circles_get_my_circle(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MyCircleInformationResult())


def _support_company_status() -> SupportCompanyLevelStatus:
    # zero status with a non-null level_limit_status (matches the official response)
    return SupportCompanyLevelStatus(
        level_limit_status=SupportCompanyLevelLimitStatus()
    )


# /api/Circles/GetSupportAndTheaterLevelInformation
@router.get(
    "/api/Circles/GetSupportAndTheaterLevelInformation",
    name="Circles_GetSupportAndTheaterLevelInformation",
)
async def circles_get_support_and_theater_level_information(request: Request):
    app: YumeApp = request.app
    return respond(  # hardcoded: all four companies at zero
        SupportCompanyInformation(
            sirius=_support_company_status(),
            eden=_support_company_status(),
            gingaza=_support_company_status(),
            denki=_support_company_status(),
        )
    )


# /api/Circles/Join?circleId=
@router.post("/api/Circles/Join", name="Circles_JoinCircle")
async def circles_join_circle(request: Request, circleId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/ReceiveTheaterStamina
@router.post(
    "/api/Circles/ReceiveTheaterStamina", name="Circles_ReceiveCircleTheaterStamina"
)
async def circles_receive_circle_theater_stamina(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Circles/RecommendUsers?circleId=
@router.post("/api/Circles/RecommendUsers", name="Circles_RecommendInviteUser")
async def circles_recommend_invite_user(
    request: Request, circleId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleSearchResult())


# /api/Circles/RejectInvite/{inviteId}
@router.post(
    "/api/Circles/RejectInvite/{inviteId}", name="Circles_RejectInviteCircleInvite"
)
async def circles_reject_invite_circle_invite(request: Request, inviteId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/RejectRequest/{requstId}
@router.post(
    "/api/Circles/RejectRequest/{requstId}", name="Circles_RejectRequestCircleInvite"
)
async def circles_reject_request_circle_invite(request: Request, requstId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/Release?circleId=
@router.post("/api/Circles/Release", name="Circles_ReleaseCircle")
async def circles_release_circle(request: Request, circleId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/Resignation?circleId=
@router.post("/api/Circles/Resignation", name="Circles_ResignationCircle")
async def circles_resignation_circle(request: Request, circleId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/Search/Friend
@router.post("/api/Circles/Search/Friend", name="Circles_SearchFriend")
async def circles_search_friend(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleSearchResult())


# /api/Circles/Search/Inviting
@router.post("/api/Circles/Search/Inviting", name="Circles_SearchInviting")
async def circles_search_inviting(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleSearchResult())


# /api/Circles/Search/Request?circleId=
@router.post("/api/Circles/Search/Request", name="Circles_SearchRequestCircle")
async def circles_search_request_circle(
    request: Request, circleId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleSearchResult())


# /api/Circles/SearchUser?targetUserId=
@router.post("/api/Circles/SearchUser", name="Circles_SearchUserIdCircle")
async def circles_search_user_id_circle(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleSearchIdResult())


# /api/Circles/SendInvite?targetUserId=
@router.post("/api/Circles/SendInvite", name="Circles_SendCircleInvite")
async def circles_send_circle_invite(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleInviteResult())


# /api/Circles/JoinPreRequest?circleId=
@router.post("/api/Circles/JoinPreRequest", name="Circles_SendCirclePreRequest")
async def circles_send_circle_pre_request(
    request: Request, circleId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/JoinRequest?circleId=
@router.post("/api/Circles/JoinRequest", name="Circles_SendCirclenRequest")
async def circles_send_circlen_request(
    request: Request, circleId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/SetIsPublishRanking/{IsPublishRanking}
@router.post(
    "/api/Circles/SetIsPublishRanking/{IsPublishRanking}",
    name="Circles_SetIsPublishRanking",
)
async def circles_set_is_publish_ranking(request: Request, IsPublishRanking: bool):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/SetSupportCompany/{company}
@router.post(
    "/api/Circles/SetSupportCompany/{company}", name="Circles_SetSupportCompany"
)
async def circles_set_support_company(request: Request, company: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(CircleResult())


# /api/Circles/SetVisibleActivityLog?isPublicActivityLog=
@router.post("/api/Circles/SetVisibleActivityLog", name="Circles_SetVisibleActivityLog")
async def circles_set_visible_activity_log(
    request: Request, isPublicActivityLog: Optional[bool] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
