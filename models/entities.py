from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from .enums import *


class AbilityVarietyUpPayload(BaseModel):
    photo_id: Optional[int] = None
    variety_to: Optional[int] = None
    item_master_id: Optional[int] = None


class AccessoryAutoSellConvertThing(BaseModel):
    accessory_master_id: Optional[int] = None
    convert_thing: Optional[ReceivedThing] = None


class AccessoryFavoritePayload(BaseModel):
    accessory_id: Optional[int] = None
    set_favorite: Optional[bool] = None


class AccountConnectPayload(BaseModel):
    provider: Optional[AuthenticationProviders] = None
    token: Optional[str] = None


class AccountDeletionResult(BaseModel):
    is_success: Optional[bool] = None
    error: Optional[AccountDeletionErrorTypes] = None


class AccountRegistResult(BaseModel):
    token: Optional[str] = None
    error_type: Optional[AccountRegisterErrorTypes] = None


class AcquirableThing(BaseModel):
    id_: Optional[int] = None
    quantity: Optional[int] = None


class AcquirableThingsPayload(BaseModel):
    things: Optional[list[AcquirableThing]] = None


class ActorPortalCharacterPayload(BaseModel):
    character_base_id: Optional[int] = None
    character_id: Optional[int] = None
    is_awakening: Optional[bool] = None


class AlbumArrangingPayload(BaseModel):
    publishing: Optional[bool] = None
    page: Optional[int] = None
    items: Optional[list[int]] = None
    m_album_theme_id: Optional[int] = None


class AlbumPageResult(BaseModel):
    album_page_id: Optional[int] = None
    album_id: Optional[int] = None
    level: Optional[int] = None
    page: Optional[int] = None
    edit_type: Optional[EditTypes] = None
    publishing: Optional[bool] = None
    items: Optional[list[int]] = None
    album_theme_master_id: Optional[int] = None


class AlbumPageSearchResult(BaseModel):
    album_page_result: Optional[AlbumPageResult] = None
    is_success: Optional[bool] = None


class AlbumPhotoPayload(BaseModel):
    photo_id: Optional[int] = None
    order: Optional[int] = None


class AuditionClearParty(BaseModel):
    id_: Optional[int] = None
    score: Optional[int] = None
    difficulty: Optional[MusicDifficulties] = None
    slots: Optional[list[AuditionClearPartySlot]] = None
    user_name: Optional[str] = None
    rate_grade: Optional[AchievementRateGrades] = None
    player_rank: Optional[str] = None
    leader_position: Optional[int] = None


class AuditionClearPartySlot(BaseModel):
    position: Optional[int] = None
    character_master_id: Optional[int] = None
    character_level: Optional[int] = None
    character_talent_stage: Optional[int] = None
    character_awakening_phase: Optional[int] = None
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    star_rank: Optional[int] = None
    talent_stage: Optional[int] = None
    awakening_phase: Optional[int] = None
    current_status: Optional[Status] = None
    character_display_awakening_status: Optional[bool] = None


class AuditionClearedInformationParties(BaseModel):
    parties: Optional[list[AuditionClearParty]] = None
    cleared_phase: Optional[int] = None


class AuditionClearedInformationResult(BaseModel):
    parties_phases: Optional[list[AuditionClearedInformationParties]] = None


class AuthenticatePayload(BaseModel):
    login_token: Optional[str] = None
    game_version: Optional[GameVersions] = None
    apk_hash: Optional[str] = None
    apk_application_signature: Optional[str] = None
    application_version: Optional[str] = None


class AuthenticateResult(BaseModel):
    token: Optional[str] = None
    ban_level: Optional[BanLevels] = None
    warned_until: Optional[str] = None


class BannerPayload(BaseModel):
    circle_hashed_id: Optional[str] = None
    poster_master_id: Optional[int] = None
    x1: Optional[float] = None
    y1: Optional[float] = None
    x2: Optional[float] = None
    y2: Optional[float] = None
    rotation_angle: Optional[int] = None
    display_poster_string: Optional[bool] = None
    banner_ratio: Optional[float] = None


class BaseScoreBlock(BaseModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    note_id: Optional[int] = None
    timing_type: Optional[TimingTypes] = None
    combo: Optional[int] = None


class BlockListResult(BaseModel):
    results: Optional[list[FriendResult]] = None


class BonusLiveResult(BaseModel):
    rewards: Optional[list[ReceivedThing]] = None


class BooleanResult(BaseModel):
    is_success: Optional[bool] = None


class BulkLevelUpPayload(BaseModel):
    character_id: Optional[int] = None
    order: Optional[int] = None


class BulkReceivePayload(BaseModel):
    inbox_ids: Optional[list[int]] = None


class CalculateLessonTimeEventPayload(BaseModel):
    music_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None


class CalculateTimeEventPayload(BaseModel):
    music_master_id: Optional[int] = None
    sense_notation_master_id: Optional[int] = None
    party_id: Optional[int] = None
    vocal_version: Optional[int] = None
    is_story_event_challenge: Optional[bool] = None


class ChangeNamePayload(BaseModel):
    name: Optional[str] = None


class ChangePhotoAbilityPayload(BaseModel):
    photo_id: Optional[int] = None
    item_master_id: Optional[int] = None
    photo_effect_type_group_master_id: Optional[int] = None


class CharacterBaseStarPointResult(BaseModel):
    character_base_master_id: Optional[int] = None
    star_point_result: Optional[StarPointResult] = None
    link_character_received_reward: Optional[list[ReceivedThing]] = None


class CharacterFavoritePayload(BaseModel):
    character_id: Optional[int] = None
    set_favorite: Optional[bool] = None


class CharacterLineupResult(BaseModel):
    normal_probabilities: Optional[list[CharacterRarityProbability]] = None
    fixed_probabilities: Optional[list[CharacterRarityProbability]] = None
    normal_lineup_items: Optional[list[GachaLineupItemProbability]] = None
    fixed_lineup_items: Optional[list[GachaLineupItemProbability]] = None


class CharacterPointEventInformationResult(BaseModel):
    current_total_point: Optional[int] = None
    overall_rank: Optional[int] = None
    character_rank: Optional[int] = None


class CharacterPointEventRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRankingWithLongPoint]] = None
    user_profiles: Optional[list[UserProfile]] = None


class CharacterRank(BaseModel):
    m_character_base_id: Optional[int] = None
    rank: Optional[int] = None


class CharacterRarityProbability(BaseModel):
    rarity: Optional[CharacterRarities] = None
    probability: Optional[float] = None


class ChatworkSendMessagePayload(BaseModel):
    message: Optional[str] = None


class CircleAuthorityChangePayload(BaseModel):
    circle_hashed_id: Optional[str] = None
    user_id: Optional[str] = None
    authority: Optional[CircleAuthorities] = None


class CircleAuthorityResult(BaseModel):
    result_status: Optional[CircleAuthorityResultStatus] = None


class CircleBanner(BaseModel):
    poster_master_id: Optional[int] = None
    x1: Optional[float] = None
    y1: Optional[float] = None
    x2: Optional[float] = None
    y2: Optional[float] = None
    rotation_angle: Optional[int] = None
    display_poster_string: Optional[bool] = None
    banner_ratio: Optional[float] = None


class CircleEventCircleMissionProgress(BaseModel):
    circle_event_mission_master_id: Optional[int] = None
    current_count: Optional[int] = None


class CircleEventInformationResult(BaseModel):
    circle_point: Optional[int] = None
    user_point: Optional[int] = None
    last_received_circle_point: Optional[int] = None
    mission_refresh_count: Optional[int] = None
    progresses: Optional[list[CircleEventCircleMissionProgress]] = None


class CircleEventRanking(BaseModel):
    circle_raw_rankings: Optional[list[CircleRawRanking]] = None
    circle_profiles: Optional[list[CircleProfile]] = None


class CircleInformationResult(BaseModel):
    u_circle_hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: Optional[PlayTimeTypes] = None
    play_time_end_type: Optional[PlayTimeTypes] = None
    entry_type: Optional[EntryTypes] = None
    member_count: Optional[int] = None
    invite_id: Optional[int] = None
    result_status: Optional[CircleResultStatus] = None
    circle_banner: Optional[CircleBanner] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    icon_fame_master_id: Optional[int] = None


class CircleInviteResult(BaseModel):
    result_status: Optional[CircleResultStatus] = None
    invite_id: Optional[int] = None


