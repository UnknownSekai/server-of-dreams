"""High-level WDS API client — one method per ground-truth route (AUTO-GENERATED).

Each route was recovered from the binary by resolving the operation method's route
string through the ELF relocations. Verbs + body/no-body come from the IHttpClientFactory
dispatch. Object/array payloads are sent as a MessagePack [Key(n)] array body; scalar
arguments are sent as query parameters (their names match the ?key= hints in the route).
Results decode into models_generated.py types when known.
"""

from __future__ import annotations

from typing import Any, Optional

from .transport import SiriusApiClient


class WdsApiClient(SiriusApiClient):
    """Typed facade over every ground-truth route."""

    def accessories_sell(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Accessories/Sell  (op Accessories_Sell) -> BooleanResult\n        params: SellAccessoryPayload payload"""
        return self.request(
            "/api/Accessories/Sell",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def accessories_set_accessory_favorite(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Accessories/SetFavorite  (op Accessories_SetAccessoryFavorite) -> BooleanResult\n        params: AccessoryFavoritePayload payload"""
        return self.request(
            "/api/Accessories/SetFavorite",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def account_authenticate(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Account/Authenticate  (op Account_Authenticate) -> AuthenticateResult\n        params: AuthenticatePayload payload"""
        return self.request(
            "/api/Account/Authenticate",
            method=method,
            payload=payload,
            query=None,
            result_model="AuthenticateResult",
            result_is_array=False,
            raw=raw,
        )

    def account_connect_account(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Account/ConnectAccount  (op Account_ConnectAccount) -> BooleanResult\n        params: AccountConnectPayload payload"""
        return self.request(
            "/api/Account/ConnectAccount",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def account_delete_account(self, method: str = "POST", raw: bool = False):
        """POST /api/Account/Delete  (op Account_DeleteAccount) -> AccountDeletionResult"""
        return self.request(
            "/api/Account/Delete",
            method=method,
            payload=None,
            query=None,
            result_model="AccountDeletionResult",
            result_is_array=False,
            raw=raw,
        )

    def account_get_confirmation_code(self, method: str = "POST", raw: bool = False):
        """POST /api/Account/GetConfirmationCode  (op Account_GetConfirmationCode) -> TimedConfirmationCode"""
        return self.request(
            "/api/Account/GetConfirmationCode",
            method=method,
            payload=None,
            query=None,
            result_model="TimedConfirmationCode",
            result_is_array=False,
            raw=raw,
        )

    def account_get_current_user_data(self, method: str = "GET", raw: bool = False):
        """GET /api/Account/GetCurrentUserData  (op Account_GetCurrentUserData) -> UserResult"""
        return self.request(
            "/api/Account/GetCurrentUserData",
            method=method,
            payload=None,
            query=None,
            result_model="UserResult",
            result_is_array=False,
            raw=raw,
        )

    def account_get_precedence_transition_token(
        self, method: str = "GET", raw: bool = False
    ):
        """GET /api/Account/GetPrecedenceTransitionToken  (op Account_GetPrecedenceTransitionToken) -> TransitionTokenResult"""
        return self.request(
            "/api/Account/GetPrecedenceTransitionToken",
            method=method,
            payload=None,
            query=None,
            result_model="TransitionTokenResult",
            result_is_array=False,
            raw=raw,
        )

    def account_get_rooot_transition_token(
        self, method: str = "GET", raw: bool = False
    ):
        """GET /api/Account/GetRoootTransitionToken  (op Account_GetRoootTransitionToken) -> TransitionTokenResult"""
        return self.request(
            "/api/Account/GetRoootTransitionToken",
            method=method,
            payload=None,
            query=None,
            result_model="TransitionTokenResult",
            result_is_array=False,
            raw=raw,
        )

    def account_get_take_over_account(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Account/GetTakeOverAccount  (op Account_GetTakeOverAccount) -> TakeOverAccountResult\n        params: TakeOverAccountPayload payload"""
        return self.request(
            "/api/Account/GetTakeOverAccount",
            method=method,
            payload=payload,
            query=None,
            result_model="TakeOverAccountResult",
            result_is_array=False,
            raw=raw,
        )

    def account_register(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Account/Register  (op Account_Register) -> AccountRegistResult\n        params: RegisterPayload payload"""
        return self.request(
            "/api/Account/Register",
            method=method,
            payload=payload,
            query=None,
            result_model="AccountRegistResult",
            result_is_array=False,
            raw=raw,
        )

    def account_register_take_over_password(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Account/RegisterTakeOverPassword  (op Account_RegisterTakeOverPassword) -> TakeOverCodeResult\n        params: RegisterTakeOverPasswordPayload payload"""
        return self.request(
            "/api/Account/RegisterTakeOverPassword",
            method=method,
            payload=payload,
            query=None,
            result_model="TakeOverCodeResult",
            result_is_array=False,
            raw=raw,
        )

    def account_take_over_with_account_connect(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Account/TakeOverWithAccountConnect  (op Account_TakeOverWithAccountConnect) -> TakeOverAccountResult\n        params: AccountConnectPayload payload"""
        return self.request(
            "/api/Account/TakeOverWithAccountConnect",
            method=method,
            payload=payload,
            query=None,
            result_model="TakeOverAccountResult",
            result_is_array=False,
            raw=raw,
        )

    def account_update_birth_date(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Account/UpdateBirthDate  (op Account_UpdateBirthDate) -> BooleanResult\n        params: RegisterBirthDayPayload payload"""
        return self.request(
            "/api/Account/UpdateBirthDate",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def character_mission_receive_all_mission_rewards_all(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/CharacterMissions/BulkReceiveAllMission  (op CharacterMission_ReceiveAllMissionRewardsAll) -> CharacterBaseStarPointResult[]\n        params: long[] mCharacterBaseIds"""
        return self.request(
            "/api/CharacterMissions/BulkReceiveAllMission",
            method=method,
            payload=payload,
            query=None,
            result_model="CharacterBaseStarPointResult",
            result_is_array=True,
            raw=raw,
        )

    def character_mission_check_initialize_character_missions(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/CharacterMissions/checkInitializeMissions  (op CharacterMission_CheckInitializeCharacterMissions) -> BooleanResult"""
        return self.request(
            "/api/CharacterMissions/checkInitializeMissions",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def characters_bulk_level_up(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Characters/BulkLevelUp  (op Characters_BulkLevelUp) -> BooleanResult\n        params: BulkLevelUpPayload[] payloads"""
        return self.request(
            "/api/Characters/BulkLevelUp",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def characters_set_portal_m_character(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Characters/Portal/SetCharacter  (op Characters_SetPortalMCharacter) -> BooleanResult\n        params: ActorPortalCharacterPayload payload"""
        return self.request(
            "/api/Characters/Portal/SetCharacter",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def characters_set_character_favorite(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Characters/SetFavorite  (op Characters_SetCharacterFavorite) -> BooleanResult\n        params: CharacterFavoritePayload payload"""
        return self.request(
            "/api/Characters/SetFavorite",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_circle(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles?circleId=  (op Circles_GetCircle) -> CircleInformationResult\n        params: string circleId"""
        return self.request(
            "/api/Circles",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleInformationResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_circles(self, method: str = "GET", raw: bool = False):
        """GET /api/Circles  (op Circles_GetCircles) -> CircleInformationResult[]"""
        return self.request(
            "/api/Circles",
            method=method,
            payload=None,
            query=None,
            result_model="CircleInformationResult",
            result_is_array=True,
            raw=raw,
        )

    def circles_authority_change_circle(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/AuthorityChange  (op Circles_AuthorityChangeCircle) -> CircleAuthorityResult\n        params: CircleAuthorityChangePayload payload"""
        return self.request(
            "/api/Circles/AuthorityChange",
            method=method,
            payload=payload,
            query=None,
            result_model="CircleAuthorityResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_circles_condition_search(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/Condition  (op Circles_GetCirclesConditionSearch) -> CircleInformationResult[]\n        params: CirclePayload payload"""
        return self.request(
            "/api/Circles/Condition",
            method=method,
            payload=payload,
            query=None,
            result_model="CircleInformationResult",
            result_is_array=True,
            raw=raw,
        )

    def circles_create_circle(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/Create  (op Circles_CreateCircle) -> CreateCircleResult\n        params: CirclePayload payload"""
        return self.request(
            "/api/Circles/Create",
            method=method,
            payload=payload,
            query=None,
            result_model="CreateCircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_donate_support_company(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/DonateSupportCompany  (op Circles_DonateSupportCompany) -> DonateSupportCompanyResult\n        params: DonateSupportLevelLimitPayload payload"""
        return self.request(
            "/api/Circles/DonateSupportCompany",
            method=method,
            payload=payload,
            query=None,
            result_model="DonateSupportCompanyResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_edit_circle(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/Edit  (op Circles_EditCircle) -> CircleResult\n        params: CirclePayload payload"""
        return self.request(
            "/api/Circles/Edit",
            method=method,
            payload=payload,
            query=None,
            result_model="CircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_edit_circle_banner(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/EditCircleBanner  (op Circles_EditCircleBanner) -> BooleanResult\n        params: BannerPayload payload"""
        return self.request(
            "/api/Circles/EditCircleBanner",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_expulsion_circle(
        self,
        circle_id=None,
        expulsion_user_id=None,
        method: str = "POST",
        raw: bool = False,
    ):
        """POST /api/Circles/Expulsion?circleId=  (op Circles_ExpulsionCircle) -> CircleResult\n        params: string circleId, string expulsionUserId"""
        return self.request(
            "/api/Circles/Expulsion",
            method=method,
            payload=None,
            query={"circleId": circle_id, "expulsionUserId": expulsion_user_id},
            result_model="CircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_support_and_theater_level_information(
        self, method: str = "GET", raw: bool = False
    ):
        """GET /api/Circles/GetSupportAndTheaterLevelInformation  (op Circles_GetSupportAndTheaterLevelInformation) -> SupportCompanyInformation"""
        return self.request(
            "/api/Circles/GetSupportAndTheaterLevelInformation",
            method=method,
            payload=None,
            query=None,
            result_model="SupportCompanyInformation",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_invited_circles(self, method: str = "GET", raw: bool = False):
        """GET /api/Circles/Invited  (op Circles_GetInvitedCircles) -> CircleInformationResult[]"""
        return self.request(
            "/api/Circles/Invited",
            method=method,
            payload=None,
            query=None,
            result_model="CircleInformationResult",
            result_is_array=True,
            raw=raw,
        )

    def circles_join_circle(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/Join?circleId=  (op Circles_JoinCircle) -> CircleResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/Join",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_send_circle_pre_request(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/JoinPreRequest?circleId=  (op Circles_SendCirclePreRequest) -> CircleResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/JoinPreRequest",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_send_circlen_request(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/JoinRequest?circleId=  (op Circles_SendCirclenRequest) -> CircleResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/JoinRequest",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_circle_member_info(
        self, circle_id=None, method: str = "GET", raw: bool = False
    ):
        """GET /api/Circles/MemberInfo?circleId=  (op Circles_CircleMemberInfo) -> CircleMemberInfoResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/MemberInfo",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleMemberInfoResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_my_circle(self, method: str = "POST", raw: bool = False):
        """POST /api/Circles/MyCircleInfo  (op Circles_GetMyCircle) -> MyCircleInformationResult"""
        return self.request(
            "/api/Circles/MyCircleInfo",
            method=method,
            payload=None,
            query=None,
            result_model="MyCircleInformationResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_circle_support_point_daily_ranking(
        self, method: str = "GET", raw: bool = False
    ):
        """GET /api/Circles/Ranking/Daily  (op Circles_GetCircleSupportPointDailyRanking) -> RawRankingResult"""
        return self.request(
            "/api/Circles/Ranking/Daily",
            method=method,
            payload=None,
            query=None,
            result_model="RawRankingResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_circle_support_point_monthly_ranking(
        self, method: str = "GET", raw: bool = False
    ):
        """GET /api/Circles/Ranking/Monthly  (op Circles_GetCircleSupportPointMonthlyRanking) -> RawRankingResult"""
        return self.request(
            "/api/Circles/Ranking/Monthly",
            method=method,
            payload=None,
            query=None,
            result_model="RawRankingResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_circle_support_point_weekly_ranking(
        self, method: str = "GET", raw: bool = False
    ):
        """GET /api/Circles/Ranking/Weekly  (op Circles_GetCircleSupportPointWeeklyRanking) -> RawRankingResult"""
        return self.request(
            "/api/Circles/Ranking/Weekly",
            method=method,
            payload=None,
            query=None,
            result_model="RawRankingResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_receive_circle_theater_stamina(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/ReceiveTheaterStamina  (op Circles_ReceiveCircleTheaterStamina) -> BooleanResult"""
        return self.request(
            "/api/Circles/ReceiveTheaterStamina",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_recommend_invite_user(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/RecommendUsers?circleId=  (op Circles_RecommendInviteUser) -> CircleSearchResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/RecommendUsers",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleSearchResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_release_circle(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/Release?circleId=  (op Circles_ReleaseCircle) -> CircleResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/Release",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_resignation_circle(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/Resignation?circleId=  (op Circles_ResignationCircle) -> CircleResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/Resignation",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_get_circles_name_search(
        self, circle_name=None, method: str = "GET", raw: bool = False
    ):
        """GET /api/Circles/Search?circleName=  (op Circles_GetCirclesNameSearch) -> CircleInformationResult[]\n        params: string circleName"""
        return self.request(
            "/api/Circles/Search",
            method=method,
            payload=None,
            query={"circleName": circle_name},
            result_model="CircleInformationResult",
            result_is_array=True,
            raw=raw,
        )

    def circles_search_friend(self, method: str = "POST", raw: bool = False):
        """POST /api/Circles/Search/Friend  (op Circles_SearchFriend) -> CircleSearchResult"""
        return self.request(
            "/api/Circles/Search/Friend",
            method=method,
            payload=None,
            query=None,
            result_model="CircleSearchResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_search_inviting(self, method: str = "POST", raw: bool = False):
        """POST /api/Circles/Search/Inviting  (op Circles_SearchInviting) -> CircleSearchResult"""
        return self.request(
            "/api/Circles/Search/Inviting",
            method=method,
            payload=None,
            query=None,
            result_model="CircleSearchResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_search_request_circle(
        self, circle_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/Search/Request?circleId=  (op Circles_SearchRequestCircle) -> CircleSearchResult\n        params: string circleId"""
        return self.request(
            "/api/Circles/Search/Request",
            method=method,
            payload=None,
            query={"circleId": circle_id},
            result_model="CircleSearchResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_search_user_id_circle(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/SearchUser?targetUserId=  (op Circles_SearchUserIdCircle) -> CircleSearchIdResult\n        params: string targetUserId"""
        return self.request(
            "/api/Circles/SearchUser",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="CircleSearchIdResult",
            result_is_array=False,
            raw=raw,
        )

    def circles_send_circle_invite(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Circles/SendInvite?targetUserId=  (op Circles_SendCircleInvite) -> CircleInviteResult\n        params: string targetUserId"""
        return self.request(
            "/api/Circles/SendInvite",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="CircleInviteResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_album_simple_arranging(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/AlbumSimpleArranging  (op Debug_AlbumSimpleArranging) -> BooleanResult\n        params: DebugAlbumSimpleArrangingPayload payload"""
        return self.request(
            "/api/Debugs/AlbumSimpleArranging",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_get_cache_updated_at(self, method: str = "GET", raw: bool = False):
        """GET /api/Debugs/CacheUpdatedAt  (op Debug_GetCacheUpdatedAt) -> string"""
        return self.request(
            "/api/Debugs/CacheUpdatedAt",
            method=method,
            payload=None,
            query=None,
            raw=raw,
        )

    def debug_set_circle_support_point_info2(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/Circle/SupportCompanyLevelLimit  (op Debug_SetCircleSupportPointInfo2) -> BooleanResult\n        params: SupportCompanyLevelLimitPayload payload"""
        return self.request(
            "/api/Debugs/Circle/SupportCompanyLevelLimit",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_stamina_last_received_at(
        self, last_received_at=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/Circle/SupportPoint/StaminaLastReceivedAt/  (op Debug_SetStaminaLastReceivedAt) -> BooleanResult\n        params: string lastReceivedAt"""
        return self.request(
            "/api/Debugs/Circle/SupportPoint/StaminaLastReceivedAt/",
            method=method,
            payload=None,
            query={"lastReceivedAt": last_received_at},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_circle_usage_time_reset(
        self, set_date_time=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/CircleUsageTimeReset?setDateTime=  (op Debug_CircleUsageTimeReset) -> BooleanResult\n        params: string setDateTime"""
        return self.request(
            "/api/Debugs/CircleUsageTimeReset",
            method=method,
            payload=None,
            query={"setDateTime": set_date_time},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_get_uset_id(
        self, user_id=None, hashed_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/ConvertUserId?userId=  (op Debug_GetUsetId) -> DebugUserIdResult\n        params: string userId, string hashedUserId"""
        return self.request(
            "/api/Debugs/ConvertUserId",
            method=method,
            payload=None,
            query={"userId": user_id, "hashedUserId": hashed_user_id},
            result_model="DebugUserIdResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_create_album(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/CreateAlbum  (op Debug_CreateAlbum) -> BooleanResult"""
        return self.request(
            "/api/Debugs/CreateAlbum",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_delete_circles(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/DeleteCircles  (op Debug_DeleteCircles) -> BooleanResult"""
        return self.request(
            "/api/Debugs/DeleteCircles",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_delete_league_all_data(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/DeleteLeagueAllData  (op Debug_DeleteLeagueAllData) -> BooleanResult"""
        return self.request(
            "/api/Debugs/DeleteLeagueAllData",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_delete_league_users_data(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/DeleteLeagueUsersData  (op Debug_DeleteLeagueUsersData) -> BooleanResult\n        params: long[] userIds"""
        return self.request(
            "/api/Debugs/DeleteLeagueUsersData",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_edit_league_basic(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/EditLeagueBasic  (op Debug_EditLeagueBasic) -> BooleanResult\n        params: DebugEditLeagueBasicPayload payload"""
        return self.request(
            "/api/Debugs/EditLeagueBasic",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_execute_league_totalization(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/ExecuteLeagueTotalization  (op Debug_ExecuteLeagueTotalization) -> BooleanResult"""
        return self.request(
            "/api/Debugs/ExecuteLeagueTotalization",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_get_current_league(self, method: str = "GET", raw: bool = False):
        """GET /api/Debugs/GetCurrentLeague  (op Debug_GetCurrentLeague) -> long"""
        return self.request(
            "/api/Debugs/GetCurrentLeague",
            method=method,
            payload=None,
            query=None,
            raw=raw,
        )

    def debug_get_league_histories(self, method: str = "GET", raw: bool = False):
        """GET /api/Debugs/GetLeagueHistories  (op Debug_GetLeagueHistories) -> string"""
        return self.request(
            "/api/Debugs/GetLeagueHistories",
            method=method,
            payload=None,
            query=None,
            raw=raw,
        )

    def debug_give_enhance_items(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/GiveEnhanceItems  (op Debug_GiveEnhanceItems) -> BooleanResult"""
        return self.request(
            "/api/Debugs/GiveEnhanceItems",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_give_enhance_items_and_grow_characters_max(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/GiveEnhanceItemsAndGrowCharactersMax  (op Debug_GiveEnhanceItemsAndGrowCharactersMax) -> BooleanResult"""
        return self.request(
            "/api/Debugs/GiveEnhanceItemsAndGrowCharactersMax",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_give_enhance_items_and_grow_posters_max(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/GiveEnhanceItemsAndGrowPostersMax  (op Debug_GiveEnhanceItemsAndGrowPostersMax) -> BooleanResult"""
        return self.request(
            "/api/Debugs/GiveEnhanceItemsAndGrowPostersMax",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_give_enhance_items_and_grow_accessories_max(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/GrowAccessoriesMax  (op Debug_GiveEnhanceItemsAndGrowAccessoriesMax) -> BooleanResult"""
        return self.request(
            "/api/Debugs/GrowAccessoriesMax",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_initialize_league_basic_data(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/InitializeLeagueBasicData  (op Debug_InitializeLeagueBasicData) -> BooleanResult"""
        return self.request(
            "/api/Debugs/InitializeLeagueBasicData",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_initialize_player_rate(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/InitializePlayerRate  (op Debug_InitializePlayerRate) -> BooleanResult"""
        return self.request(
            "/api/Debugs/InitializePlayerRate",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_get_live_score_history(self, method: str = "GET", raw: bool = False):
        """GET /api/Debugs/LiveScoreHistory  (op Debug_GetLiveScoreHistory) -> ScoreWithDateResult[]"""
        return self.request(
            "/api/Debugs/LiveScoreHistory",
            method=method,
            payload=None,
            query=None,
            result_model="ScoreWithDateResult",
            result_is_array=True,
            raw=raw,
        )

    def debug_prepare_league_group_user(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/PrepareLeagueGroupUser  (op Debug_PrepareLeagueGroupUser) -> BooleanResult\n        params: DebugPrepareLeagueGroupUserPayload payload"""
        return self.request(
            "/api/Debugs/PrepareLeagueGroupUser",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_refresh_memory_cache(self, method: str = "GET", raw: bool = False):
        """GET /api/Debugs/RefreshMemoryCache  (op Debug_RefreshMemoryCache) -> BooleanResult"""
        return self.request(
            "/api/Debugs/RefreshMemoryCache",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_release_all_music_difficulty(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/ReleaseAllMusicDifficulty  (op Debug_ReleaseAllMusicDifficulty) -> BooleanResult"""
        return self.request(
            "/api/Debugs/ReleaseAllMusicDifficulty",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_reset_auto_play(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/ResetAutoPlay  (op Debug_ResetAutoPlay) -> BooleanResult"""
        return self.request(
            "/api/Debugs/ResetAutoPlay",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_reset_lesson(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/ResetLesson  (op Debug_ResetLesson) -> BooleanResult"""
        return self.request(
            "/api/Debugs/ResetLesson",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_accessories(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendAccessories  (op Debug_SendAccessories) -> BooleanResult\n        params: long[] mAccessoryIds"""
        return self.request(
            "/api/Debugs/SendAccessories",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_albu_themes(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendAlbumThemes  (op Debug_SendAlbuThemes) -> BooleanResult\n        params: long[] mAlbumThemeIds"""
        return self.request(
            "/api/Debugs/SendAlbumThemes",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_bombs(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendBombs  (op Debug_SendBombs) -> BooleanResult\n        params: long[] mBombIds"""
        return self.request(
            "/api/Debugs/SendBombs",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_characters(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendCharacters  (op Debug_SendCharacters) -> BooleanResult\n        params: AcquirableThingsPayload payload"""
        return self.request(
            "/api/Debugs/SendCharacters",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_chatwork_message(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendChatworkMessage  (op Debug_SendChatworkMessage) -> BooleanResult\n        params: ChatworkSendMessagePayload payload"""
        return self.request(
            "/api/Debugs/SendChatworkMessage",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_costumes(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendCostumes  (op Debug_SendCostumes) -> BooleanResult\n        params: long[] mCostumeIds"""
        return self.request(
            "/api/Debugs/SendCostumes",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_decorations(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendDecorations  (op Debug_SendDecorations) -> BooleanResult\n        params: long[] mDecorationIds"""
        return self.request(
            "/api/Debugs/SendDecorations",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_home_skins(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendHomeSkins  (op Debug_SendHomeSkins) -> BooleanResult\n        params: long[] mHomeSkinIds"""
        return self.request(
            "/api/Debugs/SendHomeSkins",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_icon_frames(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendIconFrames  (op Debug_SendIconFrames) -> BooleanResult\n        params: long[] mIconFrameIds"""
        return self.request(
            "/api/Debugs/SendIconFrames",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_items(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendItems  (op Debug_SendItems) -> BooleanResult\n        params: AcquirableThingsPayload payload"""
        return self.request(
            "/api/Debugs/SendItems",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_musics(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendMusics  (op Debug_SendMusics) -> BooleanResult\n        params: long[] mMusicIds"""
        return self.request(
            "/api/Debugs/SendMusics",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_name_base_colors(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendNameBaseColors  (op Debug_SendNameBaseColors) -> BooleanResult\n        params: long[] mNameBaseColorIds"""
        return self.request(
            "/api/Debugs/SendNameBaseColors",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_name_colors(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendNameColors  (op Debug_SendNameColors) -> BooleanResult\n        params: long[] mNameColorIds"""
        return self.request(
            "/api/Debugs/SendNameColors",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_nameplates(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendNameplates  (op Debug_SendNameplates) -> BooleanResult\n        params: long[] mNamePlateIds"""
        return self.request(
            "/api/Debugs/SendNameplates",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_notes(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendNotes  (op Debug_SendNotes) -> BooleanResult\n        params: long[] mNoteIds"""
        return self.request(
            "/api/Debugs/SendNotes",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_notification(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/SendNotification  (op Debug_SendNotification) -> BooleanResult"""
        return self.request(
            "/api/Debugs/SendNotification",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_posters(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendPosters  (op Debug_SendPosters) -> BooleanResult\n        params: AcquirableThingsPayload payload"""
        return self.request(
            "/api/Debugs/SendPosters",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_stamp(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendStamps  (op Debug_SendStamp) -> BooleanResult\n        params: long[] mStampIds"""
        return self.request(
            "/api/Debugs/SendStamps",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_send_trophies(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SendTrophies  (op Debug_SendTrophies) -> BooleanResult\n        params: long[] mTrophyIds"""
        return self.request(
            "/api/Debugs/SendTrophies",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_character_enhance_info(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SetCharacterEnhanceInfo  (op Debug_SetCharacterEnhanceInfo) -> BooleanResult\n        params: DebugModifyCharacterEnhanceInformationPayload[] payloads"""
        return self.request(
            "/api/Debugs/SetCharacterEnhanceInfo",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_login_pass_until(
        self, until=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SetLoginPassUntil?until=  (op Debug_SetLoginPassUntil) -> BooleanResult\n        params: string until"""
        return self.request(
            "/api/Debugs/SetLoginPassUntil",
            method=method,
            payload=None,
            query={"until": until},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_player_rate(self, rate=None, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/SetPlayerRate?rate=  (op Debug_SetPlayerRate) -> BooleanResult\n        params: string rate"""
        return self.request(
            "/api/Debugs/SetPlayerRate",
            method=method,
            payload=None,
            query={"rate": rate},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_poster_enhance_info(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SetPosterEnhanceInfo  (op Debug_SetPosterEnhanceInfo) -> BooleanResult\n        params: DebugModifyPosterEnhanceInformationPayload[] payloads"""
        return self.request(
            "/api/Debugs/SetPosterEnhanceInfo",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_server_time(
        self, date_time=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SetServerTime?dateTime=  (op Debug_SetServerTime) -> BooleanResult\n        params: string dateTime"""
        return self.request(
            "/api/Debugs/SetServerTime",
            method=method,
            payload=None,
            query={"dateTime": date_time},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_splash_last_displayed_at(
        self, displayed_at_text=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SetSplashLastDisplayedAt?displayedAtText=  (op Debug_SetSplashLastDisplayedAt) -> BooleanResult\n        params: string displayedAtText"""
        return self.request(
            "/api/Debugs/SetSplashLastDisplayedAt",
            method=method,
            payload=None,
            query={"displayedAtText": displayed_at_text},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_set_time_warp_by_date(
        self, set_date_time=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/SetTimeWarpByDate?setDateTime=  (op Debug_SetTimeWarpByDate) -> BooleanResult\n        params: string setDateTime"""
        return self.request(
            "/api/Debugs/SetTimeWarpByDate",
            method=method,
            payload=None,
            query={"setDateTime": set_date_time},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_unlock_all_features(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/UnlockAllFeatures  (op Debug_UnlockAllFeatures) -> BooleanResult"""
        return self.request(
            "/api/Debugs/UnlockAllFeatures",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_upload_toutch_log(
        self, logs=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Debugs/UploadToutchLog  (op Debug_UploadToutchLog) -> UrlResult\n        params: string logs"""
        return self.request(
            "/api/Debugs/UploadToutchLog",
            method=method,
            payload=logs,
            query=None,
            result_model="UrlResult",
            result_is_array=False,
            raw=raw,
        )

    def debug_grant_all_thing(self, method: str = "POST", raw: bool = False):
        """POST /api/Debugs/Yokubari  (op Debug_GrantAllThing) -> BooleanResult"""
        return self.request(
            "/api/Debugs/Yokubari",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def environment_ping(self, method: str = "GET", raw: bool = False):
        """GET /api/Environment/Ping  (op Environment_Ping) -> BooleanResult"""
        return self.request(
            "/api/Environment/Ping",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def events_edit_trial_party_event_party(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Events/TrialPartyEvent/EditParty  (op Events_EditTrialPartyEventParty) -> BooleanResult\n        params: EditTrialPartyEventStagePartyPayload payload"""
        return self.request(
            "/api/Events/TrialPartyEvent/EditParty",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def flash_sale_read_flash_sale_stage(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/FlashSale/ReadFlashSaleStage  (op FlashSale_ReadFlashSaleStage) -> BooleanResult\n        params: FlashSaleReadStagePayload payload"""
        return self.request(
            "/api/FlashSale/ReadFlashSaleStage",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friend_invitation_check_invitation_code_info(
        self, invitation_code=None, method: str = "GET", raw: bool = False
    ):
        """GET /api/FriendInvitation/Check?invitationCode=  (op FriendInvitation_CheckInvitationCodeInfo) -> FriendInvitationUserInfoResult\n        params: string invitationCode"""
        return self.request(
            "/api/FriendInvitation/Check",
            method=method,
            payload=None,
            query={"invitationCode": invitation_code},
            result_model="FriendInvitationUserInfoResult",
            result_is_array=False,
            raw=raw,
        )

    def friend_invitation_activate_invitation_code(
        self, invitation_code=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/FriendInvitation/Input?invitationCode=  (op FriendInvitation_ActivateInvitationCode) -> BooleanResult\n        params: string invitationCode"""
        return self.request(
            "/api/FriendInvitation/Input",
            method=method,
            payload=None,
            query={"invitationCode": invitation_code},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friend_invitation_receive_invitation_mission_rewards(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/FriendInvitation/Receive  (op FriendInvitation_ReceiveInvitationMissionRewards) -> ReceivedThing[]\n        params: FriendInvitationMissionPayload payload"""
        return self.request(
            "/api/FriendInvitation/Receive",
            method=method,
            payload=payload,
            query=None,
            result_model="ReceivedThing",
            result_is_array=True,
            raw=raw,
        )

    def friend_invitation_update_invitation_mission(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/FriendInvitation/Update  (op FriendInvitation_UpdateInvitationMission) -> BooleanResult"""
        return self.request(
            "/api/FriendInvitation/Update",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_get_friends(self, method: str = "GET", raw: bool = False):
        """GET /api/Friends  (op Friends_GetFriends) -> FriendListResult"""
        return self.request(
            "/api/Friends",
            method=method,
            payload=None,
            query=None,
            result_model="FriendListResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_accept_friend_request(
        self, from_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/AcceptRequest?fromUserId=  (op Friends_AcceptFriendRequest) -> FriendAcceptResult\n        params: string fromUserId"""
        return self.request(
            "/api/Friends/AcceptRequest",
            method=method,
            payload=None,
            query={"fromUserId": from_user_id},
            result_model="FriendAcceptResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_block_user(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/BlockUser?targetUserId=  (op Friends_BlockUser) -> BooleanResult\n        params: string targetUserId"""
        return self.request(
            "/api/Friends/BlockUser",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_block_users(self, method: str = "GET", raw: bool = False):
        """GET /api/Friends/BlockUsers  (op Friends_BlockUsers) -> BlockListResult"""
        return self.request(
            "/api/Friends/BlockUsers",
            method=method,
            payload=None,
            query=None,
            result_model="BlockListResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_cancel_friend_request(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/CancelRequest?targetUserId=  (op Friends_CancelFriendRequest) -> BooleanResult\n        params: string targetUserId"""
        return self.request(
            "/api/Friends/CancelRequest",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_deny_friend_request(
        self, from_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/DenyRequest?fromUserId=  (op Friends_DenyFriendRequest) -> BooleanResult\n        params: string fromUserId"""
        return self.request(
            "/api/Friends/DenyRequest",
            method=method,
            payload=None,
            query={"fromUserId": from_user_id},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_remove_block_user(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/RemoveBlockUser?targetUserId=  (op Friends_RemoveBlockUser) -> BooleanResult\n        params: string targetUserId"""
        return self.request(
            "/api/Friends/RemoveBlockUser",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_remove_friend(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/RemoveFriend?targetUserId=  (op Friends_RemoveFriend) -> BooleanResult\n        params: string targetUserId"""
        return self.request(
            "/api/Friends/RemoveFriend",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_search_friend(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/Search?targetUserId=  (op Friends_SearchFriend) -> FriendSearchResult\n        params: string targetUserId"""
        return self.request(
            "/api/Friends/Search",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="FriendSearchResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_send_friend_request(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/SendRequest?targetUserId=  (op Friends_SendFriendRequest) -> FriendRequestResult\n        params: string targetUserId"""
        return self.request(
            "/api/Friends/SendRequest",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="FriendRequestResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_set_friend_favorite(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Friends/SetFavorite  (op Friends_SetFriendFavorite) -> BooleanResult\n        params: FriendFavoritePayload payload"""
        return self.request(
            "/api/Friends/SetFavorite",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def gachas_get_available_gachas(self, method: str = "GET", raw: bool = False):
        """GET /api/Gachas  (op Gachas_GetAvailableGachas) -> GachaInfoResult[]"""
        return self.request(
            "/api/Gachas",
            method=method,
            payload=None,
            query=None,
            result_model="GachaInfoResult",
            result_is_array=True,
            raw=raw,
        )

    def home_check_eexternal_payment(self, method: str = "POST", raw: bool = False):
        """POST /api/Home/CheckEexternalPayment  (op Home_CheckEexternalPayment) -> EexternalPaymentResult"""
        return self.request(
            "/api/Home/CheckEexternalPayment",
            method=method,
            payload=None,
            query=None,
            result_model="EexternalPaymentResult",
            result_is_array=False,
            raw=raw,
        )

    def home_check_receive_login_bonus(self, method: str = "POST", raw: bool = False):
        """POST /api/Home/CheckReceiveLoginBonus  (op Home_CheckReceiveLoginBonus) -> LoginBonusResult[]"""
        return self.request(
            "/api/Home/CheckReceiveLoginBonus",
            method=method,
            payload=None,
            query=None,
            result_model="LoginBonusResult",
            result_is_array=True,
            raw=raw,
        )

    def home_get_multi_live_restriction_notification(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Home/GetMultiLiveRestrictionNotification  (op Home_GetMultiLiveRestrictionNotification) -> BooleanResult"""
        return self.request(
            "/api/Home/GetMultiLiveRestrictionNotification",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def home_get_notifications(self, method: str = "POST", raw: bool = False):
        """POST /api/Home/GetNotificationsAsync  (op Home_GetNotifications) -> NotificationResult[]"""
        return self.request(
            "/api/Home/GetNotificationsAsync",
            method=method,
            payload=None,
            query=None,
            result_model="NotificationResult",
            result_is_array=True,
            raw=raw,
        )

    def home_get_notifications_anonymous(self, method: str = "GET", raw: bool = False):
        """GET /api/Home/GetNotificationsInTitleAsync  (op Home_GetNotificationsAnonymous) -> NotificationResult[]"""
        return self.request(
            "/api/Home/GetNotificationsInTitleAsync",
            method=method,
            payload=None,
            query=None,
            result_model="NotificationResult",
            result_is_array=True,
            raw=raw,
        )

    def home_update_notification_read_time(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Home/UpdateNotificationReadTime  (op Home_UpdateNotificationReadTime) -> BooleanResult\n        params: ReadNotificationPayload payload"""
        return self.request(
            "/api/Home/UpdateNotificationReadTime",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def inbox_bulk_receive(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Inboxes/BulkReceive  (op Inbox_BulkReceive) -> InboxReceiveResult\n        params: BulkReceivePayload payload"""
        return self.request(
            "/api/Inboxes/BulkReceive",
            method=method,
            payload=payload,
            query=None,
            result_model="InboxReceiveResult",
            result_is_array=False,
            raw=raw,
        )

    def inbox_check_packages(self, method: str = "POST", raw: bool = False):
        """POST /api/Inboxes/CheckPackagesAsync  (op Inbox_CheckPackages) -> BooleanResult"""
        return self.request(
            "/api/Inboxes/CheckPackagesAsync",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def items_exchange_character_piece(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Items/ExchangeCharacterPiece  (op Items_ExchangeCharacterPiece) -> ReceivedThing\n        params: long[] itemMasterIds"""
        return self.request(
            "/api/Items/ExchangeCharacterPiece",
            method=method,
            payload=payload,
            query=None,
            result_model="ReceivedThing",
            result_is_array=False,
            raw=raw,
        )

    def items_use_recovery_stamina_items(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Items/UseStaminaRecoveryItems  (op Items_UseRecoveryStaminaItems) -> BooleanResult\n        params: UseStaminaRecoveryItemsPayload payload"""
        return self.request(
            "/api/Items/UseStaminaRecoveryItems",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def leagues_send_thing_league_rewards(self, method: str = "GET", raw: bool = False):
        """GET /api/Leagues  (op Leagues_SendThingLeagueRewards) -> LeagueReceiveResults"""
        return self.request(
            "/api/Leagues",
            method=method,
            payload=None,
            query=None,
            result_model="LeagueReceiveResults",
            result_is_array=False,
            raw=raw,
        )

    def leagues_get_top_menu_information(self, method: str = "POST", raw: bool = False):
        """POST /api/Leagues/TopMenuInformation  (op Leagues_GetTopMenuInformation) -> LeagueTopMenuInformationResult"""
        return self.request(
            "/api/Leagues/TopMenuInformation",
            method=method,
            payload=None,
            query=None,
            result_model="LeagueTopMenuInformationResult",
            result_is_array=False,
            raw=raw,
        )

    def lessons_start(
        self,
        payload: Any = None,
        character_base_master_id=None,
        live_master_id=None,
        method: str = "POST",
        raw: bool = False,
    ):
        """POST /api/Lessons/  (op Lessons_Start) -> BooleanResult\n        params: string characterBaseMasterId, string liveMasterId, StartLessonPayload payload"""
        return self.request(
            "/api/Lessons/",
            method=method,
            payload=payload,
            query={
                "characterBaseMasterId": character_base_master_id,
                "liveMasterId": live_master_id,
            },
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def lessons_finish(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lessons/Finish  (op Lessons_Finish) -> BooleanResult\n        params: FinishLessonPayload payload"""
        return self.request(
            "/api/Lessons/Finish",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def lives_calculate_lesson_timing_events(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/CalculateLessonTimingEvents  (op Lives_CalculateLessonTimingEvents) -> LiveTimeEvent\n        params: CalculateLessonTimeEventPayload payload"""
        return self.request(
            "/api/Lives/CalculateLessonTimingEvents",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveTimeEvent",
            result_is_array=False,
            raw=raw,
        )

    def lives_calculate_time_events(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/CalculateTimingEvents  (op Lives_CalculateTimeEvents) -> LiveTimeEvent\n        params: CalculateTimeEventPayload payload"""
        return self.request(
            "/api/Lives/CalculateTimingEvents",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveTimeEvent",
            result_is_array=False,
            raw=raw,
        )

    def lives_finish_and_validate(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/FinishAndValidate  (op Lives_FinishAndValidate) -> FinishLiveResult\n        params: FinishLivePayload payload"""
        return self.request(
            "/api/Lives/FinishAndValidate",
            method=method,
            payload=payload,
            query=None,
            result_model="FinishLiveResult",
            result_is_array=False,
            raw=raw,
        )

    def lives_finish_another_notation_live(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/FinishAnotherNotationLive  (op Lives_FinishAnotherNotationLive) -> FinishLiveResult\n        params: FinishAnotherNotationLivePayload payload"""
        return self.request(
            "/api/Lives/FinishAnotherNotationLive",
            method=method,
            payload=payload,
            query=None,
            result_model="FinishLiveResult",
            result_is_array=False,
            raw=raw,
        )

    def lives_matching_ghost_live(self, method: str = "POST", raw: bool = False):
        """POST /api/Lives/MatchingGhostLive  (op Lives_MatchingGhostLive) -> MatchingGhostLiveResult"""
        return self.request(
            "/api/Lives/MatchingGhostLive",
            method=method,
            payload=None,
            query=None,
            result_model="MatchingGhostLiveResult",
            result_is_array=False,
            raw=raw,
        )

    def lives_edit_bookmark(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/Music/EditBookmark  (op Lives_EditBookmark) -> BooleanResult\n        params: EditBookmarkPayload payload"""
        return self.request(
            "/api/Lives/Music/EditBookmark",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def lives_retire(self, method: str = "POST", raw: bool = False):
        """POST /api/Lives/Retire  (op Lives_Retire) -> BooleanResult"""
        return self.request(
            "/api/Lives/Retire",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def lives_select_music_course_random_music(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/SelectMusicCourseRandomMusic  (op Lives_SelectMusicCourseRandomMusic) -> MusicCourseRandomSelectResult\n        params: SelectMusicCourseRandomMusicPayload payload"""
        return self.request(
            "/api/Lives/SelectMusicCourseRandomMusic",
            method=method,
            payload=payload,
            query=None,
            result_model="MusicCourseRandomSelectResult",
            result_is_array=False,
            raw=raw,
        )

    def lives_start(self, payload: Any = None, method: str = "POST", raw: bool = False):
        """POST /api/Lives/Start  (op Lives_Start) -> LiveUnit\n        params: StartLivePayload payload"""
        return self.request(
            "/api/Lives/Start",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_bonus_live(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartBonusLive  (op Lives_StartBonusLive) -> LiveUnit\n        params: StartLivePayload payload"""
        return self.request(
            "/api/Lives/StartBonusLive",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_concert(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartConcert  (op Lives_StartConcert) -> LiveUnit\n        params: StartLivePayload payload"""
        return self.request(
            "/api/Lives/StartConcert",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_ghost_live(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartGhostLive  (op Lives_StartGhostLive) -> LiveUnit\n        params: StartLivePayload payload"""
        return self.request(
            "/api/Lives/StartGhostLive",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_lesson(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartLesson  (op Lives_StartLesson) -> LiveUnit\n        params: StartLessonPayload payload"""
        return self.request(
            "/api/Lives/StartLesson",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_multi_live(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartMultiLive  (op Lives_StartMultiLive) -> LiveUnit\n        params: StartMultiLivePayload payload"""
        return self.request(
            "/api/Lives/StartMultiLive",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_multi_room_live(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartMultiRoomLive  (op Lives_StartMultiRoomLive) -> LiveUnit\n        params: StartMultiRoomLivePayload payload"""
        return self.request(
            "/api/Lives/StartMultiRoomLive",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_music_course(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartMusicCourseLive  (op Lives_StartMusicCourse) -> LiveUnit\n        params: StartLivePayload payload"""
        return self.request(
            "/api/Lives/StartMusicCourseLive",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_tournament(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartTournament  (op Lives_StartTournament) -> LiveUnit\n        params: StartTournamentPayload payload"""
        return self.request(
            "/api/Lives/StartTournament",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_trial_party_event_stage(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartTrialPartyEventStage  (op Lives_StartTrialPartyEventStage) -> LiveUnit\n        params: StartLivePayload payload"""
        return self.request(
            "/api/Lives/StartTrialPartyEventStage",
            method=method,
            payload=payload,
            query=None,
            result_model="LiveUnit",
            result_is_array=False,
            raw=raw,
        )

    def lives_start_triple_cast_live(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Lives/StartTripleCastLive  (op Lives_StartTripleCastLive) -> StartTripleCastLiveResult\n        params: StartTripleCastLivePayload payload"""
        return self.request(
            "/api/Lives/StartTripleCastLive",
            method=method,
            payload=payload,
            query=None,
            result_model="StartTripleCastLiveResult",
            result_is_array=False,
            raw=raw,
        )

    def login_login(self, payload: Any = None, method: str = "POST", raw: bool = False):
        """POST /api/Login  (op Login_Login) -> LoginResult\n        params: LoginPayload payload"""
        return self.request(
            "/api/Login",
            method=method,
            payload=payload,
            query=None,
            result_model="LoginResult",
            result_is_array=False,
            raw=raw,
        )

    def multi_room_get_multi_rooms(self, method: str = "GET", raw: bool = False):
        """GET /api/MultiRooms  (op MultiRoom_GetMultiRooms) -> MultiRoomInformationResult[]"""
        return self.request(
            "/api/MultiRooms",
            method=method,
            payload=None,
            query=None,
            result_model="MultiRoomInformationResult",
            result_is_array=True,
            raw=raw,
        )

    def multi_room_create_multi_rooms(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Create  (op MultiRoom_CreateMultiRooms) -> MultiRoomCreateResult\n        params: CreateMultiRoomPayload payload"""
        return self.request(
            "/api/MultiRooms/Create",
            method=method,
            payload=payload,
            query=None,
            result_model="MultiRoomCreateResult",
            result_is_array=False,
            raw=raw,
        )

    def multi_room_get_multi_room_detail(
        self, hashed_multi_room_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Detail?hashedMultiRoomId=  (op MultiRoom_GetMultiRoomDetail) -> MultiRoomDetailResult\n        params: string hashedMultiRoomId"""
        return self.request(
            "/api/MultiRooms/Detail",
            method=method,
            payload=None,
            query={"hashedMultiRoomId": hashed_multi_room_id},
            result_model="MultiRoomDetailResult",
            result_is_array=False,
            raw=raw,
        )

    def multi_room_get_invited_multi_rooms(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Invited  (op MultiRoom_GetInvitedMultiRooms) -> MultiRoomInvitedResult[]"""
        return self.request(
            "/api/MultiRooms/Invited",
            method=method,
            payload=None,
            query=None,
            result_model="MultiRoomInvitedResult",
            result_is_array=True,
            raw=raw,
        )

    def multi_room_join_multi_rooms(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Join  (op MultiRoom_JoinMultiRooms) -> BooleanResult\n        params: JoinMultiRoomPayload payload"""
        return self.request(
            "/api/MultiRooms/Join",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def multi_room_get_joined_multi_rooms(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Joined  (op MultiRoom_GetJoinedMultiRooms) -> MultiRoomJoinnedResult[]"""
        return self.request(
            "/api/MultiRooms/Joined",
            method=method,
            payload=None,
            query=None,
            result_model="MultiRoomJoinnedResult",
            result_is_array=True,
            raw=raw,
        )

    def multi_room_release_multi_rooms(
        self, hashed_multi_room_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Release?hashedMultiRoomId=  (op MultiRoom_ReleaseMultiRooms) -> BooleanResult\n        params: string hashedMultiRoomId"""
        return self.request(
            "/api/MultiRooms/Release",
            method=method,
            payload=None,
            query={"hashedMultiRoomId": hashed_multi_room_id},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def multi_room_resignation_multi_room(
        self, hashed_multi_room_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Resignation?hashedMultiRoomId=  (op MultiRoom_ResignationMultiRoom) -> BooleanResult\n        params: string hashedMultiRoomId"""
        return self.request(
            "/api/MultiRooms/Resignation",
            method=method,
            payload=None,
            query={"hashedMultiRoomId": hashed_multi_room_id},
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def multi_room_send_multi_room_invite(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/MultiRooms/Send/Invite  (op MultiRoom_SendMultiRoomInvite) -> BooleanResult\n        params: InviteMultiRoomPayload payload"""
        return self.request(
            "/api/MultiRooms/Send/Invite",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def kms_general_payment_process_app_store_payment(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Payments/process/appstore  (op KmsGeneralPayment_ProcessAppStorePayment) -> ProcessPaymentResult\n        params: RegisterAppStorePaymentPayload model"""
        return self.request(
            "/api/Payments/process/appstore",
            method=method,
            payload=payload,
            query=None,
            result_model="ProcessPaymentResult",
            result_is_array=False,
            raw=raw,
        )

    def kms_general_payment_process_google_play_payment(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Payments/process/googleplay  (op KmsGeneralPayment_ProcessGooglePlayPayment) -> ProcessPaymentResult\n        params: RegisterGooglePlayPaymentPayload model"""
        return self.request(
            "/api/Payments/process/googleplay",
            method=method,
            payload=payload,
            query=None,
            result_model="ProcessPaymentResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_ability_variety_up(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photo/AbilityVarietyUp  (op Photo_AbilityVarietyUp) -> BooleanResult\n        params: AbilityVarietyUpPayload payload"""
        return self.request(
            "/api/Photo/AbilityVarietyUp",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_album_detail_arranging(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photo/AlbumDetailArranging  (op Photo_AlbumDetailArranging) -> BooleanResult\n        params: AlbumArrangingPayload payload"""
        return self.request(
            "/api/Photo/AlbumDetailArranging",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_album_simple_arranging(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photo/AlbumSimpleArranging  (op Photo_AlbumSimpleArranging) -> BooleanResult\n        params: AlbumArrangingPayload payload"""
        return self.request(
            "/api/Photo/AlbumSimpleArranging",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_change_photo_ability(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photo/ChangePhotoAbility  (op Photo_ChangePhotoAbility) -> BooleanResult\n        params: ChangePhotoAbilityPayload payload"""
        return self.request(
            "/api/Photo/ChangePhotoAbility",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_get_album_main_page(
        self, target_user_id=None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photo/GetAlbumMainPage?targetUserId=  (op Photo_GetAlbumMainPage) -> AlbumPageSearchResult\n        params: string targetUserId"""
        return self.request(
            "/api/Photo/GetAlbumMainPage",
            method=method,
            payload=None,
            query={"targetUserId": target_user_id},
            result_model="AlbumPageSearchResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_set_album_publishing(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photo/SetAlbumPublishing  (op Photo_SetAlbumPublishing) -> BooleanResult\n        params: SetAlbumPublishingPayload payload"""
        return self.request(
            "/api/Photo/SetAlbumPublishing",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_set_character_base_tags(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photo/SetCharacterBaseTags  (op Photo_SetCharacterBaseTags) -> BooleanResult\n        params: SetPhotoTagPayload payload"""
        return self.request(
            "/api/Photo/SetCharacterBaseTags",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_finish_generate_photo(self, method: str = "POST", raw: bool = False):
        """POST /api/Photos/FinishGeneratePhoto  (op Photo_FinishGeneratePhoto) -> BooleanResult"""
        return self.request(
            "/api/Photos/FinishGeneratePhoto",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_generate_photo(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photos/GeneratePhoto  (op Photo_GeneratePhoto) -> GeneratePhotoResult\n        params: GeneratePhotoPayload payload"""
        return self.request(
            "/api/Photos/GeneratePhoto",
            method=method,
            payload=payload,
            query=None,
            result_model="GeneratePhotoResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_generate_photos(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photos/GeneratePhotos  (op Photo_GeneratePhotos) -> GeneratePhotoResult[]\n        params: GeneratePhotosPayload payload"""
        return self.request(
            "/api/Photos/GeneratePhotos",
            method=method,
            payload=payload,
            query=None,
            result_model="GeneratePhotoResult",
            result_is_array=True,
            raw=raw,
        )

    def photo_photo_level_up(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Photos/PhotoLevelUp  (op Photo_PhotoLevelUp) -> LevelUpPhotoResult\n        params: LevelUpPhotoPayload payload"""
        return self.request(
            "/api/Photos/PhotoLevelUp",
            method=method,
            payload=payload,
            query=None,
            result_model="LevelUpPhotoResult",
            result_is_array=False,
            raw=raw,
        )

    def photo_sell(self, payload: Any = None, method: str = "POST", raw: bool = False):
        """POST /api/Photos/Sell  (op Photo_Sell) -> BooleanResult\n        params: long[] photoIds"""
        return self.request(
            "/api/Photos/Sell",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def player_release_player_rank_cap(self, method: str = "POST", raw: bool = False):
        """POST /api/Player/ReleasePlayerRankCap  (op Player_ReleasePlayerRankCap) -> BooleanResult"""
        return self.request(
            "/api/Player/ReleasePlayerRankCap",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def player_update_caped_player_rank_announce(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Player/UpdateCapedPlayerRankAnnounce  (op Player_UpdateCapedPlayerRankAnnounce) -> BooleanResult"""
        return self.request(
            "/api/Player/UpdateCapedPlayerRankAnnounce",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def player_update_game_hint_read(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Player/UpdateGameHintRead  (op Player_UpdateGameHintRead) -> BooleanResult\n        params: UpdateGameHintPayload payload"""
        return self.request(
            "/api/Player/UpdateGameHintRead",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def player_update_home_display_preference(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Player/UpdateHomeDisplayPreference  (op Player_UpdateHomeDisplayPreference) -> BooleanResult\n        params: UpdateHomeDisplayPreferencePayload payload"""
        return self.request(
            "/api/Player/UpdateHomeDisplayPreference",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def player_update_home_last_transition_time(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/Player/UpdateSplashLastDisplayTime  (op Player_UpdateHomeLastTransitionTime) -> BooleanResult"""
        return self.request(
            "/api/Player/UpdateSplashLastDisplayTime",
            method=method,
            payload=None,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def player_update_tutorial(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Player/UpdateTutorial  (op Player_UpdateTutorial) -> BooleanResult\n        params: UpdateTutorialPayload payload"""
        return self.request(
            "/api/Player/UpdateTutorial",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def possessions_bulk_set_costume_favorite(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Possessions/SetFavorite  (op Possessions_BulkSetCostumeFavorite) -> BooleanResult\n        params: CostumeFavoritePayload payload"""
        return self.request(
            "/api/Possessions/SetFavorite",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def possessions_sort_favorite_stamps(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Possessions/SortFavoriteStamps  (op Possessions_SortFavoriteStamps) -> BooleanResult\n        params: FavoriteStampOrderPayload payload"""
        return self.request(
            "/api/Possessions/SortFavoriteStamps",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def posters_change_poster_alternative_image(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Posters/ChangePosterAlternativeImage  (op Posters_ChangePosterAlternativeImage) -> BooleanResult\n        params: PosterAlternativeImagePayload payload"""
        return self.request(
            "/api/Posters/ChangePosterAlternativeImage",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def posters_set_poster_favorite(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Posters/SetFavorite  (op Posters_SetPosterFavorite) -> BooleanResult\n        params: PosterFavoritePayload payload"""
        return self.request(
            "/api/Posters/SetFavorite",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def profile_edit(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Profiles/Edit  (op Profile_Edit) -> BooleanResult\n        params: EditUserProfilePayload payload"""
        return self.request(
            "/api/Profiles/Edit",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_get_received_request(self, method: str = "POST", raw: bool = False):
        """POST /api/ReceivedRequest  (op Friends_GetReceivedRequest) -> FriendListResult"""
        return self.request(
            "/api/ReceivedRequest",
            method=method,
            payload=None,
            query=None,
            result_model="FriendListResult",
            result_is_array=False,
            raw=raw,
        )

    def friends_get_sending_request(self, method: str = "GET", raw: bool = False):
        """GET /api/SendingRequest  (op Friends_GetSendingRequest) -> FriendListResult"""
        return self.request(
            "/api/SendingRequest",
            method=method,
            payload=None,
            query=None,
            result_model="FriendListResult",
            result_is_array=False,
            raw=raw,
        )

    def shops_exchange_market_things(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Shops/ExchangeMarketThings  (op Shops_ExchangeMarketThings) -> ReceivedThing[]\n        params: int[] numbers"""
        return self.request(
            "/api/Shops/ExchangeMarketThings",
            method=method,
            payload=payload,
            query=None,
            result_model="ReceivedThing",
            result_is_array=True,
            raw=raw,
        )

    def shops_exchange_shop_things(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Shops/ExchangeShopThings  (op Shops_ExchangeShopThings) -> ReceivedThing[]\n        params: ExchangeShopThingPayload[] payloads"""
        return self.request(
            "/api/Shops/ExchangeShopThings",
            method=method,
            payload=payload,
            query=None,
            result_model="ReceivedThing",
            result_is_array=True,
            raw=raw,
        )

    def shops_get_or_refresh_market(self, method: str = "POST", raw: bool = False):
        """POST /api/Shops/GetOrRefreshMarket  (op Shops_GetOrRefreshMarket) -> MarketResult"""
        return self.request(
            "/api/Shops/GetOrRefreshMarket",
            method=method,
            payload=None,
            query=None,
            result_model="MarketResult",
            result_is_array=False,
            raw=raw,
        )

    def shops_purchase(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Shops/Purchase  (op Shops_Purchase) -> ReceivedThing[]\n        params: PurchaseItemPayload payload"""
        return self.request(
            "/api/Shops/Purchase",
            method=method,
            payload=payload,
            query=None,
            result_model="ReceivedThing",
            result_is_array=True,
            raw=raw,
        )

    def shops_update_market_with_jewel(self, method: str = "POST", raw: bool = False):
        """POST /api/Shops/RefreshMarketWithJewel  (op Shops_UpdateMarketWithJewel) -> MarketResult"""
        return self.request(
            "/api/Shops/RefreshMarketWithJewel",
            method=method,
            payload=None,
            query=None,
            result_model="MarketResult",
            result_is_array=False,
            raw=raw,
        )

    def shops_update_last_viewed_at(
        self, payload: Any = None, method: str = "POST", raw: bool = False
    ):
        """POST /api/Shops/UpdateLastViewedAt  (op Shops_UpdateLastViewedAt) -> BooleanResult\n        params: UpdateLastViewedAtPayload payload"""
        return self.request(
            "/api/Shops/UpdateLastViewedAt",
            method=method,
            payload=payload,
            query=None,
            result_model="BooleanResult",
            result_is_array=False,
            raw=raw,
        )

    def shops_view_page(self, method: str = "POST", raw: bool = False):
        """POST /api/Shops/ViewPage  (op Shops_ViewPage) -> ViewShopResult"""
        return self.request(
            "/api/Shops/ViewPage",
            method=method,
            payload=None,
            query=None,
            result_model="ViewShopResult",
            result_is_array=False,
            raw=raw,
        )

    def leagues_send_triple_cast_thing_league_rewards(
        self, method: str = "GET", raw: bool = False
    ):
        """GET /api/TripleCast  (op Leagues_SendTripleCastThingLeagueRewards) -> LeagueReceiveResults"""
        return self.request(
            "/api/TripleCast",
            method=method,
            payload=None,
            query=None,
            result_model="LeagueReceiveResults",
            result_is_array=False,
            raw=raw,
        )

    def leagues_get_triple_cast_top_menu_information(
        self, method: str = "POST", raw: bool = False
    ):
        """POST /api/TripleCast/TopMenuInformation  (op Leagues_GetTripleCastTopMenuInformation) -> LeagueTopMenuInformationResult"""
        return self.request(
            "/api/TripleCast/TopMenuInformation",
            method=method,
            payload=None,
            query=None,
            result_model="LeagueTopMenuInformationResult",
            result_is_array=False,
            raw=raw,
        )

    def data_get_master_data(self, method: str = "GET", raw: bool = False):
        """GET /api/data/master  (op Data_GetMasterData) -> MasterDataManifest"""
        return self.request(
            "/api/data/master",
            method=method,
            payload=None,
            query=None,
            result_model="MasterDataManifest",
            result_is_array=False,
            raw=raw,
        )

    def data_get_user_data(self, method: str = "GET", raw: bool = False):
        """GET /api/data/user  (op Data_GetUserData) -> IDataObject[]"""
        return self.request(
            "/api/data/user", method=method, payload=None, query=None, raw=raw
        )

    def call_operation(
        self,
        operation: str,
        payload: Any = None,
        *,
        path: Optional[str] = None,
        query: Optional[dict] = None,
        raw: bool = False,
    ):
        """Call any of the 468 operations by name (binary-recovered verb/body/result).
        Uses the ground-truth route when known; else synthesizes /api/<Feature>/<Action>.
        """
        from .routes import OPERATION_BY_NAME, ROUTE_BY_OPERATION

        o = OPERATION_BY_NAME[operation]
        if path is None:
            r = ROUTE_BY_OPERATION.get(operation)
            if r:
                path = str(r["path"])
            else:
                feat, _, action = operation.partition("_")
                path = f"/api/{feat}/{action}"
        return self.request(
            path,
            method=str(o["method"]),
            payload=payload if o["has_body"] else None,
            query=query,
            result_model=o["result_model"],
            result_is_array=o["result_is_array"],
            raw=raw,
        )
