from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from .enums import *

from models.master_data import Status
from models.master_data import *  # master types live in models/master_data/


class AbilityVarietyUpPayload(BaseModel):
    photo_id: int = 0
    variety_to: int = 0
    item_master_id: int = 0


class AcceptFriendRequest(BaseModel):
    request_user_id: Optional[str] = None
    received_user_id: Optional[str] = None
    received_user_name: Optional[str] = None


class Accessory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    accessory_master_id: int = 0
    level: int = 0
    locked: bool = False
    accessory_effects: Optional[list[int]] = None
    reference_counting: int = 0
    is_favorite: bool = False


class AccessoryAutoSell(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    auto_sell_rarity: PossessionRarityFlag = PossessionRarityFlag.None_


class AccessoryAutoSellConvertThing(BaseModel):
    accessory_master_id: int = 0
    convert_thing: Optional[ReceivedThing] = None


class AccessoryFavoritePayload(BaseModel):
    accessory_id: int = 0
    set_favorite: bool = False


class AccountConnectPayload(BaseModel):
    provider: AuthenticationProviders = AuthenticationProviders.Google
    token: Optional[str] = None


class AccountDeletionResult(BaseModel):
    is_success: bool = False
    error: Optional[AccountDeletionErrorTypes] = None


class AccountRegistResult(BaseModel):
    token: Optional[str] = None
    error_type: AccountRegisterErrorTypes = AccountRegisterErrorTypes.None_


class AcquirableThing(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    quantity: int = 0


class AcquirableThingsPayload(BaseModel):
    things: Optional[list[AcquirableThing]] = None


class ActorPortalCharacterPayload(BaseModel):
    character_base_id: int = 0
    character_id: int = 0
    is_awakening: bool = False


class Album(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    level: int = 0
    publish_page_number: int = 0
    current_preset_order: int = 0


class AlbumArrangingPayload(BaseModel):
    publishing: bool = False
    page: int = 0
    items: Optional[list[int]] = None
    m_album_theme_id: Optional[int] = None


class AlbumPage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    page: int = 0
    edit_type: EditTypes = EditTypes.SimpleEdit
    publishing: bool = False
    items: Optional[list[int]] = None
    album_theme_master_id: Optional[int] = None


class AlbumPageResult(BaseModel):
    album_page_id: int = 0
    album_id: int = 0
    level: int = 0
    page: int = 0
    edit_type: EditTypes = EditTypes.SimpleEdit
    publishing: bool = False
    items: Optional[list[int]] = None
    album_theme_master_id: Optional[int] = None


class AlbumPageSearchResult(BaseModel):
    album_page_result: Optional[AlbumPageResult] = None
    is_success: bool = False


class AlbumPhotoPayload(BaseModel):
    photo_id: int = 0
    order: int = 0


class AlbumPreset(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    order: int = 0


class AlbumTheme(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    album_theme_master_id: int = 0


class AnotherNotation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    another_notation_master_id: int = 0
    clear_lamp: ClearLamps = ClearLamps.None_
    rate_grade: AchievementRateGrades = AchievementRateGrades.None_
    achievement_rate_percent_record: Optional[str] = None


class AuditionClear(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    audition_master_id: int = 0
    clear_phase: int = 0
    audition_clear_party_id: int = 0
    user_id: Optional[str] = None
    skip_clear_phase: int = 0


class AuditionClearParty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    score: int = 0
    difficulty: MusicDifficulties = MusicDifficulties.None_
    slots: Optional[list[AuditionClearPartySlot]] = None
    user_name: Optional[str] = None
    rate_grade: AchievementRateGrades = AchievementRateGrades.None_
    player_rank: Optional[str] = None
    leader_position: int = 0


class AuditionClearPartySlot(BaseModel):
    position: int = 0
    character_master_id: int = 0
    character_level: int = 0
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    star_rank: int = 0
    talent_stage: int = 0
    awakening_phase: int = 0
    current_status: Optional[Status] = None
    character_display_awakening_status: bool = False


class AuditionClearedInformationParties(BaseModel):
    parties: Optional[list[AuditionClearParty]] = None
    cleared_phase: int = 0


class AuditionClearedInformationResult(BaseModel):
    parties_phases: Optional[list[AuditionClearedInformationParties]] = None


class AuthenticatePayload(BaseModel):
    login_token: Optional[str] = None
    game_version: GameVersions = GameVersions.Unknown
    apk_hash: Optional[str] = None
    apk_application_signature: Optional[str] = None
    application_version: Optional[str] = None


class AuthenticateResult(BaseModel):
    token: Optional[str] = None
    ban_level: BanLevels = BanLevels.Normal
    warned_until: Optional[str] = None


class BannerPayload(BaseModel):
    circle_hashed_id: Optional[str] = None
    poster_master_id: int = 0
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0
    rotation_angle: int = 0
    display_poster_string: bool = False
    banner_ratio: float = 0.0


class BaseScoreBlock(BaseModel):
    hash: int = 0
    score: int = 0
    life: int = 0
    note_id: int = 0
    timing_type: TimingTypes = TimingTypes.None_
    combo: int = 0


class Behaviour(BaseModel):
    pass


class BlockListResult(BaseModel):
    results: Optional[list[FriendResult]] = None


class Bomb(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    bomb_master_ids: Optional[list[int]] = None


class BonusLive(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    bonus_live_master_id: int = 0
    cleared_stage_order: int = 0
    read_tips: bool = False
    daily_clear_times: int = 0


class BonusLiveResult(BaseModel):
    rewards: Optional[list[ReceivedThing]] = None


class BonusLiveStage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    bonus_live_master_stage_id: int = 0
    clear_times: int = 0


class BooleanResult(BaseModel):
    is_success: bool = False


class BuffItemStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    effect_type: CampaignEffectTypes = CampaignEffectTypes.LiveReward
    buff_item_master_id: int = 0
    valid_until: str = ""


class BulkLevelUpPayload(BaseModel):
    character_id: int = 0
    order: int = 0


class BulkReceivePayload(BaseModel):
    inbox_ids: Optional[list[int]] = None


class CalculateLessonTimeEventPayload(BaseModel):
    music_master_id: int = 0
    character_base_master_id: int = 0


class CalculateTimeEventPayload(BaseModel):
    music_master_id: int = 0
    sense_notation_master_id: Optional[int] = None
    party_id: int = 0
    vocal_version: int = 0
    is_story_event_challenge: bool = False


class ChangeNamePayload(BaseModel):
    name: Optional[str] = None


class ChangePhotoAbilityPayload(BaseModel):
    photo_id: int = 0
    item_master_id: int = 0
    photo_effect_type_group_master_id: int = 0


class Character(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_master_id: int = 0
    level: int = 0
    current_experience: int = 0
    talent_stage: int = 0
    awakening_phase: int = 0
    character_base_id: int = 0
    sense_level: int = 0
    read_episode_order: CharacterEpisodeOrder = CharacterEpisodeOrder.None_
    released_episode_order: CharacterEpisodeOrder = CharacterEpisodeOrder.None_
    display_awakening_status: bool = False
    secondary_character_base_id: Optional[int] = None
    secondary_sense_level: int = 0
    selection_type: CharacterSelectionTypes = CharacterSelectionTypes.Primary
    is_favorite: bool = False


class CharacterBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    star_rank: int = 0
    total_star_point: int = 0
    costume_master_id: Optional[int] = None
    key_mission_level: int = 0
    portal_character_id: int = 0
    portal_display_awakening_status: bool = False


class CharacterBaseStarPointResult(BaseModel):
    character_base_master_id: int = 0
    star_point_result: Optional[StarPointResult] = None
    link_character_received_reward: Optional[list[ReceivedThing]] = None


class CharacterFavoritePayload(BaseModel):
    character_id: int = 0
    set_favorite: bool = False


class CharacterLesson(BaseModel):
    character_base_master_id: int = 0
    set_characters: Optional[list[CharacterLessonSlot]] = None
    best_score: int = 0
    leader_position: int = 0
    reward_received_high_score: int = 0


class CharacterLessonSlot(BaseModel):
    position: int = 0
    set_character_id: Optional[int] = None


class CharacterLineupResult(BaseModel):
    normal_probabilities: Optional[list[CharacterRarityProbability]] = None
    fixed_probabilities: Optional[list[CharacterRarityProbability]] = None
    normal_lineup_items: Optional[list[GachaLineupItemProbability]] = None
    fixed_lineup_items: Optional[list[GachaLineupItemProbability]] = None


class CharacterMission(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    character_mission_master_id: int = 0
    current_stage_master_id: int = 0
    current_count: int = 0
    cleared_stage_order: int = 0
    reward_received_stage_order: int = 0
    completed_level: int = 0


class CharacterPointEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_point_event_master_id: int = 0
    character_base_master_id: Optional[int] = None
    total_acquired_point: int = 0
    last_rank: int = 0
    read_tips: bool = False


class CharacterPointEventInformationResult(BaseModel):
    current_total_point: int = 0
    overall_rank: Optional[int] = None
    character_rank: Optional[int] = None


class CharacterPointEventRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRankingWithLongPoint]] = None
    user_profiles: Optional[list[UserProfile]] = None


class CharacterRank(BaseModel):
    m_character_base_id: int = 0
    rank: int = 0


class CharacterRarityProbability(BaseModel):
    rarity: CharacterRarities = CharacterRarities.Rare1
    probability: float = 0.0


class ChatworkSendMessagePayload(BaseModel):
    message: Optional[str] = None


class CircleAuthorityChangePayload(BaseModel):
    circle_hashed_id: Optional[str] = None
    user_id: Optional[str] = None
    authority: CircleAuthorities = CircleAuthorities.None_


class CircleAuthorityResult(BaseModel):
    result_status: CircleAuthorityResultStatus = (
        CircleAuthorityResultStatus.PermissionDenied
    )


class CircleBanner(BaseModel):
    poster_master_id: int = 0
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0
    rotation_angle: int = 0
    display_poster_string: bool = False
    banner_ratio: float = 0.0


class CircleEventCircleMissionProgress(BaseModel):
    circle_event_mission_master_id: int = 0
    current_count: int = 0


class CircleEventInformationResult(BaseModel):
    circle_point: Optional[int] = None
    user_point: int = 0
    last_received_circle_point: int = 0
    mission_refresh_count: int = 0
    progresses: Optional[list[CircleEventCircleMissionProgress]] = None


class CircleEventMission(BaseModel):
    circle_event_mission_master_id: int = 0
    current_count: int = 0
    is_active: bool = False


class CircleEventRanking(BaseModel):
    circle_raw_rankings: Optional[list[CircleRawRanking]] = None
    circle_profiles: Optional[list[CircleProfile]] = None


class CircleInformationResult(BaseModel):
    u_circle_hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: PlayTimeTypes = PlayTimeTypes.Zero
    play_time_end_type: PlayTimeTypes = PlayTimeTypes.Zero
    entry_type: EntryTypes = EntryTypes.None_
    member_count: int = 0
    invite_id: int = 0
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal
    circle_banner: Optional[CircleBanner] = None
    main_character_master_id: int = 0
    display_awakening_status: bool = False
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    icon_fame_master_id: int = 0


class CircleInviteResult(BaseModel):
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal
    invite_id: Optional[int] = None


class CircleMemberInfoParameters(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    player_rank: int = 0
    last_login_at: str = ""
    authority: Optional[CircleAuthorities] = None
    main_u_character: Optional[MainCharacter] = None
    invite_id: Optional[int] = None
    request_id: Optional[int] = None
    trophy_master_id1: int = 0
    trophy_master_id2: int = 0
    trophy_master_id3: int = 0
    main_character_master_id: int = 0
    display_awakening_status: bool = False
    player_rate: Optional[str] = None
    is_public_player_rate: bool = False
    league_class: LeagueClassTypes = LeagueClassTypes.None_
    icon_fame_master_id: int = 0


class CircleMemberInfoResult(BaseModel):
    parameters: Optional[list[CircleMemberInfoParameters]] = None
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal
    circle_banner: Optional[CircleBanner] = None


class CircleMemberParameters(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    player_rank: int = 0
    last_login_at: str = ""
    authority: Optional[CircleAuthorities] = None
    main_u_character: Optional[MainCharacter] = None
    invite_id: Optional[int] = None
    request_id: Optional[int] = None
    trophy_master_id1: int = 0
    trophy_master_id2: int = 0
    trophy_master_id3: int = 0
    main_character_master_id: int = 0
    display_awakening_status: bool = False
    icon_fame_master_id: int = 0


class CirclePayload(BaseModel):
    hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: PlayTimeTypes = PlayTimeTypes.Zero
    play_time_end_type: PlayTimeTypes = PlayTimeTypes.Zero
    entry_type: EntryTypes = EntryTypes.None_
    member_type: SearchCircleMemberConditionTypes = (
        SearchCircleMemberConditionTypes.None_
    )
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None


class CircleProfile(BaseModel):
    circle_id: Optional[str] = None
    name: Optional[str] = None
    member_count: int = 0
    main_character_master_id: int = 0
    display_awakening_status: bool = False
    icon_frame_master_id: int = 0


class CircleRawRanking(BaseModel):
    rank: int = 0
    point: int = 0
    circle_id: Optional[str] = None


class CircleResult(BaseModel):
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal


class CircleSearchIdResult(BaseModel):
    parameters: Optional[CircleMemberParameters] = None
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal


class CircleSearchResult(BaseModel):
    parameters: Optional[list[CircleMemberParameters]] = None
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal
    circle_banner: Optional[CircleBanner] = None


class ComebackCampaign(BaseModel):
    comeback_campaign_master_id: int = 0
    activated_at: str = ""


class Comic(BaseModel):
    comic_episode_master_id: int = 0


class Component(BaseModel):
    pass


class ConcertResult(BaseModel):
    rewards: Optional[list[ReceivedThing]] = None


class ConcertStage(BaseModel):
    concert_stage_master_id: int = 0


class ConcoursDetailInformationResult(BaseModel):
    concours_detail_master_id: int = 0
    rank: Optional[int] = None


class ConcoursInfomationResult(BaseModel):
    details: Optional[list[ConcoursDetailInformationResult]] = None
    current_point: int = 0


class ConnectWithAccount(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    provider: AuthenticationProviders = AuthenticationProviders.Google


class ConnectWithPassword(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")


class ConvertedThingResult(BaseModel):
    exchange_shop_master_id: int = 0
    original_quantity: int = 0
    received_thing: Optional[ReceivedThing] = None


class Costume(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    costume_master_id: int = 0


class CostumeFavoritePayload(BaseModel):
    costume_master_id: int = 0
    character_base_master_id: int = 0
    set_favorite: bool = False


class CourseRankingResult(BaseModel):
    rank: int = 0
    user_id: int = 0
    user_profile: Optional[UserProfile] = None
    course_result: Optional[CourseResult] = None
    note_result: Optional[NoteResult] = None


class CourseResult(BaseModel):
    total_achievement_rate_percent_record: str = Field(
        default_factory=lambda: Decimal()
    )
    best_record_challenge_count: int = 0
    best_record_date: str = ""


class CreateCircleResult(BaseModel):
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal
    circle_hashed_id: Optional[str] = None


class CreateMultiRoomPayload(BaseModel):
    room_name: Optional[str] = None
    password: Optional[str] = None
    can_join_max_member: int = 0
    start_date: str = ""
    end_date: str = ""
    play_mode: MultiRoomPlayModes = MultiRoomPlayModes.AchievementRate
    live_master_id1: int = 0
    live_master_id2: Optional[int] = None
    live_master_id3: Optional[int] = None


class Currency(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    coin: int = 0
    free_jewel: int = 0
    paid_jewel: int = 0


class DailyLesson(BaseModel):
    times_left: int = 0


class DailyLimit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    auto_play_times: int = 0
    daily_lesson_times: int = 0
    last_refreshed_at: Optional[str] = None
    music_course_free_challenge_times: int = 0


class DebugAlbumSimpleArrangingPayload(BaseModel):
    publishing: bool = False
    page: int = 0
    photos: Optional[list[AlbumPhotoPayload]] = None
    m_album_theme_id: Optional[int] = None


class DebugEditLeagueBasicPayload(BaseModel):
    current_class_type: LeagueClassTypes = LeagueClassTypes.None_
    best_class_type: LeagueClassTypes = LeagueClassTypes.None_


class DebugLinkageCodeResult(BaseModel):
    password: Optional[str] = None
    take_over_code_result: Optional[TakeOverCodeResult] = None


class DebugModifyCharacterEnhanceInformationPayload(BaseModel):
    m_character_id: int = 0
    actor_level: int = 0
    is_awaken: bool = False
    sense_level: int = 0
    talent_bloom_stage: int = 0


class DebugModifyPosterEnhanceInformationPayload(BaseModel):
    m_poster_id: int = 0
    level: int = 0
    release_phase: int = 0


class DebugPrepareLeagueGroupUserPayload(BaseModel):
    league_master_id: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    user_ids: Optional[list[int]] = None


class DebugUserIdResult(BaseModel):
    user_id: Optional[str] = None
    hashed_user_id: Optional[str] = None


class Decimal(BaseModel):
    pass


class Decoration(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    decoration_master_id: int = 0


class Dictionary(BaseModel):
    pass


class DonateSupportCompanyResult(BaseModel):
    my_circle_information: Optional[MyCircleInformationResult] = None
    result_status: CircleDonateSupportCompanyResult = (
        CircleDonateSupportCompanyResult.Success
    )


class DonateSupportLevelLimitDetail(BaseModel):
    order: int = 0
    quantity: int = 0


class DonateSupportLevelLimitPayload(BaseModel):
    company: Companies = Companies.None_
    next_level_limit: int = 0
    coin_quantity: int = 0
    details: Optional[list[DonateSupportLevelLimitDetail]] = None


class DugongRun(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    cleared_course_ids: Optional[list[int]] = None
    no_mistake_course_ids: Optional[list[int]] = None
    dugong_run_course_group_id: int = 0


class EditBookmarkPayload(BaseModel):
    music_master_id: int = 0
    bookmark_flag: MusicBookmarkFlags = MusicBookmarkFlags.None_


class EditPartyPayload(BaseModel):
    party_slots: Optional[list[EditPartySlotPayload]] = None
    sense_notation_master_id: Optional[int] = None
    music_master_id: Optional[int] = None
    vocal_version: Optional[int] = None
    is_high_score_challenge: bool = False
    leader_position: Optional[int] = None


class EditPartySlotPayload(BaseModel):
    u_party_slot_id: int = 0
    u_character_id: int = 0
    u_accessory_id: Optional[int] = None
    u_poster_id: Optional[int] = None
    bonus_ability_enable_flags: BonusAbilityEnableFlags = BonusAbilityEnableFlags.None_


class EditPositionPayload(BaseModel):
    slots: Optional[list[EditPositionSlotPayload]] = None


class EditPositionSlotPayload(BaseModel):
    u_party_slot_id: int = 0
    position: int = 0


class EditTrialPartyEventStagePartyPayload(BaseModel):
    trial_party_event_stage_master_id: int = 0
    slots: Optional[list[EditTrialPartyEventStagePartyPayloadSlot]] = None
    leader_position: int = 0


class EditTrialPartyEventStagePartyPayloadSlot(BaseModel):
    position: int = 0
    trial_party_character_master_id: int = 0
    trial_party_poster_master_id: Optional[int] = None
    trial_party_accessory_master_id: Optional[int] = None


class EditUserProfilePayload(BaseModel):
    name: Optional[str] = None
    introduction: Optional[str] = None
    main_u_character_id: int = 0
    m_nameplate_id: Optional[int] = None
    m_name_color_id: int = 0
    m_trophy_id1: Optional[int] = None
    m_trophy_id2: Optional[int] = None
    m_trophy_id3: Optional[int] = None
    is_public_player_rate: bool = False
    display_awakening_status: bool = False
    main_character_master_id: int = 0
    name_base_color_masterid: int = 0
    icon_frame_master_id: int = 0
    home_skin_master_id: int = 0


class EexternalPaymentResult(BaseModel):
    received_jewel_shop_item_master_ids: Optional[list[int]] = None


class Effect(BaseModel):
    order: int = 0
    master_id: int = 0
    effect_types: EffectTypes = EffectTypes.BaseVocalUp
    triggers: list[EffectTrigger] = Field(default_factory=list)
    targets: list[EffectTargetValue] = Field(default_factory=list)
    duration: int = 0


class EffectBranch(BaseModel):
    condition_value: Optional[int] = None
    judge_types: Optional[BranchJudgeTypes] = None
    sense_effects: list[Effect] = Field(default_factory=list)


class EffectTargetValue(BaseModel):
    target_actor_id: Optional[int] = None
    value: float = 0.0


class EffectTrigger(BaseModel):
    type: TriggerTypes = TriggerTypes.OverLife
    value: int = 0


class EnvironmentResult(BaseModel):
    application_version: Optional[str] = None
    asset_version: Optional[str] = None
    api_endpoint: Optional[str] = None
    maintenance_api_endpoint: Optional[str] = None
    news_api_endpoint: Optional[str] = None
    is_maintenance: bool = False
    master_data_url: Optional[str] = None
    static_content_url: Optional[str] = None
    asset_url: Optional[str] = None
    is_app_review: bool = False
    photo_content_url: Optional[str] = None
    multi_real_time_server_url: Optional[str] = None
    external_payment_url: Optional[str] = None


class Episode(BaseModel):
    episode_master_id: int = 0
    has_read_all: bool = False


class EpisodeResult(BaseModel):
    episode_title: Optional[str] = None
    story_type: StoryTypes = StoryTypes.None_
    episode_order: int = 0
    episode_detail_asset_source: Optional[str] = None


# One character's on-screen state for a scene line (a member of EpisodeDetailResult.CharacterMotions).
# Aliases are the vendored-JSON (PascalCase) keys so the files in _data/episodes/ load directly.
class EpisodeDetailCharacterMotionResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    slot_number: int = Field(default=0, alias="SlotNumber")
    facial_expression_master_id: Optional[int] = Field(
        default=None, alias="FacialExpressionMasterId"
    )
    head_motion_master_id: Optional[int] = Field(
        default=None, alias="HeadMotionMasterId"
    )
    head_direction_master_id: Optional[int] = Field(
        default=None, alias="HeadDirectionMasterId"
    )
    body_motion_master_id: Optional[int] = Field(
        default=None, alias="BodyMotionMasterId"
    )
    lip_sync_master_id: Optional[int] = Field(default=None, alias="LipSyncMasterId")
    spine_id: int = Field(default=0, alias="SpineId")
    character_appearance_type: Optional[CharacterAppearanceTypes] = Field(
        default=None, alias="CharacterAppearanceType"
    )
    character_position: CharacterPositions = Field(
        default=CharacterPositions.None_, alias="CharacterPosition"
    )
    character_layer_type: CharacterLayerTypes = Field(
        default=CharacterLayerTypes.None_, alias="CharacterLayerType"
    )
    spine_size: SpineSizes = Field(default=SpineSizes.Middle, alias="SpineSize")


# A single scene line of an episode (dialogue + presentation). The vendored JSON omits null
# fields; the model fills them so the wire array (models/keys.py) has all 24 slots.
class EpisodeDetailResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="Id")
    episode_master_id: int = Field(default=0, alias="EpisodeMasterId")
    order: int = Field(default=0, alias="Order")
    group_order: int = Field(default=0, alias="GroupOrder")
    effect: Optional[str] = Field(default=None, alias="Effect")
    speaker_name: Optional[str] = Field(default=None, alias="SpeakerName")
    font_size: FontSizes = Field(default=FontSizes.Middle, alias="FontSize")
    phrase: Optional[str] = Field(default=None, alias="Phrase")
    title: Optional[str] = Field(default=None, alias="Title")
    background_image_file_name: Optional[str] = Field(
        default=None, alias="BackgroundImageFileName"
    )
    background_character_image_file_name: Optional[str] = Field(
        default=None, alias="BackgroundCharacterImageFileName"
    )
    background_image_file_fade_type: Optional[FadeTypes] = Field(
        default=None, alias="BackgroundImageFileFadeType"
    )
    bgm_file_name: Optional[str] = Field(default=None, alias="BgmFileName")
    se_file_name: Optional[str] = Field(default=None, alias="SeFileName")
    still_photo_file_name: Optional[str] = Field(
        default=None, alias="StillPhotoFileName"
    )
    movie_file_name: Optional[str] = Field(default=None, alias="MovieFileName")
    window_effect: Optional[WindowEffects] = Field(default=None, alias="WindowEffect")
    scene_camera_master_id: Optional[int] = Field(
        default=None, alias="SceneCameraMasterId"
    )
    voice_file_name: Optional[str] = Field(default=None, alias="VoiceFileName")
    character_motions: Optional[list[EpisodeDetailCharacterMotionResult]] = Field(
        default=None, alias="CharacterMotions"
    )
    speaker_icon_id: Optional[str] = Field(default=None, alias="SpeakerIconId")
    fade_value1: Optional[float] = Field(default=None, alias="FadeValue1")
    fade_value2: Optional[float] = Field(default=None, alias="FadeValue2")
    fade_value3: Optional[float] = Field(default=None, alias="FadeValue3")


class Event(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    total_acquired_point: int = 0
    acquired_point_updated_date: str = ""
    last_rank: Optional[int] = None
    read_tips: bool = False
    login_days: int = 0


class EventBoxGacha(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_box_gacha_master_id: int = 0
    current_box_count: int = 0


class EventBoxGachaBoxThing(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_box_gacha_box_thing_master_id: int = 0
    hit_count: int = 0


class EventBoxGachaRollResult(BaseModel):
    received_things: Optional[list[ReceivedThing]] = None
    has_reset: bool = False
    drawn_event_box_gacha_box_thing_master_ids: Optional[list[int]] = None


class EventCamp(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    camp_type: CampTypes = CampTypes.None_
    total_support_point: int = 0


class EventResult(BaseModel):
    acquired_event_point: Optional[int] = None
    attached_story_event_master_id: Optional[int] = None
    circle_event_high_score: Optional[int] = None
    circle_event_high_score_multiplier_percent: Optional[int] = None
    circle_event_before_high_score: Optional[int] = None
    high_score_before: Optional[int] = None
    high_score_after: Optional[int] = None
    before_rank: int = 0
    after_rank: int = 0
    story_event_master_id: Optional[int] = None
    event_master_id: Optional[int] = None
    this_time_support_point: Optional[int] = None
    camp_before_rank: Optional[int] = None
    camp_after_rank: Optional[int] = None


class ExchangeLimit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    exchange_shop_thing_id: int = 0
    replace_type: ShopReplaceTypes = ShopReplaceTypes.None_
    specified_number_of_days_limit: Optional[int] = None
    exchanged_count: int = 0
    until: Optional[str] = None


class ExchangeShopThingPayload(BaseModel):
    m_exchange_shop_thing_id: int = 0
    quantity: int = 0


class FavoriteCostume(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    favorite_costume_master_ids: Optional[list[int]] = None


class FavoriteStampOrderPayload(BaseModel):
    stamp_master_ids: Optional[list[int]] = None


class FinishAnotherNotationLivePayload(BaseModel):
    base_score_blocks: Optional[list[BaseScoreBlock]] = None
    sense_score_blocks: Optional[list[SenseScoreBlock]] = None
    star_act_score_blocks: Optional[list[StarActScoreBlock]] = None
    multi_live_additional_score_blocks: Optional[
        list[MultiLiveAdditionalScoreBlock]
    ] = None
    another_notation_master_id: int = 0
    is_auto_play: bool = False


class FinishLessonPayload(BaseModel):
    score: int = 0
    max_combo: int = 0
    judges: Optional[list[NoteJudgePayload]] = None


class FinishLivePayload(BaseModel):
    score: int = 0
    max_combo: int = 0
    judges: Optional[list[NoteJudgePayload]] = None
    is_cleared: bool = False
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
    clear_lamp: ClearLamps = ClearLamps.None_
    rate_grade: AchievementRateGrades = AchievementRateGrades.None_
    is_high_score: bool = False
    audition_before_phase: int = 0
    audition_after_phase: int = 0
    audition_rewards: Optional[list[ReceivedThing]] = None
    story_event_rewards: Optional[list[ReceivedThing]] = None
    achievement_rate_average: float = 0.0
    audition_master_id: Optional[int] = None
    sp_rate_update_result: Optional[SpRateUpdateResult] = None
    tournament_result: Optional[TournamentResult] = None
    celling_max_count: Optional[int] = None
    celling_user_count: Optional[int] = None
    before_clear_lamp: ClearLamps = ClearLamps.None_
    poster_drop_up_percent: int = 0
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


class FlashSaleStage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    flash_sale_stage_master_id: int = 0
    purchase_limited_at: Optional[str] = None
    is_default: bool = False
    is_completed: bool = False


class FriendAcceptResult(BaseModel):
    result_status: FriendAcceptResultStatus = FriendAcceptResultStatus.AcceptSuccess


class FriendFavoritePayload(BaseModel):
    target_user_id: Optional[str] = None
    set_favorite: bool = False


class FriendInvitation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    invitation_code: Optional[str] = None
    has_input_other_invitation_code: bool = False


class FriendInvitationMission(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    friend_invitation_mission_master_id: int = 0
    friend_invitation_mission_stage_master_id: int = 0
    current_count: int = 0
    is_cleared: bool = False
    is_reward_received: bool = False


class FriendInvitationMissionPayload(BaseModel):
    friend_invitation_mission_master_ids: Optional[list[int]] = None


class FriendInvitationUserInfoResult(BaseModel):
    hashed_user_id: Optional[str] = None
    name: Optional[str] = None
    player_rank: int = 0
    result_status: InvitationCodeResultStatuses = InvitationCodeResultStatuses.Success


class FriendListResult(BaseModel):
    results: Optional[list[FriendResult]] = None
    current_friend_count: int = 0


class FriendRequest(BaseModel):
    request_user_id: Optional[str] = None
    received_user_id: Optional[str] = None
    request_user_name: Optional[str] = None


class FriendRequestResult(BaseModel):
    result_status: FriendRequestResultStatus = FriendRequestResultStatus.RequestSuccess


class FriendResult(BaseModel):
    user_id: Optional[str] = None
    player_rank: int = 0
    trophy_master_id1: int = 0
    trophy_master_id2: int = 0
    trophy_master_id3: int = 0
    introduction: Optional[str] = None
    last_logged_in_at: str = ""
    name: Optional[str] = None
    player_rate: Optional[float] = None
    is_public_player_rate: bool = False
    league_class: LeagueClassTypes = LeagueClassTypes.None_
    character_ranks: Optional[list[CharacterRank]] = None
    is_public_album_main_page: bool = False
    main_character_master_id: int = 0
    display_awakening_status: bool = False
    icon_frame_master_id: int = 0
    is_favorite: bool = False


class FriendSearchResult(BaseModel):
    friend_result: Optional[FriendResult] = None
    result_status: FriendSearchResultStatus = FriendSearchResultStatus.Friend


class Gacha(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    gacha_master_id: int = 0
    roll_count: int = 0


class GachaHistoryResult(BaseModel):
    master_id: int = 0
    created_at: str = ""


class GachaInfoResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    roll_limits: Optional[list[GachaRollLimit]] = None
    normal_emission_flags: GachaEmissionFlags = GachaEmissionFlags.Rare2
    fixed_emission_flags: GachaEmissionFlags = GachaEmissionFlags.Rare2


class GachaLineupItemProbability(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    probability: float = 0.0


class GachaReRoll(BaseModel):
    gacha_master_id: int = 0
    roll_count: int = 0
    is_decided: bool = False


class GachaRollLimit(BaseModel):
    gacha_detail_master_id: int = 0
    roll_left: int = 0


class GachaRollResult(BaseModel):
    m_gacha_master_id: int = 0
    received_things: Optional[list[GachaThingResult]] = None
    received_bonus_things: Optional[list[ReceivedThing]] = None
    received_detail_bonus_things: Optional[list[ReceivedThing]] = None
    received_roll_bonus_things: Optional[list[ReceivedThing]] = None


class GachaSelectedThing(BaseModel):
    gacha_master_id: int = 0
    gacha_thing_ids: Optional[list[int]] = None


class GachaSelectedThingsResult(BaseModel):
    selected_gacha_thing_ids: Optional[list[int]] = None


class GachaThingResult(BaseModel):
    received_things: Optional[list[ReceivedThing]] = None
    additional_received_things: Optional[list[ReceivedThing]] = None
    movie_costume_master_id: Optional[int] = None


class GameHint(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    page_category: PageCategories = PageCategories.TutorialIngame
    has_already_read: bool = False


class GameHintMonoBehaviour(BaseModel):
    pass


class GenerateLotteryResultPayload(BaseModel):
    prize: int = 0
    amount: int = 0


class GeneratePhotoPayload(BaseModel):
    character_base_master_id: Optional[int] = None
    item_master_id: int = 0
    image_data: Optional[list[int]] = None
    thumbnail_image_data: Optional[list[int]] = None
    appeared_characters: Optional[list[PhotoAppearedCharacter]] = None


class GeneratePhotoResult(BaseModel):
    photo_id: int = 0
    file_name: Optional[str] = None
    sas_token: Optional[str] = None
    rarity: PhotoRarities = PhotoRarities.Rare1
    sign_master_id: Optional[int] = None
    photo_effect_master_id: Optional[int] = None


class GeneratePhotosPayload(BaseModel):
    payloads: Optional[list[GeneratePhotoPayload]] = None


class GhostLiveInfo(BaseModel):
    leader_position: int = 0
    party_slot: Optional[list[PartySlotDetail]] = None


class GhostLiveResult(BaseModel):
    ghost_user_profile: Optional[UserProfileDetail] = None
    ghost_user_score: int = 0
    total_battle_win_count: int = 0
    matching_result: MatchingResult = MatchingResult.Win
    display_character_master_id: int = 0
    display_character_awakening_status: bool = False


class GradualMissionGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    gradual_mission_group_master_id: int = 0
    start_at: str = ""


class HighScoreBuff(BaseModel):
    user_id: Optional[str] = None
    buffs: Optional[list[HighScoreBuffSetting]] = None


class HighScoreBuffSetting(BaseModel):
    story_event_high_score_buff_setting_id: int = 0
    current_level: int = 0


class HighScoreParty(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    party_name: Optional[str] = None
    slots: Optional[list[HighScorePartySlot]] = None
    difficulty: MusicDifficulties = MusicDifficulties.None_
    leader_position: int = 0


class HighScorePartySlot(BaseModel):
    position: int = 0
    character_master_id: int = 0
    character_level: int = 0
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status: Optional[Status] = None
    character_display_awakening_status: bool = False


class HomeBGM(BaseModel):
    home_b_g_m_master_id: int = 0
    selection_type: HomeBGMSelectionTypes = HomeBGMSelectionTypes.UserSelect
    home_b_g_m_detail_master_id: Optional[int] = None


class HomeDisplayPreference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    home_character_base_master_id: Optional[int] = None
    member_character_base_master_id: Optional[int] = None
    story_character_base_master_id: Optional[int] = None
    shop_character_base_master_id: Optional[int] = None
    home_costume_master_id: Optional[int] = None
    member_costume_master_id: Optional[int] = None
    story_costume_master_id: Optional[int] = None
    shop_costume_master_id: Optional[int] = None
    illust_character_master_id: int = 0
    display_awakening_status: bool = False
    home_character_display_type: HomeCharacterDisplayTypes = (
        HomeCharacterDisplayTypes.CharacterModel
    )
    login_bonus_character_base_master_id: Optional[int] = None
    login_bonus_costume_master_id: Optional[int] = None


class HomeSkin(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    home_skin_master_ids: Optional[list[int]] = None


class IconFrame(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    icon_frame_master_ids: Optional[list[int]] = None


class Inbox(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    thing_type: ThingTypes = ThingTypes.Item
    thing_id: int = 0
    thing_quantity: int = 0
    is_time_limited: bool = False
    has_received: bool = False
    title: Optional[str] = None
    description: Optional[str] = None
    sent_at: str = ""
    received_at: Optional[str] = None
    receive_limit_at: str = ""


class InboxReceiveResult(BaseModel):
    received_things: Optional[list[ReceivedThing]] = None
    has_not_receive_things: bool = False


class InviteMultiRoomPayload(BaseModel):
    hashed_user_ids: Optional[list[str]] = None


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    item_master_id: int = 0
    stock: int = 0


class JewelShop(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    jewel_shop_item_master_id: int = 0
    purchase_count: int = 0
    total_purchase_count: int = 0
    re_purchase_date: Optional[str] = None


class JoinMultiRoomPayload(BaseModel):
    hashed_room_id: Optional[str] = None
    password: Optional[str] = None


class LeagueBasic(BaseModel):
    my_property: int = 0
    star_enroll_count: int = 0
    dai_star_enroll_count: int = 0
    current_class_type: LeagueClassTypes = LeagueClassTypes.None_
    best_class_type: LeagueClassTypes = LeagueClassTypes.None_
    last_joined_league_season_master_id: Optional[int] = None


class LeagueGroup(BaseModel):
    league_master_id: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    class_order: int = 0


class LeagueGroupMember(BaseModel):
    league_group_id: int = 0
    league_master_id: int = 0
    best_score: Optional[int] = None


class LeagueHighScoreParty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    league_master_id: int = 0
    high_score: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    difficulty: MusicDifficulties = MusicDifficulties.None_
    music_master_id: int = 0
    league_group_id: int = 0
    slots: Optional[list[LeagueHighScorePartySlot]] = None
    user_name: Optional[str] = None
    acting_ability: int = 0
    leader_position: int = 0


class LeagueHighScorePartySlot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    league_high_score_party_id: int = 0
    position: int = 0
    character_master_id: int = 0
    character_level: int = 0
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status: Optional[Status] = None
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    character_display_awakening_status: bool = False


class LeagueHistory(BaseModel):
    league_master_id: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    history_count: int = 0
    is_sended_reward: bool = False
    is_played: bool = False
    class_change_type: LeagueClassChangeTypes = LeagueClassChangeTypes.None_
    group_rank: int = 0
    global_rank: int = 0
    all_class_global_rank: int = 0


class LeaguePartyAndRankingResult(BaseModel):
    rank: Optional[int] = None
    user_id: Optional[str] = None
    best_score: int = 0
    league_master_id: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    user_name: Optional[str] = None
    acting_ability: int = 0
    slots: Optional[list[LeaguePartySlotResult]] = None
    difficulty: MusicDifficulties = MusicDifficulties.None_


class LeaguePartySlotResult(BaseModel):
    slot_position: int = 0
    character_master_id: int = 0
    attribute: Attributes = Attributes.Cute
    character_rarity: CharacterRarities = CharacterRarities.Rare1
    character_level: int = 0
    poster_master_id: Optional[int] = None
    poster_rarity: Optional[PossessionRarities] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_rarity: Optional[PossessionRarities] = None
    accessory_level: Optional[int] = None
    current_status: Optional[Status] = None
    position: int = 0
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    character_display_awakening_status: bool = False


class LeagueReceiveResults(BaseModel):
    class_reward_received_things: Optional[list[ReceivedThing]] = None
    class_reward_type: LeagueClassChangeTypes = LeagueClassChangeTypes.None_
    first_achieve_received_things: Optional[list[ReceivedThing]] = None
    group_rank_received_things: Optional[list[ReceivedThing]] = None
    is_first_time_enrolled_class: bool = False
    all_class_global_rank_received_things: Optional[list[ReceivedThing]] = None


class LeagueResult(BaseModel):
    before_group_ranking: Optional[int] = None
    after_group_ranking: int = 0
    lowest_up_border_score: Optional[int] = None
    lowest_keep_border_score: Optional[int] = None
    enrolled_group_number: int = 0
    is_in_counting: bool = False


class LeagueSeasonResult(BaseModel):
    league_season_master_id: int = 0
    dai_star_max_enroll_count: int = 0


class LeagueTopMenuInformationResult(BaseModel):
    display_start_at: str = ""
    counting_start_at: str = ""
    display_end_at: str = ""
    music_master_id: int = 0
    league_group_ranking: int = 0
    up_class_border_score: Optional[int] = None
    up_class_border_ranking: Optional[int] = None
    keep_class_border_score: Optional[int] = None
    keep_class_border_ranking: Optional[int] = None
    group_lowest_rank: Optional[int] = None
    is_participated: bool = False
    enrolled_group_number: Optional[int] = None


class LessonResult(BaseModel):
    character_base_master_id: int = 0
    star_point_result: Optional[StarPointResult] = None
    high_score_rewards: Optional[list[ReceivedThing]] = None
    high_score_before: int = 0
    high_score_after: int = 0


class LevelUpPhotoPayload(BaseModel):
    photo_id: int = 0
    after_level: int = 0


class LevelUpPhotoResult(BaseModel):
    photo_id: int = 0
    before_level: int = 0
    after_level: int = 0


class Limit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    additional_acquirable_photo_limit: int = 0
    acquirable_photo_limit_increased_times: int = 0
    additional_acquirable_accessory_limit: int = 0
    acquirable_accessory_limit_increased_times: int = 0


class LinkCharacter(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    company_master_id: int = 0
    linked_character_base_master_id: Optional[int] = None
    reward_received_max_rank: int = 0


class Live(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    live_master_id: int = 0
    times_completed: int = 0
    achievement_rate: float = 0.0
    notation_rate: float = 0.0
    clear_lamp: ClearLamps = ClearLamps.None_
    status: LiveReleaseStatus = LiveReleaseStatus.None_
    rate_grade: AchievementRateGrades = AchievementRateGrades.None_


class LiveAchievement(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    olivier_released_count: int = 0
    olivier_cleared_level: int = 0


class LiveDropCelling(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    multi_live_schedule_master_id: int = 0
    count: int = 0
    total_celling_count: int = 0


class LiveDropLimit(BaseModel):
    multi_live_schedule_master_id: int = 0
    current_count: int = 0
    count_limit: int = 0


class LiveDropThing(BaseModel):
    received_thing: Optional[ReceivedThing] = None
    order: int = 0
    live_drop_type: LiveDropTypes = LiveDropTypes.Normal
    is_fixed_drop: bool = False


class LiveTimeEvent(BaseModel):
    timings: list[SenseTimingEvent] = Field(default_factory=list)
    cool_times: list[SenseCoolTime] = Field(default_factory=list)


class LiveStatus(BaseModel):
    concentration: int = 0
    expression: int = 0
    vocal: int = 0
    total_status: int = 0


class Actor(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    character_master_id: int = 0
    awakening_phase: int = 0
    talent_stage: int = 0
    position: int = 0
    sense_level: int = 0
    base_status: LiveStatus = Field(default_factory=lambda: LiveStatus())
    current_status: LiveStatus = Field(default_factory=lambda: LiveStatus())
    display_awakening_status: bool = False
    secondary_character_base_master_id: Optional[int] = None
    secondary_sense_level: int = 0
    selection_type: CharacterSelectionTypes = CharacterSelectionTypes.Primary


class LiveUnit(BaseModel):
    # actors/time_events are MessagePack maps (Dictionary<int, ...>); we hold them as plain
    # dicts so to_wire serializes them as msgpack maps
    actors: dict = Field(default_factory=dict)
    time_events: dict = Field(default_factory=dict)
    possible_senses: list[Sense] = Field(default_factory=list)
    start_effects: list[Effect] = Field(default_factory=list)
    star_act: StarAct = Field(default_factory=lambda: StarAct())
    total_status: int = 0
    star_act_sense_light_count: int = 0
    max_principal: int = 0
    is_first_play_olivier: bool = False
    base_score_percentage: int = 0
    base_score_difficulty_auto_coefficient: float = 0.0
    u_active_live_id: int = 0


class LiveUnitWithOrder(BaseModel):
    actors: Optional[Dictionary] = None
    time_events: Optional[Dictionary] = None
    possible_senses: Optional[list[Sense]] = None
    start_effects: Optional[list[Effect]] = None
    star_act: Optional[StarAct] = None
    total_status: int = 0
    star_act_sense_light_count: int = 0
    max_principal: int = 0
    is_first_play_olivier: bool = False
    base_score_percentage: int = 0
    base_score_difficulty_auto_coefficient: float = 0.0
    u_active_live_id: int = 0
    order: int = 0


class LoginBonusDetail(BaseModel):
    thing_type: ThingTypes = ThingTypes.Item
    thing_id: int = 0
    thing_quantity: int = 0
    login_count: int = 0


class LoginBonusResult(BaseModel):
    login_bonus_id: int = 0
    current_login_count: int = 0
    received_things: Optional[list[ReceivedThing]] = None
    title: Optional[str] = None
    type: LoginBonusTypes = LoginBonusTypes.Normal
    start_date: str = ""
    end_date: Optional[str] = None
    message_template: Optional[str] = None
    background_image_path: Optional[str] = None
    cardboard_image_path: Optional[str] = None
    logo_image_path: Optional[str] = None
    total_days: int = 0
    is_loop: bool = False
    order: int = 0
    details: Optional[list[LoginBonusDetail]] = None
    navigation_spine_id: Optional[str] = None
    voice_asset_id: Optional[str] = None
    head_motion_master_id: Optional[int] = None
    facial_expression_master_id: Optional[int] = None
    head_direction_master_id: Optional[int] = None
    body_motion_master_id: Optional[int] = None
    lip_sync_master_id: Optional[int] = None
    layout_type: LoginBonusLayoutTypes = LoginBonusLayoutTypes.Normal
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
    spine_select_type: LoginBonusSpineSelectType = LoginBonusSpineSelectType.Random
    details: Optional[list[LoginBonusSpineDetail]] = None


class LoginPassStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    valid_until: str = ""


class LoginPayload(BaseModel):
    push_notification_token: Optional[str] = None


class LoginResult(BaseModel):
    invalided_star_passes: Optional[list[StarPassTypes]] = None
    login_pass_notification: LoginPassNotificationTypes = (
        LoginPassNotificationTypes.None_
    )
    is_approaching_login_pass_invalided: bool = False
    invalided_item_master_ids: Optional[list[int]] = None
    approaching_item_master_ids: Optional[list[int]] = None
    story_event_point_exchange_result: Optional[list[StoryEventPointExchangeResult]] = (
        None
    )
    invalided_buff_item_master_ids: Optional[list[int]] = None


class Lottery(BaseModel):
    lottery_master_id: int = 0
    results: Optional[list[LotteryPriseResult]] = None


class LotteryPriseResult(BaseModel):
    prize: int = 0
    amount: int = 0


class MainCharacter(BaseModel):
    character_master_id: int = 0
    awakening_phase: int = 0
    talent_stage: int = 0
    level: int = 0
    display_awakening_status: bool = False


class Market(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    last_refreshed_at: str = ""
    refresh_times: int = 0


class MarketResult(BaseModel):
    things: Optional[list[MarketThing]] = None
    required_jewel_for_refresh: Optional[int] = None


class MarketThing(BaseModel):
    frame_number: int = 0
    market_frame_thing_master_id: int = 0
    has_purchased: bool = False
    discount_percent: Optional[int] = None


class MarshalByRefObject(BaseModel):
    pass


class MasterDataManifest(BaseModel):
    uri: Optional[str] = None
    sas_token: Optional[str] = None
    version: Optional[str] = None
    publish_timestamp: int = 0


class MatchingGhostLiveResult(BaseModel):
    ghost_live_master_id: int = 0
    ghost_user_profile: Optional[UserProfileDetail] = None
    ghost_live_info: Optional[GhostLiveInfo] = None


class Mission(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    is_cleared: bool = False
    is_reward_received: bool = False
    mission_current_count: int = 0
    mission_master_id: int = 0
    current_mission_stage_master_id: int = 0


class MissionCleared(BaseModel):
    mission_master_id: int = 0
    mission_stage_master_id: int = 0


class MissionPass(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    user_id: int = 0
    mission_pass_master_id: int = 0
    paid: bool = False
    free_reward_received_phase: Optional[int] = None
    sp_reward_received_phase: Optional[int] = None
    terminated: bool = False
    free_reward_loop_count: Optional[int] = None
    free_reward_loop_received_phase: Optional[int] = None
    paid_reward_loop_count: Optional[int] = None
    paid_reward_loop_received_phase: Optional[int] = None


class MissionPassRewardsResult(BaseModel):
    mission_pass_rewards: Optional[list[ReceivedThing]] = None
    reward_result: MissionPassRewardStatus = MissionPassRewardStatus.NotReceived


class MonoBehaviour(BaseModel):
    pass


class MultiLiveAdditionalScoreBlock(BaseModel):
    hash: int = 0
    score: int = 0
    life: int = 0
    time_event_second: int = 0
    combo: int = 0


class MultiLiveInformation(BaseModel):
    scores: Dictionary = Field(default_factory=lambda: Dictionary())


class MultiLiveRestriction(BaseModel):
    restriction_finished_at: Optional[str] = None


class MultiRoomBasic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    owner_multi_room_id: Optional[str] = None


class MultiRoomCreateResult(BaseModel):
    hashed_multi_room_id: Optional[str] = None
    room_detail: Optional[MultiRoomDetailResult] = None


class MultiRoomDetailResult(BaseModel):
    multi_room_information_result: Optional[MultiRoomInformationResult] = None
    multi_room_rankings: Optional[list[MultiRoomRanking]] = None
    is_finished: bool = False
    password: Optional[str] = None


class MultiRoomInformationResult(BaseModel):
    hashed_multi_room_id: Optional[str] = None
    room_name: Optional[str] = None
    play_mode: MultiRoomPlayModes = MultiRoomPlayModes.AchievementRate
    joined_member_count: int = 0
    can_join_max_member: int = 0
    start_date: str = ""
    end_date: str = ""
    live_master_id1: int = 0
    live_master_id2: Optional[int] = None
    live_master_id3: Optional[int] = None
    has_password: bool = False


class MultiRoomInvitedResult(BaseModel):
    owner_user_name: Optional[str] = None
    multi_room_information_result: Optional[MultiRoomInformationResult] = None


class MultiRoomJoinnedResult(BaseModel):
    my_rank: int = 0
    my_score: Optional[int] = None
    my_total_achievement_rate_percent_record: Optional[str] = None
    multi_room_information_result: Optional[MultiRoomInformationResult] = None


class MultiRoomPartySlot(BaseModel):
    position: int = 0
    character_master_id: int = 0
    character_level: int = 0
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    character_display_awakening_status: bool = False
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    u_accessory_id: Optional[int] = None
    current_status: Optional[Status] = None


class MultiRoomRanking(BaseModel):
    user_id: Optional[str] = None
    rank: int = 0
    is_owner: bool = False
    score: Optional[int] = None
    total_achievement_rate_percent_record: Optional[str] = None
    best_record_challenge_count: int = 0
    best_record_date: Optional[str] = None
    user_profile: Optional[UserProfile] = None
    party_info: Optional[PartyInfo] = None
    note_result: Optional[NoteResult] = None


class Music(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    stella_released: bool = False
    vocal_version: int = 0
    olivier_release_status: OlivierReleaseStatuses = OlivierReleaseStatuses.None_
    is_possession: bool = False


class MusicBookmark(BaseModel):
    music_master_id: int = 0
    music_bookmark_flag: MusicBookmarkFlags = MusicBookmarkFlags.None_


class MusicCourse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_course_master_id: int = 0
    clear_lamp: ClearLamps = ClearLamps.None_
    certification_grade: MusicCourseCertificationGrade = (
        MusicCourseCertificationGrade.None_
    )
    total_achievement_rate_percent_record: Optional[str] = None


class MusicCourseRandomSelectResult(BaseModel):
    details: Optional[list[MusicCourseRandomSelectResultDetail]] = None


class MusicCourseRandomSelectResultDetail(BaseModel):
    set_list_number: int = 0
    live_master_id: int = 0


class MusicCourseRanking(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_course_master_id: int = 0
    current_challenge_count: int = 0
    perfect_star: int = 0
    perfect: int = 0
    great: int = 0
    good: int = 0
    bad: int = 0
    miss: int = 0
    total_achievement_rate_percent_record: Optional[str] = None
    best_record_challenge_count: int = 0
    best_record_date: Optional[str] = None
    has_received_reward: bool = False


class MusicCourseRankingPayload(BaseModel):
    user_id: int = 0
    current_challenge_count: int = 0
    perfect_star: int = 0
    perfect: int = 0
    great: int = 0
    good: int = 0
    bad: int = 0
    miss: int = 0
    total_achievement_rate_percent_record: str = Field(
        default_factory=lambda: Decimal()
    )
    best_record_challenge_count: int = 0
    best_record_date: Optional[str] = None


class MusicVideo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_video_master_id: int = 0


class MyCircleInformationResult(BaseModel):
    u_circle_hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: PlayTimeTypes = PlayTimeTypes.Zero
    play_time_end_type: PlayTimeTypes = PlayTimeTypes.Zero
    entry_type: EntryTypes = EntryTypes.None_
    member_count: int = 0
    my_authority: CircleAuthorities = CircleAuthorities.None_
    result_status: CircleResultStatus = CircleResultStatus.RequestIllegal
    circle_banner: Optional[CircleBanner] = None
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    support_company_information: Optional[SupportCompanyInformation] = None
    support_company: Companies = Companies.None_
    daily_added_support_point: int = 0
    is_publish_ranking: bool = False
    stamina_last_received_at: str = ""
    circle_authority_update_type: CircleAuthorityUpdateTypes = (
        CircleAuthorityUpdateTypes.None_
    )


class NameBaseColor(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name_base_color_master_ids: Optional[list[int]] = None


class NameColor(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name_color_master_ids: Optional[list[int]] = None


class Nameplate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name_plate_master_id: int = 0


class Note(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    note_master_ids: Optional[list[int]] = None


class NoteJudgePayload(BaseModel):
    timing: TimingTypes = TimingTypes.None_
    count: int = 0


class NoteResult(BaseModel):
    perfect_star: int = 0
    perfect: int = 0
    great: int = 0
    good: int = 0
    bad: int = 0
    miss: int = 0


class Notification(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    important_read_at: str = ""
    update_read_at: str = ""
    bug_read_at: str = ""


class NotificationContentResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    body: Optional[str] = None
    title: Optional[str] = None
    posting_at: str = ""
    last_updated_at: str = ""
    notification_tab_category: NotificationTabCategory = (
        NotificationTabCategory.Important
    )
    notification_category: NotificationCategory = NotificationCategory.Notification
    banner_path: Optional[str] = None


class NotificationResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    banner_path: Optional[str] = None
    title: Optional[str] = None
    posting_at: str = ""
    last_updated_at: str = ""
    notification_tab_category: NotificationTabCategory = (
        NotificationTabCategory.Important
    )
    notification_category: NotificationCategory = NotificationCategory.Notification
    is_confirmation: bool = False
    order: int = 0


class Party(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    name: Optional[str] = None
    leader_position: int = 0


class PartyInfo(BaseModel):
    leader_position: int = 0
    multi_room_party_slots: Optional[list[MultiRoomPartySlot]] = None


class PartyPayload(BaseModel):
    leader_position: int = 0
    party_slot_payload: Optional[list[PartySlotPayload]] = None


class PartySlot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    party_id: int = 0
    position: int = 0
    character_id: int = 0
    poster_id: Optional[int] = None
    accessory_id: Optional[int] = None
    bonus_ability_enable_flags: BonusAbilityEnableFlags = BonusAbilityEnableFlags.None_


class PartySlotAccessoryPayload(BaseModel):
    m_accessory_id: int = 0
    level: int = 0
    m_accessory_effect_id1: Optional[int] = None
    m_accessory_effect_id2: Optional[int] = None
    m_accessory_effect_id3: Optional[int] = None


class PartySlotCharacterPayload(BaseModel):
    m_character_id: int = 0
    talent_stage: int = 0
    awakening_phase: int = 0
    level: int = 0
    sense_level: int = 0
    current_experience: int = 0
    released_episode_order: CharacterEpisodeOrder = CharacterEpisodeOrder.None_
    read_episode_order: CharacterEpisodeOrder = CharacterEpisodeOrder.None_
    display_awakening_status: bool = False


class PartySlotDetail(BaseModel):
    position: int = 0
    character_master_id: int = 0
    character_level: int = 0
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    character_display_awakening_status: bool = False
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status_vocal: int = 0
    current_status_expression: int = 0
    current_status_concentration: int = 0
    u_accessory_id: Optional[int] = None


class PartySlotPayload(BaseModel):
    position: int = 0
    party_slot_character_payload: Optional[PartySlotCharacterPayload] = None
    party_slot_poster_payload: Optional[PartySlotPosterPayload] = None
    party_slot_accessory_payload: Optional[PartySlotAccessoryPayload] = None


class PartySlotPosterPayload(BaseModel):
    m_poster_id: int = 0
    level: int = 0
    phase: int = 0
    released_episode: PosterEpisodeTypes = PosterEpisodeTypes.Information


class PermanentMarketThing(BaseModel):
    permanent_market_thing_master_id: int = 0
    purchase_count: int = 0


class Photo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    file_name: Optional[str] = None
    sas_token: Optional[str] = None
    photo_effect_master_id: Optional[int] = None
    lock: bool = False
    use_album_page: Optional[int] = None
    level: int = 0
    rarity: PhotoRarities = PhotoRarities.Rare1
    sign_master_id: Optional[int] = None
    generated_at: str = ""
    thumbnail_sas_token: Optional[str] = None
    appeared_character_base_master_ids: Optional[list[int]] = None
    tagged_character_base_master_ids: Optional[list[int]] = None
    use_deco_page: UseDecoPageFlag = UseDecoPageFlag.None_


class PhotoAppearedCharacter(BaseModel):
    character_base_master_id: int = 0
    is_main_character: bool = False


class PickupCharacterMission(BaseModel):
    pickup_character_mission_master_id: int = 0
    received_detail_master_ids: Optional[list[int]] = None


class PlayerRankPointResult(BaseModel):
    rank_before: int = 0
    rank_after: int = 0
    rank_point_before: int = 0
    rank_point_after: int = 0
    rank_point_acquired: int = 0
    stamina_before: int = 0


class Poster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    poster_master_id: int = 0
    level: int = 0
    breakthrough_phase: int = 0
    released_episode: PosterEpisodeTypes = PosterEpisodeTypes.Information
    item_consume_break_through_count: int = 0
    is_favorite: bool = False
    alternative_image_pattern: int = 0


class PosterAlternativeImagePayload(BaseModel):
    poster_id: int = 0
    pattern: int = 0


class PosterFavoritePayload(BaseModel):
    poster_id: int = 0
    set_favorite: bool = False


class PosterLineupResult(BaseModel):
    normal_probabilities: Optional[list[PosterRarityProbability]] = None
    fixed_probabilities: Optional[list[PosterRarityProbability]] = None
    normal_lineup_items: Optional[list[GachaLineupItemProbability]] = None
    fixed_lineup_items: Optional[list[GachaLineupItemProbability]] = None


class PosterRarityProbability(BaseModel):
    rarity: PossessionRarities = PossessionRarities.R
    probability: float = 0.0


class ProcessPaymentResult(BaseModel):
    result: ProcessPaymentTransactionResult = ProcessPaymentTransactionResult.Success


class PurchaseItemPayload(BaseModel):
    m_jewel_shop_item_id: int = 0


class RateResult(BaseModel):
    achievement_rate_result: Optional[RateUpdateResult] = None
    live_rate_result: Optional[RateUpdateResult] = None
    total_rate_before: float = 0.0
    total_rate_after: float = 0.0


class RateUpdateResult(BaseModel):
    best_ever: float = 0.0
    this_time: float = 0.0


class RawHighScoreRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRankingWithLongPoint]] = None
    high_score_parties: Optional[list[HighScoreParty]] = None
    high_score_buffs: Optional[list[HighScoreBuff]] = None
    user_profiles: Optional[list[UserProfile]] = None


class RawRanking(BaseModel):
    rank: int = 0
    point: int = 0
    user_id: Optional[str] = None
    group_value: int = 0


class RawRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRanking]] = None
    user_profiles: Optional[list[UserProfile]] = None


class RawRankingWithLongPoint(BaseModel):
    rank: int = 0
    point: int = 0
    user_id: Optional[str] = None


class ReadNotificationPayload(BaseModel):
    tab_category: NotificationTabCategory = NotificationTabCategory.Important
    read_at: str = ""


class ReceivedThing(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: ThingTypes = ThingTypes.Item
    id_: Optional[int] = Field(default=None, alias="id")
    quantity: int = 0
    original_type: Optional[ThingTypes] = None
    original_id: Optional[int] = None
    after_phase: Optional[int] = None
    sent_inbox: bool = False


class RecyclableMonoBehaviour(BaseModel):
    pass


class RegisterAppStorePaymentPayload(BaseModel):
    receipt_base64: str = ""


class RegisterBirthDayPayload(BaseModel):
    birth_date: str = ""


class RegisterGooglePlayPaymentPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    json_: str = Field(default="", alias="json")


class RegisterPayload(BaseModel):
    name: Optional[str] = None


class RegisterTakeOverPasswordPayload(BaseModel):
    password: Optional[str] = None


class Restriction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    multi_live_restriction_finished_at: Optional[str] = None
    read_multi_live_restriction_dialog: Optional[bool] = None


class RollResult(BaseModel):
    roll_order: int = 0
    selected_slot: int = 0
    roulette_prize_master_id: int = 0


class Roulette(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    roulette_master_id: int = 0
    roll_count: int = 0


class RouletteEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    roulette_event_master_id: int = 0
    total_acquired_point: int = 0


class RouletteRollResult(BaseModel):
    roll_results: Optional[list[RollResult]] = None


class ScoreWithDateResult(BaseModel):
    score: int = 0
    date: str = ""


class SelectMusicCourseRandomMusicPayload(BaseModel):
    music_course_master_id: int = 0
    music_course_gauge_type: MusicCourseGaugeType = MusicCourseGaugeType.Normal


class SellAccessoryPayload(BaseModel):
    u_accessory_ids: Optional[list[int]] = None


class Sense(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    actor_id: int = 0
    cool_time: int = 0
    sense_type: SenseTypes = SenseTypes.Support
    acquirable_lights: list[SenseLightTypes] = Field(default_factory=list)
    pre_sense_effect: list[Effect] = Field(default_factory=list)
    sense_effect: SenseEffect = Field(default_factory=lambda: SenseEffect())
    poster_effect: list[Effect] = Field(default_factory=list)
    accessory_effect: list[Effect] = Field(default_factory=list)
    combination_sense_id: Optional[list[int]] = None
    sense_master_id: int = 0
    original_actor_id: int = 0


class SenseCoolTime(BaseModel):
    position: int = 0
    cool_time: int = 0


class SenseEffect(BaseModel):
    score_factor: int = 0
    principal: int = 0
    branch_condition: BranchConditionTypes = BranchConditionTypes.None_
    effect_branches: list[EffectBranch] = Field(default_factory=list)


class SenseScoreBlock(BaseModel):
    hash: int = 0
    score: int = 0
    life: int = 0
    time_event_second: int = 0
    sense_id: int = 0
    combo: int = 0


class SenseTimingEvent(BaseModel):
    timing_seconds: int = 0
    position: int = 0
    event: TimingEvent = Field(default_factory=lambda: TimingEvent())


class SetAlbumPublishingPayload(BaseModel):
    publishing: bool = False
    publish_page_number: int = 0


class SetLessonPartyPayload(BaseModel):
    slots: Optional[list[SetLessonPartySlotPayload]] = None


class SetLessonPartySlotPayload(BaseModel):
    order: int = 0
    character_id: int = 0


class SetPhotoTagPayload(BaseModel):
    photo_id: int = 0
    character_base_ids: Optional[list[int]] = None


class SetSelectedThingsPayload(BaseModel):
    gacha_thing_ids: Optional[list[int]] = None


class SpRate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    live_master_id: int = 0
    point: int = 0


class SpRateUpdateResult(BaseModel):
    best_ever: int = 0
    this_time: int = 0
    best_ever_total: int = 0
    this_time_total: int = 0


class SpecialEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    special_event_master_id: int = 0
    read_tips: bool = False


class Stamp(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    stamp_master_ids: Optional[list[int]] = None
    favorite_stamp_master_ids: Optional[list[int]] = None


class StarAct(BaseModel):
    score_factor: int = 0
    actor_id: int = 0
    branch_condition: BranchConditionTypes = BranchConditionTypes.None_
    effect_branches: list[EffectBranch] = Field(default_factory=list)


class StarActScoreBlock(BaseModel):
    hash: int = 0
    score: int = 0
    life: int = 0
    time_event_second: int = 0
    combo: int = 0


class StarPassStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    type: StarPassTypes = StarPassTypes.StarPass
    total_purchased_count: int = 0
    valid_until: str = ""


class StarPointResult(BaseModel):
    rank_before: int = 0
    rank_after: int = 0
    star_point_before: int = 0
    star_point_after: int = 0
    star_point_acquired: int = 0
    received_reward: Optional[list[ReceivedThing]] = None


class StartLessonPayload(BaseModel):
    character_base_master_id: int = 0
    live_master_id: int = 0


class StartLivePayload(BaseModel):
    party_id: int = 0
    live_master_id: int = 0
    audition_master_id: Optional[int] = None
    league_master_id: Optional[int] = None
    use_stamina: bool = False
    stamina_consumption_ratio: int = 0
    live_setting_master_id: int = 0
    is_auto_play: bool = False
    is_story_event_challenge: bool = False
    concert_stage_master_id: Optional[int] = None
    bonus_live_stage_master_id: Optional[int] = None
    music_course_detail_master_id: Optional[int] = None
    music_course_gauge_type: MusicCourseGaugeType = MusicCourseGaugeType.Normal
    ghost_live_master_id: Optional[int] = None
    trial_party_event_stage_master_id: Optional[int] = None


class StartMultiLivePayload(BaseModel):
    live_master_id: int = 0
    multi_live_id: int = 0
    use_stamina: bool = False
    stamina_consumption_ratio: int = 0
    party_id: Optional[int] = None


class StartMultiRoomLivePayload(BaseModel):
    hashed_multi_room_id: Optional[str] = None
    live_master_id: int = 0
    party_id: Optional[int] = None


class StartTournamentPayload(BaseModel):
    tournament_detail_master_id: int = 0
    party_id: int = 0
    stamina_consumption_ratio: int = 0


class StartTripleCastLivePayload(BaseModel):
    m_live_id: int = 0
    m_triple_cast_id: int = 0


class StartTripleCastLiveResult(BaseModel):
    live_units: Optional[list[LiveUnitWithOrder]] = None


class StoryEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    total_acquired_point: int = 0
    acquired_point_updated_date: str = ""
    last_rank: Optional[int] = None
    read_tips: bool = False
    login_days: int = 0


class StoryEventCampInfo(BaseModel):
    raw_ranking: Optional[RawRanking] = None
    camp1_total_point: int = 0
    camp2_total_point: int = 0


class StoryEventCircle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    current_point: int = 0
    high_score: int = 0
    circle_id: Optional[int] = None


class StoryEventCircleMission(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_circle_mission_master_id: int = 0
    current_count: int = 0


class StoryEventCircleMissionReward(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    story_event_circle_mission_reward_master_id: int = 0


class StoryEventHighScore(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    current_enhancement_point: int = 0
    total_acquired_enhancement_point: int = 0


class StoryEventHighScoreBuffSetting(BaseModel):
    story_event_high_score_buff_setting_master_id: int = 0
    current_level: int = 0


class StoryEventHighScoreParty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    high_score: int = 0
    rate_grade: AchievementRateGrades = AchievementRateGrades.None_
    difficulty: MusicDifficulties = MusicDifficulties.None_
    high_score_type: HighScoreTypes = HighScoreTypes.Normal
    live_setting_master_id: int = 0
    slots: Optional[list[StoryEventHighScorePartySlot]] = None
    leader_position: int = 0


class StoryEventHighScorePartySlot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_high_score_clear_party_id: int = 0
    position: int = 0
    character_master_id: int = 0
    character_level: int = 0
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status: Optional[Status] = None
    character_display_awakening_status: bool = False


class StoryEventMissionCircleProgress(BaseModel):
    story_event_circle_mission_master_id: int = 0
    current_count: int = 0


class StoryEventMissionCircleProgressResult(BaseModel):
    is_success: bool = False
    progresses: Optional[list[StoryEventMissionCircleProgress]] = None


class StoryEventPointExchangeResult(BaseModel):
    story_event_master_id: int = 0
    before_story_event_point_amount: int = 0
    after_coin_amount: int = 0


class SupportCompanyInformation(BaseModel):
    sirius: Optional[SupportCompanyLevelStatus] = None
    eden: Optional[SupportCompanyLevelStatus] = None
    gingaza: Optional[SupportCompanyLevelStatus] = None
    denki: Optional[SupportCompanyLevelStatus] = None


class SupportCompanyLevelLimitDetail(BaseModel):
    order: int = 0
    quantity: int = 0


class SupportCompanyLevelLimitPayload(BaseModel):
    company: Companies = Companies.None_
    coin_quantity: int = 0
    details: Optional[list[SupportCompanyLevelLimitDetail]] = None


class SupportCompanyLevelLimitStatus(BaseModel):
    current_coin_quantity: int = 0
    details: Optional[list[SupportCompanyLevelLimitStatusDetail]] = None


class SupportCompanyLevelLimitStatusDetail(BaseModel):
    order: int = 0
    current_quantity: int = 0


class SupportCompanyLevelStatus(BaseModel):
    level: int = 0
    current_support_point: int = 0
    last_level_upped_at: str = ""
    level_limit: int = 0
    level_limit_status: Optional[SupportCompanyLevelLimitStatus] = None


class TakeOverAccountPayload(BaseModel):
    linkage_code: Optional[str] = None
    password: Optional[str] = None


class TakeOverAccountResult(BaseModel):
    is_success: bool = False
    user_id: Optional[str] = None
    name: Optional[str] = None
    rank: int = 0
    login_token: Optional[str] = None


class TakeOverCodeResult(BaseModel):
    is_success: bool = False
    linkage_code: Optional[str] = None


class TheaterStory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    theater_story_master_id: int = 0


class TimeLimitedControl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    time_limited_control_master_id: int = 0
    expired_at: str = ""


class TimedConfirmationCode(BaseModel):
    confirmation_code: Optional[str] = None
    remaining_seconds: int = 0


class TimingEvent(BaseModel):
    total_sense_lights: list[SenseLightTypes] = Field(default_factory=list)
    grant_sense_lights: list[SenseLightTypes] = Field(default_factory=list)
    is_star_act: bool = False
    lost_lights: bool = False
    acquirable_lights: list[SenseLightTypes] = Field(default_factory=list)
    sense_ids: list[int] = Field(default_factory=list)
    sense_voice_ids: list[int] = Field(default_factory=list)
    sense_master_id: int = 0


class TotalPointEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    total_point_event_master_id: int = 0
    total_acquired_point: int = 0
    received_reward_order: int = 0


class TotalPointEventInformationResult(BaseModel):
    current_total_point: int = 0


class TotalPointEventRankingResult(BaseModel):
    raw_ranking: Optional[list[RawRankingWithLongPoint]] = None
    user_profiles: Optional[list[UserProfile]] = None


class TournamentDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    tournament_detail_master_id: int = 0
    best_unique_score: int = 0
    perfect_star: int = 0
    perfect: int = 0
    great: int = 0
    good: int = 0
    bad: int = 0
    miss: int = 0
    recorded_at: str = ""


class TournamentQualifying(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    tournament_qualifying_master_id: int = 0
    music_course_master_id: int = 0
    current_challenge_count: int = 0
    perfect_star: int = 0
    perfect: int = 0
    great: int = 0
    good: int = 0
    bad: int = 0
    miss: int = 0
    total_achievement_rate_percent_record: Optional[str] = None
    best_record_challenge_count: int = 0
    best_record_date: Optional[str] = None


class TournamentQualifyingInformationResult(BaseModel):
    entry_code: Optional[str] = None


class TournamentResult(BaseModel):
    best_ever_unique_score: int = 0
    this_time_unique_score: int = 0
    tournament_detail_master_id: int = 0


class TransitionTokenResult(BaseModel):
    token: Optional[str] = None


class TrialPartyEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_event_master_id: int = 0
    current_stage_order: int = 0
    is_completed: bool = False


class TrialPartyEventResult(BaseModel):
    rewards: Optional[list[ReceivedThing]] = None


class TrialPartyEventStage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_event_stage_master_id: int = 0
    is_cleared: bool = False


class TrialPartyEventStageParty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_event_stage_master_id: int = 0
    leader_position: int = 0


class TrialPartyEventStagePartySlot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_event_stage_party_id: int = 0
    position: int = 0
    trial_party_character_master_id: int = 0
    trial_party_poster_master_id: Optional[int] = None
    trial_party_accessory_master_id: Optional[int] = None


class TrialPartyEventStageResult(BaseModel):
    principal_gauge_value: int = 0


class TripleCastBasic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    star_enroll_count: int = 0
    dai_star_enroll_count: int = 0
    current_class_type: LeagueClassTypes = LeagueClassTypes.None_
    best_class_type: LeagueClassTypes = LeagueClassTypes.None_
    last_joined_triple_cast_season_master_id: Optional[int] = None
    party_order1: Optional[int] = None
    party_order2: Optional[int] = None
    party_order3: Optional[int] = None


class TripleCastGroup(BaseModel):
    triple_cast_master_id: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    class_order: int = 0


class TripleCastGroupMember(BaseModel):
    triple_cast_group_id: int = 0
    triple_cast_master_id: int = 0
    best_score: Optional[int] = None


class TripleCastHighScoreParty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    triple_cast_master_id: int = 0
    order: int = 0
    high_score: int = 0
    slots: Optional[list[TripleCastHighScorePartySlot]] = None
    acting_ability: int = 0
    leader_position: int = 0
    difficulty: MusicDifficulties = MusicDifficulties.None_


class TripleCastHighScorePartySlot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    triple_cast_high_score_party_id: int = 0
    position: int = 0
    character_master_id: int = 0
    character_level: int = 0
    poster_master_id: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status: Optional[Status] = None
    character_talent_stage: int = 0
    character_awakening_phase: int = 0
    character_display_awakening_status: bool = False


class TripleCastHistory(BaseModel):
    triple_cast_master_id: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    history_count: int = 0
    is_sended_reward: bool = False
    is_played: bool = False
    class_change_type: LeagueClassChangeTypes = LeagueClassChangeTypes.None_
    group_rank: int = 0
    global_rank: int = 0
    all_class_global_rank: int = 0


class TripleCastParty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    name: Optional[str] = None
    leader_position: int = 0


class TripleCastPartyAndRankingResult(BaseModel):
    rank: Optional[int] = None
    user_id: Optional[str] = None
    best_score: int = 0
    triple_cast_master_id: int = 0
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    difficulty: MusicDifficulties = MusicDifficulties.None_
    user_name: Optional[str] = None
    parties: Optional[list[TripleCastPartyResult]] = None


class TripleCastPartyResult(BaseModel):
    order: int = 0
    score: int = 0
    slots: Optional[list[LeaguePartySlotResult]] = None


class TripleCastPartyScore(BaseModel):
    order: int = 0
    score: int = 0


class TripleCastPartySlot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    party_id: int = 0
    position: int = 0
    character_id: int = 0
    poster_id: Optional[int] = None
    accessory_id: Optional[int] = None
    bonus_ability_enable_flags: BonusAbilityEnableFlags = BonusAbilityEnableFlags.None_


class TripleCastSeasonResult(BaseModel):
    triple_cast_season_master_id: int = 0
    dai_star_max_enroll_count: int = 0


class Trophy(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trophy_master_id: int = 0
    trophy_group_master_id: int = 0
    current_order: int = 0


class UpdateClearLampResult(BaseModel):
    clear_lamp: ClearLamps = ClearLamps.None_


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
    illust_character_master_id: int = 0
    display_awakening_status: bool = False
    home_character_display_type: HomeCharacterDisplayTypes = (
        HomeCharacterDisplayTypes.CharacterModel
    )
    login_bonus_character_base_master_id: Optional[int] = None
    login_bonus_spine_costume_master_id: Optional[int] = None


class UpdateLastViewedAtPayload(BaseModel):
    viewed_shop_category_types: ViewedShopCategoryTypes = (
        ViewedShopCategoryTypes.ExchangeShop
    )
    exchange_shop_master_id: Optional[int] = None


class UpdateTutorialPayload(BaseModel):
    tutorial_status: TutorialStatus = TutorialStatus.Start


class UrlResult(BaseModel):
    url: Optional[str] = None


class UseExperienceItemsPayload(BaseModel):
    item_master_id: int = 0
    quantity: int = 0


class UseStaminaRecoveryItem(BaseModel):
    item_master_id: int = 0
    quantity: int = 0


class UseStaminaRecoveryItemsPayload(BaseModel):
    items: Optional[list[UseStaminaRecoveryItem]] = None


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    player_rank: int = 0
    current_rank_point: int = 0
    current_stamina: int = 0
    max_stamina_restored_at: str = ""
    paid_jewel: int = 0
    free_jewel: int = 0
    coin: int = 0
    player_rank_limit: int = 0
    stamina_recover_times_with_jewel: int = 0
    circle_usage_restrictions_end_time: str = ""
    circle_id: Optional[str] = None
    game_start_at: str = ""
    hash_user_id: Optional[str] = None
    ban_level: BanLevels = BanLevels.Normal
    tutorial_status: TutorialStatus = TutorialStatus.Start
    monthly_payment: int = 0
    splash_last_displayed_at: str = ""
    is_caped_player_rank: bool = False
    require_caped_player_rank_announce: bool = False


class UserBlock(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    block_user_id: Optional[str] = None


class UserBonus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    experience_bonus: float = 0.0
    lesson_star_rank_bonus: float = 0.0


class UserPreference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    multi_party_id: int = 0
    birth_date: Optional[str] = None


class UserProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    introduction: Optional[str] = None
    main_u_character_id: int = 0
    m_nameplate_id: Optional[int] = None
    m_name_color_id: int = 0
    m_trophy_id1: Optional[int] = None
    m_trophy_id2: Optional[int] = None
    m_trophy_id3: Optional[int] = None
    player_rate: Optional[float] = (
        None  # own data always fills it; null when hidden for others
    )
    is_public_player_rate: bool = False
    league_class: LeagueClassTypes = LeagueClassTypes.None_
    total_sp_count: int = 0
    is_public_album_main_page: bool = False
    m_nameplate_detail_id: Optional[int] = None
    main_character_master_id: int = 0
    display_awakening_status: bool = False
    is_public_activity_log: bool = False
    name_base_color_master_id: int = 0
    icon_frame_master_id: int = 0
    home_skin_master_id: int = 0


class UserProfileDetail(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_m_character_id: int = 0
    main_character_level: int = 0
    character_display_awakening_status: bool = False
    icon_frame_master_id: int = 0
    name_color_master_id: int = 0
    name_base_color_master_id: int = 0
    nameplate_master_id: Optional[int] = None
    nameplate_detail_master_id: Optional[int] = None


class UserResult(BaseModel):
    user: Optional[User] = None


class ViewShopResult(BaseModel):
    converted_things: Optional[list[ConvertedThingResult]] = None


class ViewedShop(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    exchange_shop_master_id: Optional[int] = None
    last_viewed_at: str = ""
    viewed_shop_category: ViewedShopCategoryTypes = ViewedShopCategoryTypes.ExchangeShop


class Fault(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    error_code: str = Field(default="", alias="errorCode")
    message: Optional[str] = Field(default=None, alias="message")
    stack_trace: Optional[str] = Field(default=None, alias="stackTrace")


class DeletedDataObject(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type_name: str = Field(default="", alias="typeName")
    id_: int = Field(default=0, alias="id")


__all__ = [
    "AbilityVarietyUpPayload",
    "AcceptFriendRequest",
    "Accessory",
    "AccessoryAutoSell",
    "AccessoryAutoSellConvertThing",
    "AccessoryFavoritePayload",
    "AccountConnectPayload",
    "AccountDeletionResult",
    "AccountRegistResult",
    "AcquirableThing",
    "AcquirableThingsPayload",
    "ActorPortalCharacterPayload",
    "Album",
    "AlbumArrangingPayload",
    "AlbumPage",
    "AlbumPageResult",
    "AlbumPageSearchResult",
    "AlbumPhotoPayload",
    "AlbumPreset",
    "AlbumTheme",
    "AnotherNotation",
    "AuditionClear",
    "AuditionClearParty",
    "AuditionClearPartySlot",
    "AuditionClearedInformationParties",
    "AuditionClearedInformationResult",
    "AuthenticatePayload",
    "AuthenticateResult",
    "BannerPayload",
    "BaseScoreBlock",
    "Behaviour",
    "BlockListResult",
    "Bomb",
    "BonusLive",
    "BonusLiveResult",
    "BonusLiveStage",
    "BooleanResult",
    "BuffItemStatus",
    "BulkLevelUpPayload",
    "BulkReceivePayload",
    "CalculateLessonTimeEventPayload",
    "CalculateTimeEventPayload",
    "ChangeNamePayload",
    "ChangePhotoAbilityPayload",
    "Character",
    "CharacterBase",
    "CharacterBaseStarPointResult",
    "CharacterFavoritePayload",
    "CharacterLesson",
    "CharacterLessonSlot",
    "CharacterLineupResult",
    "CharacterMission",
    "CharacterPointEvent",
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
    "CircleEventMission",
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
    "ComebackCampaign",
    "Comic",
    "Component",
    "ConcertResult",
    "ConcertStage",
    "ConcoursDetailInformationResult",
    "ConcoursInfomationResult",
    "ConnectWithAccount",
    "ConnectWithPassword",
    "ConvertedThingResult",
    "Costume",
    "CostumeFavoritePayload",
    "CourseRankingResult",
    "CourseResult",
    "CreateCircleResult",
    "CreateMultiRoomPayload",
    "Currency",
    "DailyLesson",
    "DailyLimit",
    "DebugAlbumSimpleArrangingPayload",
    "DebugEditLeagueBasicPayload",
    "DebugLinkageCodeResult",
    "DebugModifyCharacterEnhanceInformationPayload",
    "DebugModifyPosterEnhanceInformationPayload",
    "DebugPrepareLeagueGroupUserPayload",
    "DebugUserIdResult",
    "Decimal",
    "Decoration",
    "Dictionary",
    "DonateSupportCompanyResult",
    "DonateSupportLevelLimitDetail",
    "DonateSupportLevelLimitPayload",
    "DugongRun",
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
    "Episode",
    "EpisodeResult",
    "EpisodeDetailResult",
    "EpisodeDetailCharacterMotionResult",
    "Event",
    "EventBoxGacha",
    "EventBoxGachaBoxThing",
    "EventBoxGachaRollResult",
    "EventCamp",
    "EventResult",
    "ExchangeLimit",
    "ExchangeShopThingPayload",
    "FavoriteCostume",
    "FavoriteStampOrderPayload",
    "FinishAnotherNotationLivePayload",
    "FinishLessonPayload",
    "FinishLivePayload",
    "FinishLiveResult",
    "FlashSaleReadStagePayload",
    "FlashSaleStage",
    "FriendAcceptResult",
    "FriendFavoritePayload",
    "FriendInvitation",
    "FriendInvitationMission",
    "FriendInvitationMissionPayload",
    "FriendInvitationUserInfoResult",
    "FriendListResult",
    "FriendRequest",
    "FriendRequestResult",
    "FriendResult",
    "FriendSearchResult",
    "Gacha",
    "GachaHistoryResult",
    "GachaInfoResult",
    "GachaLineupItemProbability",
    "GachaReRoll",
    "GachaRollLimit",
    "GachaRollResult",
    "GachaSelectedThing",
    "GachaSelectedThingsResult",
    "GachaThingResult",
    "GameHint",
    "GameHintMonoBehaviour",
    "GenerateLotteryResultPayload",
    "GeneratePhotoPayload",
    "GeneratePhotoResult",
    "GeneratePhotosPayload",
    "GhostLiveInfo",
    "GhostLiveResult",
    "GradualMissionGroup",
    "HighScoreBuff",
    "HighScoreBuffSetting",
    "HighScoreParty",
    "HighScorePartySlot",
    "HomeBGM",
    "HomeDisplayPreference",
    "HomeSkin",
    "IconFrame",
    "Inbox",
    "InboxReceiveResult",
    "InviteMultiRoomPayload",
    "Item",
    "JewelShop",
    "JoinMultiRoomPayload",
    "LeagueBasic",
    "LeagueGroup",
    "LeagueGroupMember",
    "LeagueHighScoreParty",
    "LeagueHighScorePartySlot",
    "LeagueHistory",
    "LeaguePartyAndRankingResult",
    "LeaguePartySlotResult",
    "LeagueReceiveResults",
    "LeagueResult",
    "LeagueSeasonResult",
    "LeagueTopMenuInformationResult",
    "LessonResult",
    "LevelUpPhotoPayload",
    "LevelUpPhotoResult",
    "Limit",
    "LinkCharacter",
    "Live",
    "LiveAchievement",
    "LiveDropCelling",
    "LiveDropLimit",
    "LiveDropThing",
    "LiveTimeEvent",
    "Actor",
    "LiveStatus",
    "LiveUnit",
    "LiveUnitWithOrder",
    "LoginBonusDetail",
    "LoginBonusResult",
    "LoginBonusSpineDetail",
    "LoginBonusSpineGroup",
    "LoginPassStatus",
    "LoginPayload",
    "LoginResult",
    "Lottery",
    "LotteryPriseResult",
    "MainCharacter",
    "Market",
    "MarketResult",
    "MarketThing",
    "MarshalByRefObject",
    "MasterDataManifest",
    "MatchingGhostLiveResult",
    "Mission",
    "MissionCleared",
    "MissionPass",
    "MissionPassRewardsResult",
    "MonoBehaviour",
    "MultiLiveAdditionalScoreBlock",
    "MultiLiveInformation",
    "MultiLiveRestriction",
    "MultiRoomBasic",
    "MultiRoomCreateResult",
    "MultiRoomDetailResult",
    "MultiRoomInformationResult",
    "MultiRoomInvitedResult",
    "MultiRoomJoinnedResult",
    "MultiRoomPartySlot",
    "MultiRoomRanking",
    "Music",
    "MusicBookmark",
    "MusicCourse",
    "MusicCourseRandomSelectResult",
    "MusicCourseRandomSelectResultDetail",
    "MusicCourseRanking",
    "MusicCourseRankingPayload",
    "MusicVideo",
    "MyCircleInformationResult",
    "NameBaseColor",
    "NameColor",
    "Nameplate",
    "Note",
    "NoteJudgePayload",
    "NoteResult",
    "Notification",
    "NotificationContentResult",
    "NotificationResult",
    "Party",
    "PartyInfo",
    "PartyPayload",
    "PartySlot",
    "PartySlotAccessoryPayload",
    "PartySlotCharacterPayload",
    "PartySlotDetail",
    "PartySlotPayload",
    "PartySlotPosterPayload",
    "PermanentMarketThing",
    "Photo",
    "PhotoAppearedCharacter",
    "PickupCharacterMission",
    "PlayerRankPointResult",
    "Poster",
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
    "RecyclableMonoBehaviour",
    "RegisterAppStorePaymentPayload",
    "RegisterBirthDayPayload",
    "RegisterGooglePlayPaymentPayload",
    "RegisterPayload",
    "RegisterTakeOverPasswordPayload",
    "Restriction",
    "RollResult",
    "Roulette",
    "RouletteEvent",
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
    "SpRate",
    "SpRateUpdateResult",
    "SpecialEvent",
    "Stamp",
    "StarAct",
    "StarActScoreBlock",
    "StarPassStatus",
    "StarPointResult",
    "StartLessonPayload",
    "StartLivePayload",
    "StartMultiLivePayload",
    "StartMultiRoomLivePayload",
    "StartTournamentPayload",
    "StartTripleCastLivePayload",
    "StartTripleCastLiveResult",
    "StoryEvent",
    "StoryEventCampInfo",
    "StoryEventCircle",
    "StoryEventCircleMission",
    "StoryEventCircleMissionReward",
    "StoryEventHighScore",
    "StoryEventHighScoreBuffSetting",
    "StoryEventHighScoreParty",
    "StoryEventHighScorePartySlot",
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
    "TheaterStory",
    "TimeLimitedControl",
    "TimedConfirmationCode",
    "TimingEvent",
    "TotalPointEvent",
    "TotalPointEventInformationResult",
    "TotalPointEventRankingResult",
    "TournamentDetail",
    "TournamentQualifying",
    "TournamentQualifyingInformationResult",
    "TournamentResult",
    "TransitionTokenResult",
    "TrialPartyEvent",
    "TrialPartyEventResult",
    "TrialPartyEventStage",
    "TrialPartyEventStageParty",
    "TrialPartyEventStagePartySlot",
    "TrialPartyEventStageResult",
    "TripleCastBasic",
    "TripleCastGroup",
    "TripleCastGroupMember",
    "TripleCastHighScoreParty",
    "TripleCastHighScorePartySlot",
    "TripleCastHistory",
    "TripleCastParty",
    "TripleCastPartyAndRankingResult",
    "TripleCastPartyResult",
    "TripleCastPartyScore",
    "TripleCastPartySlot",
    "TripleCastSeasonResult",
    "Trophy",
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
    "UserBlock",
    "UserBonus",
    "UserPreference",
    "UserProfile",
    "UserProfileDetail",
    "UserResult",
    "ViewShopResult",
    "ViewedShop",
    "Fault",
    "DeletedDataObject",
]

for _m in __all__:
    globals()[_m].model_rebuild()