class CircleMemberInfoParameters(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    player_rank: Optional[int] = None
    last_login_at: Optional[str] = None
    authority: Optional[CircleAuthorities] = None
    main_u_character: Optional[MainCharacter] = None
    invite_id: Optional[int] = None
    request_id: Optional[int] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    player_rate: Optional[Decimal] = None
    is_public_player_rate: Optional[bool] = None
    league_class: Optional[LeagueClassTypes] = None
    icon_fame_master_id: Optional[int] = None


class CircleMemberInfoResult(BaseModel):
    parameters: Optional[list[CircleMemberInfoParameters]] = None
    result_status: Optional[CircleResultStatus] = None
    circle_banner: Optional[CircleBanner] = None


class CircleMemberParameters(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    player_rank: Optional[int] = None
    last_login_at: Optional[str] = None
    authority: Optional[CircleAuthorities] = None
    main_u_character: Optional[MainCharacter] = None
    invite_id: Optional[int] = None
    request_id: Optional[int] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    icon_fame_master_id: Optional[int] = None


class CirclePayload(BaseModel):
    hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: Optional[PlayTimeTypes] = None
    play_time_end_type: Optional[PlayTimeTypes] = None
    entry_type: Optional[EntryTypes] = None
    member_type: Optional[SearchCircleMemberConditionTypes] = None
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None


class CircleProfile(BaseModel):
    circle_id: Optional[str] = None
    name: Optional[str] = None
    member_count: Optional[int] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    icon_frame_master_id: Optional[int] = None


class CircleRawRanking(BaseModel):
    rank: Optional[int] = None
    point: Optional[int] = None
    circle_id: Optional[str] = None


class CircleResult(BaseModel):
    result_status: Optional[CircleResultStatus] = None


class CircleSearchIdResult(BaseModel):
    parameters: Optional[CircleMemberParameters] = None
    result_status: Optional[CircleResultStatus] = None


class CircleSearchResult(BaseModel):
    parameters: Optional[list[CircleMemberParameters]] = None
    result_status: Optional[CircleResultStatus] = None
    circle_banner: Optional[CircleBanner] = None


class ConcertResult(BaseModel):
    rewards: Optional[list[ReceivedThing]] = None


class ConcoursDetailInformationResult(BaseModel):
    concours_detail_master_id: Optional[int] = None
    rank: Optional[int] = None


class ConcoursInfomationResult(BaseModel):
    details: Optional[list[ConcoursDetailInformationResult]] = None
    current_point: Optional[int] = None


class ConvertedThingResult(BaseModel):
    exchange_shop_master_id: Optional[int] = None
    original_quantity: Optional[int] = None
    received_thing: Optional[ReceivedThing] = None


class CostumeFavoritePayload(BaseModel):
    costume_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    set_favorite: Optional[bool] = None


class CourseRankingResult(BaseModel):
    rank: Optional[int] = None
    user_id: Optional[int] = None
    user_profile: Optional[UserProfile] = None
    course_result: Optional[CourseResult] = None
    note_result: Optional[NoteResult] = None


class CourseResult(BaseModel):
    total_achievement_rate_percent_record: Optional[Decimal] = None
    best_record_challenge_count: Optional[int] = None
    best_record_date: Optional[str] = None


class CreateCircleResult(BaseModel):
    result_status: Optional[CircleResultStatus] = None
    circle_hashed_id: Optional[str] = None


class CreateMultiRoomPayload(BaseModel):
    room_name: Optional[str] = None
    password: Optional[str] = None
    can_join_max_member: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    play_mode: Optional[MultiRoomPlayModes] = None
    live_master_id1: Optional[int] = None
    live_master_id2: Optional[int] = None
    live_master_id3: Optional[int] = None


class DebugAlbumSimpleArrangingPayload(BaseModel):
    publishing: Optional[bool] = None
    page: Optional[int] = None
    photos: Optional[list[AlbumPhotoPayload]] = None
    m_album_theme_id: Optional[int] = None


class DebugEditLeagueBasicPayload(BaseModel):
    current_class_type: Optional[LeagueClassTypes] = None
    best_class_type: Optional[LeagueClassTypes] = None


class DebugLinkageCodeResult(BaseModel):
    password: Optional[str] = None
    take_over_code_result: Optional[TakeOverCodeResult] = None


class DebugModifyCharacterEnhanceInformationPayload(BaseModel):
    m_character_id: Optional[int] = None
    actor_level: Optional[int] = None
    is_awaken: Optional[bool] = None
    sense_level: Optional[int] = None
    talent_bloom_stage: Optional[int] = None


class DebugModifyPosterEnhanceInformationPayload(BaseModel):
    m_poster_id: Optional[int] = None
    level: Optional[int] = None
    release_phase: Optional[int] = None


class DebugPrepareLeagueGroupUserPayload(BaseModel):
    league_master_id: Optional[int] = None
    class_type: Optional[LeagueClassTypes] = None
    user_ids: Optional[list[int]] = None


class DebugUserIdResult(BaseModel):
    user_id: Optional[str] = None
    hashed_user_id: Optional[str] = None


class Decimal(BaseModel):
    pass


class Dictionary(BaseModel):
    pass


class DonateSupportCompanyResult(BaseModel):
    my_circle_information: Optional[MyCircleInformationResult] = None
    result_status: Optional[CircleDonateSupportCompanyResult] = None


class DonateSupportLevelLimitDetail(BaseModel):
    order: Optional[int] = None
    quantity: Optional[int] = None


class DonateSupportLevelLimitPayload(BaseModel):
    company: Optional[Companies] = None
    next_level_limit: Optional[int] = None
    coin_quantity: Optional[int] = None
    details: Optional[list[DonateSupportLevelLimitDetail]] = None


class EditBookmarkPayload(BaseModel):
    music_master_id: Optional[int] = None
    bookmark_flag: Optional[MusicBookmarkFlags] = None


class EditPartyPayload(BaseModel):
    party_slots: Optional[list[EditPartySlotPayload]] = None
    sense_notation_master_id: Optional[int] = None
    music_master_id: Optional[int] = None
    vocal_version: Optional[int] = None
    is_high_score_challenge: Optional[bool] = None
    leader_position: Optional[int] = None


class EditPartySlotPayload(BaseModel):
    u_party_slot_id: Optional[int] = None
    u_character_id: Optional[int] = None
    u_accessory_id: Optional[int] = None
    u_poster_id: Optional[int] = None
    bonus_ability_enable_flags: Optional[BonusAbilityEnableFlags] = None


class EditPositionPayload(BaseModel):
    slots: Optional[list[EditPositionSlotPayload]] = None


class EditPositionSlotPayload(BaseModel):
    u_party_slot_id: Optional[int] = None
    position: Optional[int] = None


class EditTrialPartyEventStagePartyPayload(BaseModel):
    trial_party_event_stage_master_id: Optional[int] = None
    slots: Optional[list[EditTrialPartyEventStagePartyPayloadSlot]] = None
    leader_position: Optional[int] = None


class EditTrialPartyEventStagePartyPayloadSlot(BaseModel):
    position: Optional[int] = None
    trial_party_character_master_id: Optional[int] = None
    trial_party_poster_master_id: Optional[int] = None
    trial_party_accessory_master_id: Optional[int] = None


class EditUserProfilePayload(BaseModel):
    name: Optional[str] = None
    introduction: Optional[str] = None
    main_u_character_id: Optional[int] = None
    m_nameplate_id: Optional[int] = None
    m_name_color_id: Optional[int] = None
    m_trophy_id1: Optional[int] = None
    m_trophy_id2: Optional[int] = None
    m_trophy_id3: Optional[int] = None
    is_public_player_rate: Optional[bool] = None
    display_awakening_status: Optional[bool] = None
    main_character_master_id: Optional[int] = None
    name_base_color_masterid: Optional[int] = None
    icon_frame_master_id: Optional[int] = None
    home_skin_master_id: Optional[int] = None


class EexternalPaymentResult(BaseModel):
    received_jewel_shop_item_master_ids: Optional[list[int]] = None


class Effect(BaseModel):
    order: Optional[int] = None
    master_id: Optional[int] = None
    effect_types: Optional[EffectTypes] = None
    triggers: Optional[list[EffectTrigger]] = None
    targets: Optional[list[EffectTargetValue]] = None
    duration: Optional[int] = None


class EffectBranch(BaseModel):
    condition_value: Optional[int] = None
    judge_types: Optional[BranchJudgeTypes] = None
    sense_effects: Optional[list[Effect]] = None


class EffectTargetValue(BaseModel):
    target_actor_id: Optional[int] = None
    value: Optional[float] = None


class EffectTrigger(BaseModel):
    type: Optional[TriggerTypes] = None
    value: Optional[int] = None


class EnvironmentResult(BaseModel):
    application_version: Optional[str] = None
    asset_version: Optional[str] = None
    api_endpoint: Optional[str] = None
    maintenance_api_endpoint: Optional[str] = None
    news_api_endpoint: Optional[str] = None
    is_maintenance: Optional[bool] = None
    master_data_url: Optional[str] = None
    static_content_url: Optional[str] = None
    asset_url: Optional[str] = None
    is_app_review: Optional[bool] = None
    photo_content_url: Optional[str] = None
    multi_real_time_server_url: Optional[str] = None
    external_payment_url: Optional[str] = None


class EpisodeResult(BaseModel):
    episode_title: Optional[str] = None
    story_type: Optional[StoryTypes] = None
    episode_order: Optional[int] = None
    episode_detail_asset_source: Optional[str] = None


class EventBoxGachaRollResult(BaseModel):
    received_things: Optional[list[ReceivedThing]] = None
    has_reset: Optional[bool] = None
    drawn_event_box_gacha_box_thing_master_ids: Optional[list[int]] = None


class EventResult(BaseModel):
    acquired_event_point: Optional[int] = None
    attached_story_event_master_id: Optional[int] = None
    circle_event_high_score: Optional[int] = None
    circle_event_high_score_multiplier_percent: Optional[int] = None
    circle_event_before_high_score: Optional[int] = None
    high_score_before: Optional[int] = None
    high_score_after: Optional[int] = None
    before_rank: Optional[int] = None
    after_rank: Optional[int] = None
    story_event_master_id: Optional[int] = None
    event_master_id: Optional[int] = None
    this_time_support_point: Optional[int] = None
    camp_before_rank: Optional[int] = None
    camp_after_rank: Optional[int] = None


class ExchangeShopThingPayload(BaseModel):
    m_exchange_shop_thing_id: Optional[int] = None
    quantity: Optional[int] = None


class FavoriteStampOrderPayload(BaseModel):
    stamp_master_ids: Optional[list[int]] = None


class FinishAnotherNotationLivePayload(BaseModel):
    base_score_blocks: Optional[list[BaseScoreBlock]] = None
    sense_score_blocks: Optional[list[SenseScoreBlock]] = None
    star_act_score_blocks: Optional[list[StarActScoreBlock]] = None
    multi_live_additional_score_blocks: Optional[
        list[MultiLiveAdditionalScoreBlock]
    ] = None
    another_notation_master_id: Optional[int] = None
    is_auto_play: Optional[bool] = None


class FinishLessonPayload(BaseModel):
    score: Optional[int] = None
    max_combo: Optional[int] = None
    judges: Optional[list[NoteJudgePayload]] = None


class FinishLivePayload(BaseModel):
    score: Optional[int] = None
    max_combo: Optional[int] = None
    judges: Optional[list[NoteJudgePayload]] = None
    is_cleared: Optional[bool] = None
    base_score_blocks: Optional[list[BaseScoreBlock]] = None
    sense_score_blocks: Optional[list[SenseScoreBlock]] = None
    star_act_score_blocks: Optional[list[StarActScoreBlock]] = None
    multi_live_additional_score_blocks: Optional[
        list[MultiLiveAdditionalScoreBlock]
    ] = None
    triple_cast_party_scores: Optional[list[TripleCastPartyScore]] = None
    trial_party_event_stage_result: Optional[TrialPartyEventStageResult] = None


class FinishLiveResult(BaseModel):
    league_rewards: Optional[list[ReceivedThing]] = None
    rate_result: Optional[RateResult] = None
    player_rank_point_result: Optional[PlayerRankPointResult] = None
    clear_lamp: Optional[ClearLamps] = None
    rate_grade: Optional[AchievementRateGrades] = None
    is_high_score: Optional[bool] = None
    audition_before_phase: Optional[int] = None
    audition_after_phase: Optional[int] = None
    audition_rewards: Optional[list[ReceivedThing]] = None
    story_event_rewards: Optional[list[ReceivedThing]] = None
    achievement_rate_average: Optional[float] = None
    audition_master_id: Optional[int] = None
    sp_rate_update_result: Optional[SpRateUpdateResult] = None
    tournament_result: Optional[TournamentResult] = None
    celling_max_count: Optional[int] = None
    celling_user_count: Optional[int] = None
    before_clear_lamp: Optional[ClearLamps] = None
    poster_drop_up_percent: Optional[int] = None
    event_result: Optional[EventResult] = None
    live_drop_things: Optional[list[LiveDropThing]] = None
    lesson_result: Optional[LessonResult] = None
    league_result: Optional[LeagueResult] = None
    concert_result: Optional[ConcertResult] = None
    bonus_live_result: Optional[BonusLiveResult] = None
    ghost_live_result: Optional[GhostLiveResult] = None
    trial_party_event_result: Optional[TrialPartyEventResult] = None
    accessory_auto_sell_convert_things: Optional[
        list[AccessoryAutoSellConvertThing]
    ] = None


class FlashSaleReadStagePayload(BaseModel):
    read_flash_sale_stage_ids: Optional[list[int]] = None


class FriendAcceptResult(BaseModel):
    result_status: Optional[FriendAcceptResultStatus] = None


class FriendFavoritePayload(BaseModel):
    target_user_id: Optional[str] = None
    set_favorite: Optional[bool] = None


class FriendInvitationMissionPayload(BaseModel):
    friend_invitation_mission_master_ids: Optional[list[int]] = None


class FriendInvitationUserInfoResult(BaseModel):
    hashed_user_id: Optional[str] = None
    name: Optional[str] = None
    player_rank: Optional[int] = None
    result_status: Optional[InvitationCodeResultStatuses] = None


class FriendListResult(BaseModel):
    results: Optional[list[FriendResult]] = None
    current_friend_count: Optional[int] = None


class FriendRequestResult(BaseModel):
    result_status: Optional[FriendRequestResultStatus] = None


class FriendResult(BaseModel):
    user_id: Optional[str] = None
    player_rank: Optional[int] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    introduction: Optional[str] = None
    last_logged_in_at: Optional[str] = None
    name: Optional[str] = None
    player_rate: Optional[float] = None
    is_public_player_rate: Optional[bool] = None
    league_class: Optional[LeagueClassTypes] = None
    character_ranks: Optional[list[CharacterRank]] = None
    is_public_album_main_page: Optional[bool] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    icon_frame_master_id: Optional[int] = None
    is_favorite: Optional[bool] = None


class FriendSearchResult(BaseModel):
    friend_result: Optional[FriendResult] = None
    result_status: Optional[FriendSearchResultStatus] = None


class GachaHistoryResult(BaseModel):
    master_id: Optional[int] = None
    created_at: Optional[str] = None


class GachaInfoResult(BaseModel):
    id_: Optional[int] = None
    roll_limits: Optional[list[GachaRollLimit]] = None
    normal_emission_flags: Optional[GachaEmissionFlags] = None
    fixed_emission_flags: Optional[GachaEmissionFlags] = None


class GachaLineupItemProbability(BaseModel):
    id_: Optional[int] = None
    probability: Optional[float] = None


class GachaRollLimit(BaseModel):
    gacha_detail_master_id: Optional[int] = None
    roll_left: Optional[int] = None


class GachaRollResult(BaseModel):
    m_gacha_master_id: Optional[int] = None
    received_things: Optional[list[GachaThingResult]] = None
    received_bonus_things: Optional[list[ReceivedThing]] = None
    received_detail_bonus_things: Optional[list[ReceivedThing]] = None
    received_roll_bonus_things: Optional[list[ReceivedThing]] = None


class GachaSelectedThingsResult(BaseModel):
    selected_gacha_thing_ids: Optional[list[int]] = None


class GachaThingResult(BaseModel):
    received_things: Optional[list[ReceivedThing]] = None
    additional_received_things: Optional[list[ReceivedThing]] = None
    movie_costume_master_id: Optional[int] = None


class GenerateLotteryResultPayload(BaseModel):
    prize: Optional[int] = None
    amount: Optional[int] = None


class GeneratePhotoPayload(BaseModel):
    character_base_master_id: Optional[int] = None
    item_master_id: Optional[int] = None
    image_data: Optional[list[int]] = None
    thumbnail_image_data: Optional[list[int]] = None
    appeared_characters: Optional[list[PhotoAppearedCharacter]] = None


class GeneratePhotoResult(BaseModel):
    photo_id: Optional[int] = None
    file_name: Optional[str] = None
    sas_token: Optional[str] = None
    rarity: Optional[PhotoRarities] = None
    sign_master_id: Optional[int] = None
    photo_effect_master_id: Optional[int] = None


class GeneratePhotosPayload(BaseModel):
    payloads: Optional[list[GeneratePhotoPayload]] = None


class GhostLiveInfo(BaseModel):
    leader_position: Optional[int] = None
    party_slot: Optional[list[PartySlotDetail]] = None


class GhostLiveResult(BaseModel):
    ghost_user_profile: Optional[UserProfileDetail] = None
    ghost_user_score: Optional[int] = None
    total_battle_win_count: Optional[int] = None
    matching_result: Optional[MatchingResult] = None
    display_character_master_id: Optional[int] = None
    display_character_awakening_status: Optional[bool] = None


class HighScoreBuff(BaseModel):
    user_id: Optional[str] = None
    buffs: Optional[list[HighScoreBuffSetting]] = None


class HighScoreBuffSetting(BaseModel):
    story_event_high_score_buff_setting_id: Optional[int] = None
    current_level: Optional[int] = None


class HighScoreParty(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    party_name: Optional[str] = None
    slots: Optional[list[HighScorePartySlot]] = None
    difficulty: Optional[MusicDifficulties] = None
    leader_position: Optional[int] = None


class HighScorePartySlot(BaseModel):
    position: Optional[int] = None
    character_master_id: Optional[int] = None
    character_level: Optional[int] = None
    character_talent_stage: Optional[int] = None
    character_awakening_phase: Optional[int] = None
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status: Optional[Status] = None
    character_display_awakening_status: Optional[bool] = None


class InboxReceiveResult(BaseModel):
    received_things: Optional[list[ReceivedThing]] = None
    has_not_receive_things: Optional[bool] = None


class InviteMultiRoomPayload(BaseModel):
    hashed_user_ids: Optional[list[str]] = None


class JoinMultiRoomPayload(BaseModel):
    hashed_room_id: Optional[str] = None
    password: Optional[str] = None


class LeaguePartyAndRankingResult(BaseModel):
    rank: Optional[int] = None
    user_id: Optional[str] = None
    best_score: Optional[int] = None
    league_master_id: Optional[int] = None
    class_type: Optional[LeagueClassTypes] = None
    user_name: Optional[str] = None
    acting_ability: Optional[int] = None
    slots: Optional[list[LeaguePartySlotResult]] = None
    difficulty: Optional[MusicDifficulties] = None


class LeaguePartySlotResult(BaseModel):
    slot_position: Optional[int] = None
    character_master_id: Optional[int] = None
    attribute: Optional[Attributes] = None
    character_rarity: Optional[CharacterRarities] = None
    character_level: Optional[int] = None
    poster_master_id: Optional[int] = None
    poster_rarity: Optional[PossessionRarities] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_rarity: Optional[PossessionRarities] = None
    accessory_level: Optional[int] = None
    current_status: Optional[Status] = None
    position: Optional[int] = None
    character_talent_stage: Optional[int] = None
    character_awakening_phase: Optional[int] = None
    character_display_awakening_status: Optional[bool] = None


class LeagueReceiveResults(BaseModel):
    class_reward_received_things: Optional[list[ReceivedThing]] = None
    class_reward_type: Optional[LeagueClassChangeTypes] = None
    first_achieve_received_things: Optional[list[ReceivedThing]] = None
    group_rank_received_things: Optional[list[ReceivedThing]] = None
    is_first_time_enrolled_class: Optional[bool] = None
    all_class_global_rank_received_things: Optional[list[ReceivedThing]] = None


class LeagueResult(BaseModel):
    before_group_ranking: Optional[int] = None
    after_group_ranking: Optional[int] = None
    lowest_up_border_score: Optional[int] = None
    lowest_keep_border_score: Optional[int] = None
    enrolled_group_number: Optional[int] = None
    is_in_counting: Optional[bool] = None


class LeagueTopMenuInformationResult(BaseModel):
    display_start_at: Optional[str] = None
    counting_start_at: Optional[str] = None
    display_end_at: Optional[str] = None
    music_master_id: Optional[int] = None
    league_group_ranking: Optional[int] = None
    up_class_border_score: Optional[int] = None
    up_class_border_ranking: Optional[int] = None
    keep_class_border_score: Optional[int] = None
    keep_class_border_ranking: Optional[int] = None
    group_lowest_rank: Optional[int] = None
    is_participated: Optional[bool] = None
    enrolled_group_number: Optional[int] = None


class LessonResult(BaseModel):
    character_base_master_id: Optional[int] = None
    star_point_result: Optional[StarPointResult] = None
    high_score_rewards: Optional[list[ReceivedThing]] = None
    high_score_before: Optional[int] = None
    high_score_after: Optional[int] = None


class LevelUpPhotoPayload(BaseModel):
    photo_id: Optional[int] = None
    after_level: Optional[int] = None


class LevelUpPhotoResult(BaseModel):
    photo_id: Optional[int] = None
    before_level: Optional[int] = None
    after_level: Optional[int] = None


class LiveDropThing(BaseModel):
    received_thing: Optional[ReceivedThing] = None
    order: Optional[int] = None
    live_drop_type: Optional[LiveDropTypes] = None
    is_fixed_drop: Optional[bool] = None


class LiveTimeEvent(BaseModel):
    timings: Optional[list[SenseTimingEvent]] = None
    cool_times: Optional[list[SenseCoolTime]] = None


class LiveUnit(BaseModel):
    actors: Optional[Dictionary] = None
    time_events: Optional[Dictionary] = None
    possible_senses: Optional[list[Sense]] = None
    start_effects: Optional[list[Effect]] = None
    star_act: Optional[StarAct] = None
    total_status: Optional[int] = None
    star_act_sense_light_count: Optional[int] = None
    max_principal: Optional[int] = None
    is_first_play_olivier: Optional[bool] = None
    base_score_percentage: Optional[int] = None
    base_score_difficulty_auto_coefficient: Optional[float] = None
    u_active_live_id: Optional[int] = None


class LiveUnitWithOrder(BaseModel):
    actors: Optional[Dictionary] = None
    time_events: Optional[Dictionary] = None
    possible_senses: Optional[list[Sense]] = None
    start_effects: Optional[list[Effect]] = None
    star_act: Optional[StarAct] = None
    total_status: Optional[int] = None
    star_act_sense_light_count: Optional[int] = None
    max_principal: Optional[int] = None
    is_first_play_olivier: Optional[bool] = None
    base_score_percentage: Optional[int] = None
    base_score_difficulty_auto_coefficient: Optional[float] = None
    u_active_live_id: Optional[int] = None
    order: Optional[int] = None


class LoginBonusDetail(BaseModel):
    thing_type: Optional[ThingTypes] = None
    thing_id: Optional[int] = None
    thing_quantity: Optional[int] = None
    login_count: Optional[int] = None


class LoginBonusResult(BaseModel):
    login_bonus_id: Optional[int] = None
    current_login_count: Optional[int] = None
    received_things: Optional[list[ReceivedThing]] = None
    title: Optional[str] = None
    type: Optional[LoginBonusTypes] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    message_template: Optional[str] = None
    background_image_path: Optional[str] = None
    cardboard_image_path: Optional[str] = None
    logo_image_path: Optional[str] = None
    total_days: Optional[int] = None
    is_loop: Optional[bool] = None
    order: Optional[int] = None
    details: Optional[list[LoginBonusDetail]] = None
    navigation_spine_id: Optional[str] = None
    voice_asset_id: Optional[str] = None
    head_motion_master_id: Optional[int] = None
    facial_expression_master_id: Optional[int] = None
    head_direction_master_id: Optional[int] = None
    body_motion_master_id: Optional[int] = None
    lip_sync_master_id: Optional[int] = None
    layout_type: Optional[LoginBonusLayoutTypes] = None
    comeback_campaign_master_id: Optional[int] = None
    login_bonus_spine_group: Optional[LoginBonusSpineGroup] = None


class LoginBonusSpineDetail(BaseModel):
    target_value1: Optional[int] = None
    target_value2: Optional[int] = None
    message_template: Optional[str] = None
    navigation_spine_id: Optional[str] = None
    voice_asset_id: Optional[str] = None
    head_motion_master_id: Optional[int] = None
    facial_expression_master_id: Optional[int] = None
    head_direction_master_id: Optional[int] = None
    body_motion_master_id: Optional[int] = None
    lip_sync_master_id: Optional[int] = None


class LoginBonusSpineGroup(BaseModel):
    spine_select_type: Optional[LoginBonusSpineSelectType] = None
    details: Optional[list[LoginBonusSpineDetail]] = None


class LoginPayload(BaseModel):
    push_notification_token: Optional[str] = None


class LoginResult(BaseModel):
    invalided_star_passes: Optional[list[StarPassTypes]] = None
    login_pass_notification: Optional[LoginPassNotificationTypes] = None
    is_approaching_login_pass_invalided: Optional[bool] = None
    invalided_item_master_ids: Optional[list[int]] = None
    approaching_item_master_ids: Optional[list[int]] = None
    story_event_point_exchange_result: Optional[list[StoryEventPointExchangeResult]] = (
        None
    )
    invalided_buff_item_master_ids: Optional[list[int]] = None


class MainCharacter(BaseModel):
    character_master_id: Optional[int] = None
    awakening_phase: Optional[int] = None
    talent_stage: Optional[int] = None
    level: Optional[int] = None
    display_awakening_status: Optional[bool] = None


class MarketResult(BaseModel):
    things: Optional[list[MarketThing]] = None
    required_jewel_for_refresh: Optional[int] = None


class MarketThing(BaseModel):
    frame_number: Optional[int] = None
    market_frame_thing_master_id: Optional[int] = None
    has_purchased: Optional[bool] = None
    discount_percent: Optional[int] = None


class MasterDataManifest(BaseModel):
    uri: Optional[str] = None
    sas_token: Optional[str] = None
    version: Optional[str] = None
    publish_timestamp: Optional[int] = None


class MatchingGhostLiveResult(BaseModel):
    ghost_live_master_id: Optional[int] = None
    ghost_user_profile: Optional[UserProfileDetail] = None
    ghost_live_info: Optional[GhostLiveInfo] = None


class MissionPassRewardsResult(BaseModel):
    mission_pass_rewards: Optional[list[ReceivedThing]] = None
    reward_result: Optional[MissionPassRewardStatus] = None


class MultiLiveAdditionalScoreBlock(BaseModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    time_event_second: Optional[int] = None
    combo: Optional[int] = None


class MultiLiveInformation(BaseModel):
    scores: Optional[Dictionary] = None


class MultiRoomCreateResult(BaseModel):
    hashed_multi_room_id: Optional[str] = None
    room_detail: Optional[MultiRoomDetailResult] = None


class MultiRoomDetailResult(BaseModel):
    multi_room_information_result: Optional[MultiRoomInformationResult] = None
    multi_room_rankings: Optional[list[MultiRoomRanking]] = None
    is_finished: Optional[bool] = None
    password: Optional[str] = None


class MultiRoomInformationResult(BaseModel):
    hashed_multi_room_id: Optional[str] = None
    room_name: Optional[str] = None
    play_mode: Optional[MultiRoomPlayModes] = None
    joined_member_count: Optional[int] = None
    can_join_max_member: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    live_master_id1: Optional[int] = None
    live_master_id2: Optional[int] = None
    live_master_id3: Optional[int] = None
    has_password: Optional[bool] = None


class MultiRoomInvitedResult(BaseModel):
    owner_user_name: Optional[str] = None
    multi_room_information_result: Optional[MultiRoomInformationResult] = None


class MultiRoomJoinnedResult(BaseModel):
    my_rank: Optional[int] = None
    my_score: Optional[int] = None
    my_total_achievement_rate_percent_record: Optional[Decimal] = None
    multi_room_information_result: Optional[MultiRoomInformationResult] = None


class MultiRoomPartySlot(BaseModel):
    position: Optional[int] = None
    character_master_id: Optional[int] = None
    character_level: Optional[int] = None
    character_talent_stage: Optional[int] = None
    character_awakening_phase: Optional[int] = None
    character_display_awakening_status: Optional[bool] = None
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    u_accessory_id: Optional[int] = None
    current_status: Optional[Status] = None


class MultiRoomRanking(BaseModel):
    user_id: Optional[str] = None
    rank: Optional[int] = None
    is_owner: Optional[bool] = None
    score: Optional[int] = None
    total_achievement_rate_percent_record: Optional[Decimal] = None
    best_record_challenge_count: Optional[int] = None
    best_record_date: Optional[str] = None
    user_profile: Optional[UserProfile] = None
    party_info: Optional[PartyInfo] = None
    note_result: Optional[NoteResult] = None


class MusicCourseRandomSelectResult(BaseModel):
    details: Optional[list[MusicCourseRandomSelectResultDetail]] = None


class MusicCourseRandomSelectResultDetail(BaseModel):
    set_list_number: Optional[int] = None
    live_master_id: Optional[int] = None


class MusicCourseRankingPayload(BaseModel):
    user_id: Optional[int] = None
    current_challenge_count: Optional[int] = None
    perfect_star: Optional[int] = None
    perfect: Optional[int] = None
    great: Optional[int] = None
    good: Optional[int] = None
    bad: Optional[int] = None
    miss: Optional[int] = None
    total_achievement_rate_percent_record: Optional[Decimal] = None
    best_record_challenge_count: Optional[int] = None
    best_record_date: Optional[str] = None


class MyCircleInformationResult(BaseModel):
    u_circle_hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: Optional[PlayTimeTypes] = None
    play_time_end_type: Optional[PlayTimeTypes] = None
    entry_type: Optional[EntryTypes] = None
    member_count: Optional[int] = None
    my_authority: Optional[CircleAuthorities] = None
    result_status: Optional[CircleResultStatus] = None
    circle_banner: Optional[CircleBanner] = None
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    support_company_information: Optional[SupportCompanyInformation] = None
    support_company: Optional[Companies] = None
    daily_added_support_point: Optional[int] = None
    is_publish_ranking: Optional[bool] = None
    stamina_last_received_at: Optional[str] = None
    circle_authority_update_type: Optional[CircleAuthorityUpdateTypes] = None


class NoteJudgePayload(BaseModel):
    timing: Optional[TimingTypes] = None
    count: Optional[int] = None


class NoteResult(BaseModel):
    perfect_star: Optional[int] = None
    perfect: Optional[int] = None
    great: Optional[int] = None
    good: Optional[int] = None
    bad: Optional[int] = None
    miss: Optional[int] = None


class NotificationContentResult(BaseModel):
    id_: Optional[int] = None
    body: Optional[str] = None
    title: Optional[str] = None
    posting_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    notification_tab_category: Optional[NotificationTabCategory] = None
    notification_category: Optional[NotificationCategory] = None
    banner_path: Optional[str] = None


class NotificationResult(BaseModel):
    id_: Optional[int] = None
    banner_path: Optional[str] = None
    title: Optional[str] = None
    posting_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    notification_tab_category: Optional[NotificationTabCategory] = None
    notification_category: Optional[NotificationCategory] = None
    is_confirmation: Optional[bool] = None
    order: Optional[int] = None


class PartyInfo(BaseModel):
    leader_position: Optional[int] = None
    multi_room_party_slots: Optional[list[MultiRoomPartySlot]] = None


class PartyPayload(BaseModel):
    leader_position: Optional[int] = None
    party_slot_payload: Optional[list[PartySlotPayload]] = None


class PartySlotAccessoryPayload(BaseModel):
    m_accessory_id: Optional[int] = None
    level: Optional[int] = None
    m_accessory_effect_id1: Optional[int] = None
    m_accessory_effect_id2: Optional[int] = None
    m_accessory_effect_id3: Optional[int] = None


class PartySlotCharacterPayload(BaseModel):
    m_character_id: Optional[int] = None
    talent_stage: Optional[int] = None
    awakening_phase: Optional[int] = None
    level: Optional[int] = None
    sense_level: Optional[int] = None
    current_experience: Optional[int] = None
    released_episode_order: Optional[CharacterEpisodeOrder] = None
    read_episode_order: Optional[CharacterEpisodeOrder] = None
    display_awakening_status: Optional[bool] = None


class PartySlotDetail(BaseModel):
    position: Optional[int] = None
    character_master_id: Optional[int] = None
    character_level: Optional[int] = None
    character_talent_stage: Optional[int] = None
    character_awakening_phase: Optional[int] = None
    character_display_awakening_status: Optional[bool] = None
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status_vocal: Optional[int] = None
    current_status_expression: Optional[int] = None
    current_status_concentration: Optional[int] = None
    u_accessory_id: Optional[int] = None


class PartySlotPayload(BaseModel):
    position: Optional[int] = None
    party_slot_character_payload: Optional[PartySlotCharacterPayload] = None
    party_slot_poster_payload: Optional[PartySlotPosterPayload] = None
    party_slot_accessory_payload: Optional[PartySlotAccessoryPayload] = None


class PartySlotPosterPayload(BaseModel):
    m_poster_id: Optional[int] = None
    level: Optional[int] = None
    phase: Optional[int] = None
    released_episode: Optional[PosterEpisodeTypes] = None


class PhotoAppearedCharacter(BaseModel):
    character_base_master_id: Optional[int] = None
    is_main_character: Optional[bool] = None


class PlayerRankPointResult(BaseModel):
    rank_before: Optional[int] = None
    rank_after: Optional[int] = None
    rank_point_before: Optional[int] = None
    rank_point_after: Optional[int] = None
    rank_point_acquired: Optional[int] = None
    stamina_before: Optional[int] = None


class PosterAlternativeImagePayload(BaseModel):
    poster_id: Optional[int] = None
    pattern: Optional[int] = None


class PosterFavoritePayload(BaseModel):
    poster_id: Optional[int] = None
    set_favorite: Optional[bool] = None


class PosterLineupResult(BaseModel):
    normal_probabilities: Optional[list[PosterRarityProbability]] = None
    fixed_probabilities: Optional[list[PosterRarityProbability]] = None
    normal_lineup_items: Optional[list[GachaLineupItemProbability]] = None
    fixed_lineup_items: Optional[list[GachaLineupItemProbability]] = None


class PosterRarityProbability(BaseModel):
    rarity: Optional[PossessionRarities] = None
    probability: Optional[float] = None


class ProcessPaymentResult(BaseModel):
    result: Optional[ProcessPaymentTransactionResult] = None


class PurchaseItemPayload(BaseModel):
    m_jewel_shop_item_id: Optional[int] = None


class RateResult(BaseModel):
    achievement_rate_result: Optional[RateUpdateResult] = None
    live_rate_result: Optional[RateUpdateResult] = None
    total_rate_before: Optional[float] = None
    total_rate_after: Optional[float] = None


class RateUpdateResult(BaseModel):
    best_ever: Optional[float] = None
    this_time: Optional[float] = None


class RawHighScoreRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRankingWithLongPoint]] = None
    high_score_parties: Optional[list[HighScoreParty]] = None
    high_score_buffs: Optional[list[HighScoreBuff]] = None
    user_profiles: Optional[list[UserProfile]] = None


class RawRanking(BaseModel):
    rank: Optional[int] = None
    point: Optional[int] = None
    user_id: Optional[str] = None
    group_value: Optional[int] = None


class RawRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRanking]] = None
    user_profiles: Optional[list[UserProfile]] = None


class RawRankingWithLongPoint(BaseModel):
    rank: Optional[int] = None
    point: Optional[int] = None
    user_id: Optional[str] = None


class ReadNotificationPayload(BaseModel):
    tab_category: Optional[NotificationTabCategory] = None
    read_at: Optional[str] = None


class ReceivedThing(BaseModel):
    type: Optional[ThingTypes] = None
    id_: Optional[int] = None
    quantity: Optional[int] = None
    original_type: Optional[ThingTypes] = None
    original_id: Optional[int] = None
    after_phase: Optional[int] = None
    sent_inbox: Optional[bool] = None


class RegisterAppStorePaymentPayload(BaseModel):
    receipt_base64: Optional[str] = None


class RegisterBirthDayPayload(BaseModel):
    birth_date: Optional[str] = None


class RegisterGooglePlayPaymentPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    json_: Optional[str] = Field(default=None, alias="json")


class RegisterPayload(BaseModel):
    name: Optional[str] = None


class RegisterTakeOverPasswordPayload(BaseModel):
    password: Optional[str] = None


class RollResult(BaseModel):
    roll_order: Optional[int] = None
    selected_slot: Optional[int] = None
    roulette_prize_master_id: Optional[int] = None


class RouletteRollResult(BaseModel):
    roll_results: Optional[list[RollResult]] = None


class ScoreWithDateResult(BaseModel):
    score: Optional[int] = None
    date: Optional[str] = None


class SelectMusicCourseRandomMusicPayload(BaseModel):
    music_course_master_id: Optional[int] = None
    music_course_gauge_type: Optional[MusicCourseGaugeType] = None


class SellAccessoryPayload(BaseModel):
    u_accessory_ids: Optional[list[int]] = None


class Sense(BaseModel):
    id_: Optional[int] = None
    actor_id: Optional[int] = None
    cool_time: Optional[int] = None
    sense_type: Optional[SenseTypes] = None
    acquirable_lights: Optional[list[SenseLightTypes]] = None
    pre_sense_effect: Optional[list[Effect]] = None
    sense_effect: Optional[SenseEffect] = None
    poster_effect: Optional[list[Effect]] = None
    accessory_effect: Optional[list[Effect]] = None
    combination_sense_id: Optional[list[int]] = None
    sense_master_id: Optional[int] = None
    original_actor_id: Optional[int] = None


class SenseCoolTime(BaseModel):
    position: Optional[int] = None
    cool_time: Optional[int] = None


class SenseEffect(BaseModel):
    score_factor: Optional[int] = None
    principal: Optional[int] = None
    branch_condition: Optional[BranchConditionTypes] = None
    effect_branches: Optional[list[EffectBranch]] = None


class SenseScoreBlock(BaseModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    time_event_second: Optional[int] = None
    sense_id: Optional[int] = None
    combo: Optional[int] = None


class SenseTimingEvent(BaseModel):
    timing_seconds: Optional[int] = None
    position: Optional[int] = None
    event: Optional[TimingEvent] = None


class SetAlbumPublishingPayload(BaseModel):
    publishing: Optional[bool] = None
    publish_page_number: Optional[int] = None


class SetLessonPartyPayload(BaseModel):
    slots: Optional[list[SetLessonPartySlotPayload]] = None


class SetLessonPartySlotPayload(BaseModel):
    order: Optional[int] = None
    character_id: Optional[int] = None


class SetPhotoTagPayload(BaseModel):
    photo_id: Optional[int] = None
    character_base_ids: Optional[list[int]] = None


class SetSelectedThingsPayload(BaseModel):
    gacha_thing_ids: Optional[list[int]] = None


class SpRateUpdateResult(BaseModel):
    best_ever: Optional[int] = None
    this_time: Optional[int] = None
    best_ever_total: Optional[int] = None
    this_time_total: Optional[int] = None


class StarAct(BaseModel):
    score_factor: Optional[int] = None
    actor_id: Optional[int] = None
    branch_condition: Optional[BranchConditionTypes] = None
    effect_branches: Optional[list[EffectBranch]] = None


class StarActScoreBlock(BaseModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    time_event_second: Optional[int] = None
    combo: Optional[int] = None


class StarPointResult(BaseModel):
    rank_before: Optional[int] = None
    rank_after: Optional[int] = None
    star_point_before: Optional[int] = None
    star_point_after: Optional[int] = None
    star_point_acquired: Optional[int] = None
    received_reward: Optional[list[ReceivedThing]] = None


class StartLessonPayload(BaseModel):
    character_base_master_id: Optional[int] = None
    live_master_id: Optional[int] = None


class StartLivePayload(BaseModel):
    party_id: Optional[int] = None
    live_master_id: Optional[int] = None
    audition_master_id: Optional[int] = None
    league_master_id: Optional[int] = None
    use_stamina: Optional[bool] = None
    stamina_consumption_ratio: Optional[int] = None
    live_setting_master_id: Optional[int] = None
    is_auto_play: Optional[bool] = None
    is_story_event_challenge: Optional[bool] = None
    concert_stage_master_id: Optional[int] = None
    bonus_live_stage_master_id: Optional[int] = None
    music_course_detail_master_id: Optional[int] = None
    music_course_gauge_type: Optional[MusicCourseGaugeType] = None
    ghost_live_master_id: Optional[int] = None
    trial_party_event_stage_master_id: Optional[int] = None


class StartMultiLivePayload(BaseModel):
    live_master_id: Optional[int] = None
    multi_live_id: Optional[int] = None
    use_stamina: Optional[bool] = None
    stamina_consumption_ratio: Optional[int] = None
    party_id: Optional[int] = None


class StartMultiRoomLivePayload(BaseModel):
    hashed_multi_room_id: Optional[str] = None
    live_master_id: Optional[int] = None
    party_id: Optional[int] = None


class StartTournamentPayload(BaseModel):
    tournament_detail_master_id: Optional[int] = None
    party_id: Optional[int] = None
    stamina_consumption_ratio: Optional[int] = None


class StartTripleCastLivePayload(BaseModel):
    m_live_id: Optional[int] = None
    m_triple_cast_id: Optional[int] = None


class StartTripleCastLiveResult(BaseModel):
    live_units: Optional[list[LiveUnitWithOrder]] = None


class Status(BaseModel):
    concentration: Optional[int] = None
    expression: Optional[int] = None
    vocal: Optional[int] = None
    total_status: Optional[int] = None


class StoryEventCampInfo(BaseModel):
    raw_ranking: Optional[RawRanking] = None
    camp1_total_point: Optional[int] = None
    camp2_total_point: Optional[int] = None


class StoryEventMissionCircleProgress(BaseModel):
    story_event_circle_mission_master_id: Optional[int] = None
    current_count: Optional[int] = None


class StoryEventMissionCircleProgressResult(BaseModel):
    is_success: Optional[bool] = None
    progresses: Optional[list[StoryEventMissionCircleProgress]] = None


class StoryEventPointExchangeResult(BaseModel):
    story_event_master_id: Optional[int] = None
    before_story_event_point_amount: Optional[int] = None
    after_coin_amount: Optional[int] = None


class SupportCompanyInformation(BaseModel):
    sirius: Optional[SupportCompanyLevelStatus] = None
    eden: Optional[SupportCompanyLevelStatus] = None
    gingaza: Optional[SupportCompanyLevelStatus] = None
    denki: Optional[SupportCompanyLevelStatus] = None


class SupportCompanyLevelLimitDetail(BaseModel):
    order: Optional[int] = None
    quantity: Optional[int] = None


class SupportCompanyLevelLimitPayload(BaseModel):
    company: Optional[Companies] = None
    coin_quantity: Optional[int] = None
    details: Optional[list[SupportCompanyLevelLimitDetail]] = None


class SupportCompanyLevelLimitStatus(BaseModel):
    current_coin_quantity: Optional[int] = None
    details: Optional[list[SupportCompanyLevelLimitStatusDetail]] = None


class SupportCompanyLevelLimitStatusDetail(BaseModel):
    order: Optional[int] = None
    current_quantity: Optional[int] = None


class SupportCompanyLevelStatus(BaseModel):
    level: Optional[int] = None
    current_support_point: Optional[int] = None
    last_level_upped_at: Optional[str] = None
    level_limit: Optional[int] = None
    level_limit_status: Optional[SupportCompanyLevelLimitStatus] = None


class TakeOverAccountPayload(BaseModel):
    linkage_code: Optional[str] = None
    password: Optional[str] = None


class TakeOverAccountResult(BaseModel):
    is_success: Optional[bool] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    rank: Optional[int] = None
    login_token: Optional[str] = None


class TakeOverCodeResult(BaseModel):
    is_success: Optional[bool] = None
    linkage_code: Optional[str] = None


class TimedConfirmationCode(BaseModel):
    confirmation_code: Optional[str] = None
    remaining_seconds: Optional[int] = None


class TimingEvent(BaseModel):
    total_sense_lights: Optional[list[SenseLightTypes]] = None
    grant_sense_lights: Optional[list[SenseLightTypes]] = None
    is_star_act: Optional[bool] = None
    lost_lights: Optional[bool] = None
    acquirable_lights: Optional[list[SenseLightTypes]] = None
    sense_ids: Optional[list[int]] = None
    sense_voice_ids: Optional[list[int]] = None
    sense_master_id: Optional[int] = None


class TotalPointEventInformationResult(BaseModel):
    current_total_point: Optional[int] = None


class TotalPointEventRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRankingWithLongPoint]] = None
    user_profiles: Optional[list[UserProfile]] = None


class TournamentQualifyingInformationResult(BaseModel):
    entry_code: Optional[str] = None


class TournamentResult(BaseModel):
    best_ever_unique_score: Optional[int] = None
    this_time_unique_score: Optional[int] = None
    tournament_detail_master_id: Optional[int] = None


class TransitionTokenResult(BaseModel):
    token: Optional[str] = None


class TrialPartyEventResult(BaseModel):
    rewards: Optional[list[ReceivedThing]] = None


class TrialPartyEventStageResult(BaseModel):
    principal_gauge_value: Optional[int] = None


class TripleCastPartyAndRankingResult(BaseModel):
    rank: Optional[int] = None
    user_id: Optional[str] = None
    best_score: Optional[int] = None
    triple_cast_master_id: Optional[int] = None
    class_type: Optional[LeagueClassTypes] = None
    difficulty: Optional[MusicDifficulties] = None
    user_name: Optional[str] = None
    parties: Optional[list[TripleCastPartyResult]] = None


class TripleCastPartyResult(BaseModel):
    order: Optional[int] = None
    score: Optional[int] = None
    slots: Optional[list[LeaguePartySlotResult]] = None


class TripleCastPartyScore(BaseModel):
    order: Optional[int] = None
    score: Optional[int] = None


class UpdateClearLampResult(BaseModel):
    clear_lamp: Optional[ClearLamps] = None


class UpdateGameHintPayload(BaseModel):
    categories: Optional[list[PageCategories]] = None


class UpdateHomeDisplayPreferencePayload(BaseModel):
    home_character_base_master_id: Optional[int] = None
    member_character_base_master_id: Optional[int] = None
    story_character_base_master_id: Optional[int] = None
    shop_character_base_master_id: Optional[int] = None
    home_costume_master_id: Optional[int] = None
    member_costume_master_id: Optional[int] = None
    story_costume_master_id: Optional[int] = None
    shop_costume_master_id: Optional[int] = None
    illust_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    home_character_display_type: Optional[HomeCharacterDisplayTypes] = None
    login_bonus_character_base_master_id: Optional[int] = None
    login_bonus_spine_costume_master_id: Optional[int] = None


class UpdateLastViewedAtPayload(BaseModel):
    viewed_shop_category_types: Optional[ViewedShopCategoryTypes] = None
    exchange_shop_master_id: Optional[int] = None


class UpdateTutorialPayload(BaseModel):
    tutorial_status: Optional[TutorialStatus] = None


class UrlResult(BaseModel):
    url: Optional[str] = None


class UseExperienceItemsPayload(BaseModel):
    item_master_id: Optional[int] = None
    quantity: Optional[int] = None


class UseStaminaRecoveryItem(BaseModel):
    item_master_id: Optional[int] = None
    quantity: Optional[int] = None


class UseStaminaRecoveryItemsPayload(BaseModel):
    items: Optional[list[UseStaminaRecoveryItem]] = None


class User(BaseModel):
    id_: Optional[int] = None
    player_rank: Optional[int] = None
    current_rank_point: Optional[int] = None
    current_stamina: Optional[int] = None
    max_stamina_restored_at: Optional[str] = None
    paid_jewel: Optional[int] = None
    free_jewel: Optional[int] = None
    coin: Optional[int] = None
    player_rank_limit: Optional[int] = None
    stamina_recover_times_with_jewel: Optional[int] = None
    circle_usage_restrictions_end_time: Optional[str] = None
    circle_id: Optional[str] = None
    game_start_at: Optional[str] = None
    hash_user_id: Optional[str] = None
    ban_level: Optional[BanLevels] = None
    tutorial_status: Optional[TutorialStatus] = None
    monthly_payment: Optional[int] = None
    splash_last_displayed_at: Optional[str] = None
    is_caped_player_rank: Optional[bool] = None
    require_caped_player_rank_announce: Optional[bool] = None


class UserProfile(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_m_character_id: Optional[int] = None
    main_character_level: Optional[int] = None
    character_display_awakening_status: Optional[bool] = None
    icon_frame_master_id: Optional[int] = None


class UserProfileDetail(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_m_character_id: Optional[int] = None
    main_character_level: Optional[int] = None
    character_display_awakening_status: Optional[bool] = None
    icon_frame_master_id: Optional[int] = None
    name_color_master_id: Optional[int] = None
    name_base_color_master_id: Optional[int] = None
    nameplate_master_id: Optional[int] = None
    nameplate_detail_master_id: Optional[int] = None


class UserResult(BaseModel):
    user: Optional[User] = None


class ViewShopResult(BaseModel):
    converted_things: Optional[list[ConvertedThingResult]] = None


__all__ = [
    "AbilityVarietyUpPayload",
    "AccessoryAutoSellConvertThing",
    "AccessoryFavoritePayload",
    "AccountConnectPayload",
    "AccountDeletionResult",
    "AccountRegistResult",
    "AcquirableThing",
    "AcquirableThingsPayload",
    "ActorPortalCharacterPayload",
    "AlbumArrangingPayload",
    "AlbumPageResult",
    "AlbumPageSearchResult",
    "AlbumPhotoPayload",
    "AuditionClearParty",
    "AuditionClearPartySlot",
    "AuditionClearedInformationParties",
    "AuditionClearedInformationResult",
    "AuthenticatePayload",
    "AuthenticateResult",
    "BannerPayload",
    "BaseScoreBlock",
    "BlockListResult",
    "BonusLiveResult",
    "BooleanResult",
    "BulkLevelUpPayload",
    "BulkReceivePayload",
    "CalculateLessonTimeEventPayload",
    "CalculateTimeEventPayload",
    "ChangeNamePayload",
    "ChangePhotoAbilityPayload",
    "CharacterBaseStarPointResult",
    "CharacterFavoritePayload",
    "CharacterLineupResult",
    "CharacterPointEventInformationResult",
    "CharacterPointEventRankingResult",
    "CharacterRank",
    "CharacterRarityProbability",
    "ChatworkSendMessagePayload",
    "CircleAuthorityChangePayload",
    "CircleAuthorityResult",
    "CircleBanner",
    "CircleEventCircleMissionProgress",
    "CircleEventInformationResult",
    "CircleEventRanking",
    "CircleInformationResult",
    "CircleInviteResult",
    "CircleMemberInfoParameters",
    "CircleMemberInfoResult",
    "CircleMemberParameters",
    "CirclePayload",
    "CircleProfile",
    "CircleRawRanking",
    "CircleResult",
    "CircleSearchIdResult",
    "CircleSearchResult",
    "ConcertResult",
    "ConcoursDetailInformationResult",
    "ConcoursInfomationResult",
    "ConvertedThingResult",
    "CostumeFavoritePayload",
    "CourseRankingResult",
    "CourseResult",
    "CreateCircleResult",
    "CreateMultiRoomPayload",
    "DebugAlbumSimpleArrangingPayload",
    "DebugEditLeagueBasicPayload",
    "DebugLinkageCodeResult",
    "DebugModifyCharacterEnhanceInformationPayload",
    "DebugModifyPosterEnhanceInformationPayload",
    "DebugPrepareLeagueGroupUserPayload",
    "DebugUserIdResult",
    "Decimal",
    "Dictionary",
    "DonateSupportCompanyResult",
    "DonateSupportLevelLimitDetail",
    "DonateSupportLevelLimitPayload",
    "EditBookmarkPayload",
    "EditPartyPayload",
    "EditPartySlotPayload",
    "EditPositionPayload",
    "EditPositionSlotPayload",
    "EditTrialPartyEventStagePartyPayload",
    "EditTrialPartyEventStagePartyPayloadSlot",
    "EditUserProfilePayload",
    "EexternalPaymentResult",
    "Effect",
    "EffectBranch",
    "EffectTargetValue",
    "EffectTrigger",
    "EnvironmentResult",
    "EpisodeResult",
    "EventBoxGachaRollResult",
    "EventResult",
    "ExchangeShopThingPayload",
    "FavoriteStampOrderPayload",
    "FinishAnotherNotationLivePayload",
    "FinishLessonPayload",
    "FinishLivePayload",
    "FinishLiveResult",
    "FlashSaleReadStagePayload",
    "FriendAcceptResult",
    "FriendFavoritePayload",
    "FriendInvitationMissionPayload",
    "FriendInvitationUserInfoResult",
    "FriendListResult",
    "FriendRequestResult",
    "FriendResult",
    "FriendSearchResult",
    "GachaHistoryResult",
    "GachaInfoResult",
    "GachaLineupItemProbability",
    "GachaRollLimit",
    "GachaRollResult",
    "GachaSelectedThingsResult",
    "GachaThingResult",
    "GenerateLotteryResultPayload",
    "GeneratePhotoPayload",
    "GeneratePhotoResult",
    "GeneratePhotosPayload",
    "GhostLiveInfo",
    "GhostLiveResult",
    "HighScoreBuff",
    "HighScoreBuffSetting",
    "HighScoreParty",
    "HighScorePartySlot",
    "InboxReceiveResult",
    "InviteMultiRoomPayload",
    "JoinMultiRoomPayload",
    "LeaguePartyAndRankingResult",
    "LeaguePartySlotResult",
    "LeagueReceiveResults",
    "LeagueResult",
    "LeagueTopMenuInformationResult",
    "LessonResult",
    "LevelUpPhotoPayload",
    "LevelUpPhotoResult",
    "LiveDropThing",
    "LiveTimeEvent",
    "LiveUnit",
    "LiveUnitWithOrder",
    "LoginBonusDetail",
    "LoginBonusResult",
    "LoginBonusSpineDetail",
    "LoginBonusSpineGroup",
    "LoginPayload",
    "LoginResult",
    "MainCharacter",
    "MarketResult",
    "MarketThing",
    "MasterDataManifest",
    "MatchingGhostLiveResult",
    "MissionPassRewardsResult",
    "MultiLiveAdditionalScoreBlock",
    "MultiLiveInformation",
    "MultiRoomCreateResult",
    "MultiRoomDetailResult",
    "MultiRoomInformationResult",
    "MultiRoomInvitedResult",
    "MultiRoomJoinnedResult",
    "MultiRoomPartySlot",
    "MultiRoomRanking",
    "MusicCourseRandomSelectResult",
    "MusicCourseRandomSelectResultDetail",
    "MusicCourseRankingPayload",
    "MyCircleInformationResult",
    "NoteJudgePayload",
    "NoteResult",
    "NotificationContentResult",
    "NotificationResult",
    "PartyInfo",
    "PartyPayload",
    "PartySlotAccessoryPayload",
    "PartySlotCharacterPayload",
    "PartySlotDetail",
    "PartySlotPayload",
    "PartySlotPosterPayload",
    "PhotoAppearedCharacter",
    "PlayerRankPointResult",
    "PosterAlternativeImagePayload",
    "PosterFavoritePayload",
    "PosterLineupResult",
    "PosterRarityProbability",
    "ProcessPaymentResult",
    "PurchaseItemPayload",
    "RateResult",
    "RateUpdateResult",
    "RawHighScoreRankingResult",
    "RawRanking",
    "RawRankingResult",
    "RawRankingWithLongPoint",
    "ReadNotificationPayload",
    "ReceivedThing",
    "RegisterAppStorePaymentPayload",
    "RegisterBirthDayPayload",
    "RegisterGooglePlayPaymentPayload",
    "RegisterPayload",
    "RegisterTakeOverPasswordPayload",
    "RollResult",
    "RouletteRollResult",
    "ScoreWithDateResult",
    "SelectMusicCourseRandomMusicPayload",
    "SellAccessoryPayload",
    "Sense",
    "SenseCoolTime",
    "SenseEffect",
    "SenseScoreBlock",
    "SenseTimingEvent",
    "SetAlbumPublishingPayload",
    "SetLessonPartyPayload",
    "SetLessonPartySlotPayload",
    "SetPhotoTagPayload",
    "SetSelectedThingsPayload",
    "SpRateUpdateResult",
    "StarAct",
    "StarActScoreBlock",
    "StarPointResult",
    "StartLessonPayload",
    "StartLivePayload",
    "StartMultiLivePayload",
    "StartMultiRoomLivePayload",
    "StartTournamentPayload",
    "StartTripleCastLivePayload",
    "StartTripleCastLiveResult",
    "Status",
    "StoryEventCampInfo",
    "StoryEventMissionCircleProgress",
    "StoryEventMissionCircleProgressResult",
    "StoryEventPointExchangeResult",
    "SupportCompanyInformation",
    "SupportCompanyLevelLimitDetail",
    "SupportCompanyLevelLimitPayload",
    "SupportCompanyLevelLimitStatus",
    "SupportCompanyLevelLimitStatusDetail",
    "SupportCompanyLevelStatus",
    "TakeOverAccountPayload",
    "TakeOverAccountResult",
    "TakeOverCodeResult",
    "TimedConfirmationCode",
    "TimingEvent",
    "TotalPointEventInformationResult",
    "TotalPointEventRankingResult",
    "TournamentQualifyingInformationResult",
    "TournamentResult",
    "TransitionTokenResult",
    "TrialPartyEventResult",
    "TrialPartyEventStageResult",
    "TripleCastPartyAndRankingResult",
    "TripleCastPartyResult",
    "TripleCastPartyScore",
    "UpdateClearLampResult",
    "UpdateGameHintPayload",
    "UpdateHomeDisplayPreferencePayload",
    "UpdateLastViewedAtPayload",
    "UpdateTutorialPayload",
    "UrlResult",
    "UseExperienceItemsPayload",
    "UseStaminaRecoveryItem",
    "UseStaminaRecoveryItemsPayload",
    "User",
    "UserProfile",
    "UserProfileDetail",
    "UserResult",
    "ViewShopResult",
]

for _m in __all__:
    globals()[_m].model_rebuild()
