from db.query import SelectQuery
from models.database import (
    UserModel,
    UserProfileModel,
    UserPreferenceModel,
    HomeDisplayPreferenceModel,
    CharacterModel,
    CharacterBaseModel,
    PartyModel,
    PartySlotModel,
    CharacterMasterModel,
    CharacterBaseMasterModel,
    CharacterLevelMasterModel,
    PosterModel,
    AccessoryLevelPatternGroupMasterModel,
    AccessoryLevelPatternMasterModel,
    AccessoryMasterModel,
    EpisodeMasterModel,
    EpisodeRewardPackageMasterModel,
    LiveMasterModel,
    MusicMasterModel,
    SenseMasterModel,
    StoryMasterModel,
    PosterLevelPatternGroupMasterModel,
    PosterLevelPatternMasterModel,
    PosterMasterModel,
    LiveModel,
    MusicModel,
    AccessoryModel,
    ItemModel,
    AccessoryEffectMasterModel,
    CompanyMasterModel,
    EffectDurationGroupMasterModel,
    EffectMasterModel,
    ItemMasterModel,
    RandomEffectGroupMasterModel,
    RewardRuleMasterModel,
    SenseEffectMasterModel,
    TrophyGroupMasterModel,
    TrophyMasterModel,
    CharacterLessonModel,
    DailyLessonModel,
    InboxModel,
    BombModel,
    CostumeModel,
    NameColorModel,
    NameplateModel,
    NoteModel,
    StampModel,
    MissionModel,
    AuditionMasterModel,
    BombMasterModel,
    CharacterStarRankMasterModel,
    CharacterStarRankRewardGroupMasterModel,
    CostumeMasterModel,
    HomeCharacterVoiceMasterModel,
    NameColorMasterModel,
    NameplateMasterModel,
    NoteMasterModel,
    SpotConversationMasterModel,
    StampMasterModel,
    CharacterLessonSlotModel,
    TrophyModel,
    MarketModel,
    ViewedShopModel,
    GameHintModel,
    UserBonusModel,
    AuditionPhaseMasterModel,
    AuditionRewardPackageMasterModel,
    CampaignMasterModel,
    CharacterAwakeningItemMasterModel,
    CharacterBloomBonusGroupMasterModel,
    CharacterBloomItemMasterModel,
    CharacterExperienceItemMasterModel,
    CharacterMissionMasterModel,
    CharacterMissionStageMasterModel,
    CharacterPieceMasterModel,
    CharacterSenseEnhanceItemGroupMasterModel,
    CostumeWearableCharacterGroupMasterModel,
    ExchangeShopMasterModel,
    LiveSettingMasterModel,
    MissionMasterModel,
    MusicVocalVersionMasterModel,
    PosterReleaseItemGroupMasterModel,
    PosterReleaseItemMasterModel,
    PosterStoryMasterModel,
    StarRankRewardMasterModel,
    AuditionClearModel,
    SpRateModel,
    NotificationModel,
    EpisodeModel,
    CharacterMissionModel,
    MissionPassModel,
    MissionPassDetailMasterModel,
    MissionPassMasterModel,
    LeagueBasicModel,
    StoryEventModel,
    ExchangeLimitModel,
    LeagueGroupModel,
    LeagueGroupMemberModel,
    LeagueHistoryModel,
    JewelShopModel,
    DailyLimitModel,
    LeagueHighScorePartyModel,
    LeagueHighScorePartySlotModel,
    StoryEventCircleModel,
    StoryEventCircleMissionModel,
    StoryEventCircleMissionRewardModel,
    StoryEventHighScoreBuffSettingModel,
    StoryEventHighScorePartyModel,
    StoryEventHighScorePartySlotModel,
    ConnectWithAccountModel,
    ConnectWithPasswordModel,
    TournamentDetailModel,
    GradualMissionGroupModel,
    PhotoModel,
    AlbumModel,
    AlbumPageModel,
    StarPassStatusModel,
    LoginPassStatusModel,
    CurrencyModel,
    DecorationModel,
    LiveAchievementModel,
    MusicVideoModel,
    TheaterStoryModel,
    LiveDropCellingModel,
    StoryEventHighScoreModel,
    ComicModel,
    ComebackCampaignModel,
    ConcertStageModel,
    LimitModel,
    GachaSelectedThingModel,
    TotalPointEventModel,
    EventBoxGachaModel,
    EventBoxGachaBoxThingModel,
    SpecialEventModel,
    CharacterPointEventModel,
    AnotherNotationModel,
    MusicBookmarkModel,
    LiveDropLimitModel,
    RestrictionModel,
    PermanentMarketThingModel,
    TimeLimitedControlModel,
    FlashSaleStageModel,
    AlbumThemeModel,
    CircleEventMissionModel,
    PickupCharacterMissionModel,
    LeagueSeasonResultModel,
    EventModel,
    BonusLiveModel,
    BonusLiveStageModel,
    RouletteEventModel,
    RouletteModel,
    HomeBGMModel,
    LinkCharacterModel,
    MusicCourseModel,
    TournamentQualifyingModel,
    LotteryModel,
    TripleCastPartyModel,
    TripleCastPartySlotModel,
    TripleCastBasicModel,
    TripleCastGroupModel,
    TripleCastGroupMemberModel,
    TripleCastHighScorePartyModel,
    TripleCastHighScorePartySlotModel,
    TripleCastSeasonResultModel,
    AlbumPresetModel,
    GachaModel,
    TripleCastHistoryModel,
    DugongRunModel,
    MusicCourseRankingModel,
    FriendInvitationModel,
    FriendInvitationMissionModel,
    NameBaseColorModel,
    IconFrameModel,
    GachaReRollModel,
    TrialPartyEventModel,
    TrialPartyEventStageModel,
    TrialPartyEventStagePartyModel,
    TrialPartyEventStagePartySlotModel,
    UserBlockModel,
    HomeSkinModel,
    AccessoryAutoSellModel,
    FavoriteCostumeModel,
    BuffItemStatusModel,
    MultiRoomBasicModel,
    EventCampModel,
)


def get_users(user_id: int) -> SelectQuery[UserModel]:
    return SelectQuery(UserModel, 'SELECT * FROM "user" WHERE "userId" = $1', user_id)


def get_user_profiles(user_id: int) -> SelectQuery[UserProfileModel]:
    return SelectQuery(
        UserProfileModel, 'SELECT * FROM "user_profile" WHERE "userId" = $1', user_id
    )


def get_user_preferences(user_id: int) -> SelectQuery[UserPreferenceModel]:
    return SelectQuery(
        UserPreferenceModel,
        'SELECT * FROM "user_preference" WHERE "userId" = $1',
        user_id,
    )


def get_home_display_preferences(
    user_id: int,
) -> SelectQuery[HomeDisplayPreferenceModel]:
    return SelectQuery(
        HomeDisplayPreferenceModel,
        'SELECT * FROM "home_display_preference" WHERE "userId" = $1',
        user_id,
    )


def get_characters(user_id: int) -> SelectQuery[CharacterModel]:
    return SelectQuery(
        CharacterModel, 'SELECT * FROM "character" WHERE "userId" = $1', user_id
    )


def get_character_bases(user_id: int) -> SelectQuery[CharacterBaseModel]:
    return SelectQuery(
        CharacterBaseModel,
        'SELECT * FROM "character_base" WHERE "userId" = $1',
        user_id,
    )


def get_partys(user_id: int) -> SelectQuery[PartyModel]:
    return SelectQuery(PartyModel, 'SELECT * FROM "party" WHERE "userId" = $1', user_id)


def get_party_slots(user_id: int) -> SelectQuery[PartySlotModel]:
    return SelectQuery(
        PartySlotModel, 'SELECT * FROM "party_slot" WHERE "userId" = $1', user_id
    )


def get_character_masters(user_id: int) -> SelectQuery[CharacterMasterModel]:
    return SelectQuery(
        CharacterMasterModel,
        'SELECT * FROM "character_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_base_masters(user_id: int) -> SelectQuery[CharacterBaseMasterModel]:
    return SelectQuery(
        CharacterBaseMasterModel,
        'SELECT * FROM "character_base_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_level_masters(user_id: int) -> SelectQuery[CharacterLevelMasterModel]:
    return SelectQuery(
        CharacterLevelMasterModel,
        'SELECT * FROM "character_level_master" WHERE "userId" = $1',
        user_id,
    )


def get_posters(user_id: int) -> SelectQuery[PosterModel]:
    return SelectQuery(
        PosterModel, 'SELECT * FROM "poster" WHERE "userId" = $1', user_id
    )


def get_accessory_level_pattern_group_masters(
    user_id: int,
) -> SelectQuery[AccessoryLevelPatternGroupMasterModel]:
    return SelectQuery(
        AccessoryLevelPatternGroupMasterModel,
        'SELECT * FROM "accessory_level_pattern_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_accessory_level_pattern_masters(
    user_id: int,
) -> SelectQuery[AccessoryLevelPatternMasterModel]:
    return SelectQuery(
        AccessoryLevelPatternMasterModel,
        'SELECT * FROM "accessory_level_pattern_master" WHERE "userId" = $1',
        user_id,
    )


def get_accessory_masters(user_id: int) -> SelectQuery[AccessoryMasterModel]:
    return SelectQuery(
        AccessoryMasterModel,
        'SELECT * FROM "accessory_master" WHERE "userId" = $1',
        user_id,
    )


def get_episode_masters(user_id: int) -> SelectQuery[EpisodeMasterModel]:
    return SelectQuery(
        EpisodeMasterModel,
        'SELECT * FROM "episode_master" WHERE "userId" = $1',
        user_id,
    )


def get_episode_reward_package_masters(
    user_id: int,
) -> SelectQuery[EpisodeRewardPackageMasterModel]:
    return SelectQuery(
        EpisodeRewardPackageMasterModel,
        'SELECT * FROM "episode_reward_package_master" WHERE "userId" = $1',
        user_id,
    )


def get_live_masters(user_id: int) -> SelectQuery[LiveMasterModel]:
    return SelectQuery(
        LiveMasterModel, 'SELECT * FROM "live_master" WHERE "userId" = $1', user_id
    )


def get_music_masters(user_id: int) -> SelectQuery[MusicMasterModel]:
    return SelectQuery(
        MusicMasterModel, 'SELECT * FROM "music_master" WHERE "userId" = $1', user_id
    )


def get_sense_masters(user_id: int) -> SelectQuery[SenseMasterModel]:
    return SelectQuery(
        SenseMasterModel, 'SELECT * FROM "sense_master" WHERE "userId" = $1', user_id
    )


def get_story_masters(user_id: int) -> SelectQuery[StoryMasterModel]:
    return SelectQuery(
        StoryMasterModel, 'SELECT * FROM "story_master" WHERE "userId" = $1', user_id
    )


def get_poster_level_pattern_group_masters(
    user_id: int,
) -> SelectQuery[PosterLevelPatternGroupMasterModel]:
    return SelectQuery(
        PosterLevelPatternGroupMasterModel,
        'SELECT * FROM "poster_level_pattern_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_poster_level_pattern_masters(
    user_id: int,
) -> SelectQuery[PosterLevelPatternMasterModel]:
    return SelectQuery(
        PosterLevelPatternMasterModel,
        'SELECT * FROM "poster_level_pattern_master" WHERE "userId" = $1',
        user_id,
    )


def get_poster_masters(user_id: int) -> SelectQuery[PosterMasterModel]:
    return SelectQuery(
        PosterMasterModel, 'SELECT * FROM "poster_master" WHERE "userId" = $1', user_id
    )


def get_lives(user_id: int) -> SelectQuery[LiveModel]:
    return SelectQuery(LiveModel, 'SELECT * FROM "live" WHERE "userId" = $1', user_id)


def get_musics(user_id: int) -> SelectQuery[MusicModel]:
    return SelectQuery(MusicModel, 'SELECT * FROM "music" WHERE "userId" = $1', user_id)


def get_accessorys(user_id: int) -> SelectQuery[AccessoryModel]:
    return SelectQuery(
        AccessoryModel, 'SELECT * FROM "accessory" WHERE "userId" = $1', user_id
    )


def get_items(user_id: int) -> SelectQuery[ItemModel]:
    return SelectQuery(ItemModel, 'SELECT * FROM "item" WHERE "userId" = $1', user_id)


def get_accessory_effect_masters(
    user_id: int,
) -> SelectQuery[AccessoryEffectMasterModel]:
    return SelectQuery(
        AccessoryEffectMasterModel,
        'SELECT * FROM "accessory_effect_master" WHERE "userId" = $1',
        user_id,
    )


def get_company_masters(user_id: int) -> SelectQuery[CompanyMasterModel]:
    return SelectQuery(
        CompanyMasterModel,
        'SELECT * FROM "company_master" WHERE "userId" = $1',
        user_id,
    )


def get_effect_duration_group_masters(
    user_id: int,
) -> SelectQuery[EffectDurationGroupMasterModel]:
    return SelectQuery(
        EffectDurationGroupMasterModel,
        'SELECT * FROM "effect_duration_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_effect_masters(user_id: int) -> SelectQuery[EffectMasterModel]:
    return SelectQuery(
        EffectMasterModel, 'SELECT * FROM "effect_master" WHERE "userId" = $1', user_id
    )


def get_item_masters(user_id: int) -> SelectQuery[ItemMasterModel]:
    return SelectQuery(
        ItemMasterModel, 'SELECT * FROM "item_master" WHERE "userId" = $1', user_id
    )


def get_random_effect_group_masters(
    user_id: int,
) -> SelectQuery[RandomEffectGroupMasterModel]:
    return SelectQuery(
        RandomEffectGroupMasterModel,
        'SELECT * FROM "random_effect_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_reward_rule_masters(user_id: int) -> SelectQuery[RewardRuleMasterModel]:
    return SelectQuery(
        RewardRuleMasterModel,
        'SELECT * FROM "reward_rule_master" WHERE "userId" = $1',
        user_id,
    )


def get_sense_effect_masters(user_id: int) -> SelectQuery[SenseEffectMasterModel]:
    return SelectQuery(
        SenseEffectMasterModel,
        'SELECT * FROM "sense_effect_master" WHERE "userId" = $1',
        user_id,
    )


def get_trophy_group_masters(user_id: int) -> SelectQuery[TrophyGroupMasterModel]:
    return SelectQuery(
        TrophyGroupMasterModel,
        'SELECT * FROM "trophy_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_trophy_masters(user_id: int) -> SelectQuery[TrophyMasterModel]:
    return SelectQuery(
        TrophyMasterModel, 'SELECT * FROM "trophy_master" WHERE "userId" = $1', user_id
    )


def get_character_lessons(user_id: int) -> SelectQuery[CharacterLessonModel]:
    return SelectQuery(
        CharacterLessonModel,
        'SELECT * FROM "character_lesson" WHERE "userId" = $1',
        user_id,
    )


def get_daily_lessons(user_id: int) -> SelectQuery[DailyLessonModel]:
    return SelectQuery(
        DailyLessonModel, 'SELECT * FROM "daily_lesson" WHERE "userId" = $1', user_id
    )


def get_inboxs(user_id: int) -> SelectQuery[InboxModel]:
    return SelectQuery(InboxModel, 'SELECT * FROM "inbox" WHERE "userId" = $1', user_id)


def get_unchecked_inboxs(user_id: int) -> SelectQuery[InboxModel]:
    """Inbox packages not yet surfaced by CheckPackages (its new-package diff)."""
    return SelectQuery(
        InboxModel,
        'SELECT * FROM "inbox" WHERE "userId" = $1 AND "checked" = false',
        user_id,
    )


def get_bombs(user_id: int) -> SelectQuery[BombModel]:
    return SelectQuery(BombModel, 'SELECT * FROM "bomb" WHERE "userId" = $1', user_id)


def get_costumes(user_id: int) -> SelectQuery[CostumeModel]:
    return SelectQuery(
        CostumeModel, 'SELECT * FROM "costume" WHERE "userId" = $1', user_id
    )


def get_name_colors(user_id: int) -> SelectQuery[NameColorModel]:
    return SelectQuery(
        NameColorModel, 'SELECT * FROM "name_color" WHERE "userId" = $1', user_id
    )


def get_nameplates(user_id: int) -> SelectQuery[NameplateModel]:
    return SelectQuery(
        NameplateModel, 'SELECT * FROM "nameplate" WHERE "userId" = $1', user_id
    )


def get_notes(user_id: int) -> SelectQuery[NoteModel]:
    return SelectQuery(NoteModel, 'SELECT * FROM "note" WHERE "userId" = $1', user_id)


def get_stamps(user_id: int) -> SelectQuery[StampModel]:
    return SelectQuery(StampModel, 'SELECT * FROM "stamp" WHERE "userId" = $1', user_id)


def get_missions(user_id: int) -> SelectQuery[MissionModel]:
    return SelectQuery(
        MissionModel, 'SELECT * FROM "mission" WHERE "userId" = $1', user_id
    )


def get_audition_masters(user_id: int) -> SelectQuery[AuditionMasterModel]:
    return SelectQuery(
        AuditionMasterModel,
        'SELECT * FROM "audition_master" WHERE "userId" = $1',
        user_id,
    )


def get_bomb_masters(user_id: int) -> SelectQuery[BombMasterModel]:
    return SelectQuery(
        BombMasterModel, 'SELECT * FROM "bomb_master" WHERE "userId" = $1', user_id
    )


def get_character_star_rank_masters(
    user_id: int,
) -> SelectQuery[CharacterStarRankMasterModel]:
    return SelectQuery(
        CharacterStarRankMasterModel,
        'SELECT * FROM "character_star_rank_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_star_rank_reward_group_masters(
    user_id: int,
) -> SelectQuery[CharacterStarRankRewardGroupMasterModel]:
    return SelectQuery(
        CharacterStarRankRewardGroupMasterModel,
        'SELECT * FROM "character_star_rank_reward_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_costume_masters(user_id: int) -> SelectQuery[CostumeMasterModel]:
    return SelectQuery(
        CostumeMasterModel,
        'SELECT * FROM "costume_master" WHERE "userId" = $1',
        user_id,
    )


def get_home_character_voice_masters(
    user_id: int,
) -> SelectQuery[HomeCharacterVoiceMasterModel]:
    return SelectQuery(
        HomeCharacterVoiceMasterModel,
        'SELECT * FROM "home_character_voice_master" WHERE "userId" = $1',
        user_id,
    )


def get_name_color_masters(user_id: int) -> SelectQuery[NameColorMasterModel]:
    return SelectQuery(
        NameColorMasterModel,
        'SELECT * FROM "name_color_master" WHERE "userId" = $1',
        user_id,
    )


def get_nameplate_masters(user_id: int) -> SelectQuery[NameplateMasterModel]:
    return SelectQuery(
        NameplateMasterModel,
        'SELECT * FROM "nameplate_master" WHERE "userId" = $1',
        user_id,
    )


def get_note_masters(user_id: int) -> SelectQuery[NoteMasterModel]:
    return SelectQuery(
        NoteMasterModel, 'SELECT * FROM "note_master" WHERE "userId" = $1', user_id
    )


def get_spot_conversation_masters(
    user_id: int,
) -> SelectQuery[SpotConversationMasterModel]:
    return SelectQuery(
        SpotConversationMasterModel,
        'SELECT * FROM "spot_conversation_master" WHERE "userId" = $1',
        user_id,
    )


def get_stamp_masters(user_id: int) -> SelectQuery[StampMasterModel]:
    return SelectQuery(
        StampMasterModel, 'SELECT * FROM "stamp_master" WHERE "userId" = $1', user_id
    )


def get_character_lesson_slots(user_id: int) -> SelectQuery[CharacterLessonSlotModel]:
    return SelectQuery(
        CharacterLessonSlotModel,
        'SELECT * FROM "character_lesson_slot" WHERE "userId" = $1',
        user_id,
    )


def get_trophys(user_id: int) -> SelectQuery[TrophyModel]:
    return SelectQuery(
        TrophyModel, 'SELECT * FROM "trophy" WHERE "userId" = $1', user_id
    )


def get_markets(user_id: int) -> SelectQuery[MarketModel]:
    return SelectQuery(
        MarketModel, 'SELECT * FROM "market" WHERE "userId" = $1', user_id
    )


def get_viewed_shops(user_id: int) -> SelectQuery[ViewedShopModel]:
    return SelectQuery(
        ViewedShopModel, 'SELECT * FROM "viewed_shop" WHERE "userId" = $1', user_id
    )


def get_game_hints(user_id: int) -> SelectQuery[GameHintModel]:
    return SelectQuery(
        GameHintModel, 'SELECT * FROM "game_hint" WHERE "userId" = $1', user_id
    )


def get_user_bonuss(user_id: int) -> SelectQuery[UserBonusModel]:
    return SelectQuery(
        UserBonusModel, 'SELECT * FROM "user_bonus" WHERE "userId" = $1', user_id
    )


def get_audition_phase_masters(user_id: int) -> SelectQuery[AuditionPhaseMasterModel]:
    return SelectQuery(
        AuditionPhaseMasterModel,
        'SELECT * FROM "audition_phase_master" WHERE "userId" = $1',
        user_id,
    )


def get_audition_reward_package_masters(
    user_id: int,
) -> SelectQuery[AuditionRewardPackageMasterModel]:
    return SelectQuery(
        AuditionRewardPackageMasterModel,
        'SELECT * FROM "audition_reward_package_master" WHERE "userId" = $1',
        user_id,
    )


def get_campaign_masters(user_id: int) -> SelectQuery[CampaignMasterModel]:
    return SelectQuery(
        CampaignMasterModel,
        'SELECT * FROM "campaign_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_awakening_item_masters(
    user_id: int,
) -> SelectQuery[CharacterAwakeningItemMasterModel]:
    return SelectQuery(
        CharacterAwakeningItemMasterModel,
        'SELECT * FROM "character_awakening_item_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_bloom_bonus_group_masters(
    user_id: int,
) -> SelectQuery[CharacterBloomBonusGroupMasterModel]:
    return SelectQuery(
        CharacterBloomBonusGroupMasterModel,
        'SELECT * FROM "character_bloom_bonus_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_bloom_item_masters(
    user_id: int,
) -> SelectQuery[CharacterBloomItemMasterModel]:
    return SelectQuery(
        CharacterBloomItemMasterModel,
        'SELECT * FROM "character_bloom_item_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_experience_item_masters(
    user_id: int,
) -> SelectQuery[CharacterExperienceItemMasterModel]:
    return SelectQuery(
        CharacterExperienceItemMasterModel,
        'SELECT * FROM "character_experience_item_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_mission_masters(
    user_id: int,
) -> SelectQuery[CharacterMissionMasterModel]:
    return SelectQuery(
        CharacterMissionMasterModel,
        'SELECT * FROM "character_mission_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_mission_stage_masters(
    user_id: int,
) -> SelectQuery[CharacterMissionStageMasterModel]:
    return SelectQuery(
        CharacterMissionStageMasterModel,
        'SELECT * FROM "character_mission_stage_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_piece_masters(user_id: int) -> SelectQuery[CharacterPieceMasterModel]:
    return SelectQuery(
        CharacterPieceMasterModel,
        'SELECT * FROM "character_piece_master" WHERE "userId" = $1',
        user_id,
    )


def get_character_sense_enhance_item_group_masters(
    user_id: int,
) -> SelectQuery[CharacterSenseEnhanceItemGroupMasterModel]:
    return SelectQuery(
        CharacterSenseEnhanceItemGroupMasterModel,
        'SELECT * FROM "character_sense_enhance_item_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_costume_wearable_character_group_masters(
    user_id: int,
) -> SelectQuery[CostumeWearableCharacterGroupMasterModel]:
    return SelectQuery(
        CostumeWearableCharacterGroupMasterModel,
        'SELECT * FROM "costume_wearable_character_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_exchange_shop_masters(user_id: int) -> SelectQuery[ExchangeShopMasterModel]:
    return SelectQuery(
        ExchangeShopMasterModel,
        'SELECT * FROM "exchange_shop_master" WHERE "userId" = $1',
        user_id,
    )


def get_live_setting_masters(user_id: int) -> SelectQuery[LiveSettingMasterModel]:
    return SelectQuery(
        LiveSettingMasterModel,
        'SELECT * FROM "live_setting_master" WHERE "userId" = $1',
        user_id,
    )


def get_mission_masters(user_id: int) -> SelectQuery[MissionMasterModel]:
    return SelectQuery(
        MissionMasterModel,
        'SELECT * FROM "mission_master" WHERE "userId" = $1',
        user_id,
    )


def get_music_vocal_version_masters(
    user_id: int,
) -> SelectQuery[MusicVocalVersionMasterModel]:
    return SelectQuery(
        MusicVocalVersionMasterModel,
        'SELECT * FROM "music_vocal_version_master" WHERE "userId" = $1',
        user_id,
    )


def get_poster_release_item_group_masters(
    user_id: int,
) -> SelectQuery[PosterReleaseItemGroupMasterModel]:
    return SelectQuery(
        PosterReleaseItemGroupMasterModel,
        'SELECT * FROM "poster_release_item_group_master" WHERE "userId" = $1',
        user_id,
    )


def get_poster_release_item_masters(
    user_id: int,
) -> SelectQuery[PosterReleaseItemMasterModel]:
    return SelectQuery(
        PosterReleaseItemMasterModel,
        'SELECT * FROM "poster_release_item_master" WHERE "userId" = $1',
        user_id,
    )


def get_poster_story_masters(user_id: int) -> SelectQuery[PosterStoryMasterModel]:
    return SelectQuery(
        PosterStoryMasterModel,
        'SELECT * FROM "poster_story_master" WHERE "userId" = $1',
        user_id,
    )


def get_star_rank_reward_masters(
    user_id: int,
) -> SelectQuery[StarRankRewardMasterModel]:
    return SelectQuery(
        StarRankRewardMasterModel,
        'SELECT * FROM "star_rank_reward_master" WHERE "userId" = $1',
        user_id,
    )


def get_audition_clears(user_id: int) -> SelectQuery[AuditionClearModel]:
    return SelectQuery(
        AuditionClearModel,
        'SELECT * FROM "audition_clear" WHERE "userId" = $1',
        user_id,
    )


def get_sp_rates(user_id: int) -> SelectQuery[SpRateModel]:
    return SelectQuery(
        SpRateModel, 'SELECT * FROM "sp_rate" WHERE "userId" = $1', user_id
    )


def get_notifications(user_id: int) -> SelectQuery[NotificationModel]:
    return SelectQuery(
        NotificationModel, 'SELECT * FROM "notification" WHERE "userId" = $1', user_id
    )


def get_episodes(user_id: int) -> SelectQuery[EpisodeModel]:
    return SelectQuery(
        EpisodeModel, 'SELECT * FROM "episode" WHERE "userId" = $1', user_id
    )


def get_character_missions(user_id: int) -> SelectQuery[CharacterMissionModel]:
    return SelectQuery(
        CharacterMissionModel,
        'SELECT * FROM "character_mission" WHERE "userId" = $1',
        user_id,
    )


def get_mission_passs(user_id: int) -> SelectQuery[MissionPassModel]:
    return SelectQuery(
        MissionPassModel, 'SELECT * FROM "mission_pass" WHERE "userId" = $1', user_id
    )


def get_mission_pass_detail_masters(
    user_id: int,
) -> SelectQuery[MissionPassDetailMasterModel]:
    return SelectQuery(
        MissionPassDetailMasterModel,
        'SELECT * FROM "mission_pass_detail_master" WHERE "userId" = $1',
        user_id,
    )


def get_mission_pass_masters(user_id: int) -> SelectQuery[MissionPassMasterModel]:
    return SelectQuery(
        MissionPassMasterModel,
        'SELECT * FROM "mission_pass_master" WHERE "userId" = $1',
        user_id,
    )


def get_league_basics(user_id: int) -> SelectQuery[LeagueBasicModel]:
    return SelectQuery(
        LeagueBasicModel, 'SELECT * FROM "league_basic" WHERE "userId" = $1', user_id
    )


def get_story_events(user_id: int) -> SelectQuery[StoryEventModel]:
    return SelectQuery(
        StoryEventModel, 'SELECT * FROM "story_event" WHERE "userId" = $1', user_id
    )


def get_exchange_limits(user_id: int) -> SelectQuery[ExchangeLimitModel]:
    return SelectQuery(
        ExchangeLimitModel,
        'SELECT * FROM "exchange_limit" WHERE "userId" = $1',
        user_id,
    )


def get_league_groups(user_id: int) -> SelectQuery[LeagueGroupModel]:
    return SelectQuery(
        LeagueGroupModel, 'SELECT * FROM "league_group" WHERE "userId" = $1', user_id
    )


def get_league_group_members(user_id: int) -> SelectQuery[LeagueGroupMemberModel]:
    return SelectQuery(
        LeagueGroupMemberModel,
        'SELECT * FROM "league_group_member" WHERE "userId" = $1',
        user_id,
    )


def get_league_historys(user_id: int) -> SelectQuery[LeagueHistoryModel]:
    return SelectQuery(
        LeagueHistoryModel,
        'SELECT * FROM "league_history" WHERE "userId" = $1',
        user_id,
    )


def get_jewel_shops(user_id: int) -> SelectQuery[JewelShopModel]:
    return SelectQuery(
        JewelShopModel, 'SELECT * FROM "jewel_shop" WHERE "userId" = $1', user_id
    )


def get_daily_limits(user_id: int) -> SelectQuery[DailyLimitModel]:
    return SelectQuery(
        DailyLimitModel, 'SELECT * FROM "daily_limit" WHERE "userId" = $1', user_id
    )


def get_league_high_score_partys(
    user_id: int,
) -> SelectQuery[LeagueHighScorePartyModel]:
    return SelectQuery(
        LeagueHighScorePartyModel,
        'SELECT * FROM "league_high_score_party" WHERE "userId" = $1',
        user_id,
    )


def get_league_high_score_party_slots(
    user_id: int,
) -> SelectQuery[LeagueHighScorePartySlotModel]:
    return SelectQuery(
        LeagueHighScorePartySlotModel,
        'SELECT * FROM "league_high_score_party_slot" WHERE "userId" = $1',
        user_id,
    )


def get_story_event_circles(user_id: int) -> SelectQuery[StoryEventCircleModel]:
    return SelectQuery(
        StoryEventCircleModel,
        'SELECT * FROM "story_event_circle" WHERE "userId" = $1',
        user_id,
    )


def get_story_event_circle_missions(
    user_id: int,
) -> SelectQuery[StoryEventCircleMissionModel]:
    return SelectQuery(
        StoryEventCircleMissionModel,
        'SELECT * FROM "story_event_circle_mission" WHERE "userId" = $1',
        user_id,
    )


def get_story_event_circle_mission_rewards(
    user_id: int,
) -> SelectQuery[StoryEventCircleMissionRewardModel]:
    return SelectQuery(
        StoryEventCircleMissionRewardModel,
        'SELECT * FROM "story_event_circle_mission_reward" WHERE "userId" = $1',
        user_id,
    )


def get_story_event_high_score_buff_settings(
    user_id: int,
) -> SelectQuery[StoryEventHighScoreBuffSettingModel]:
    return SelectQuery(
        StoryEventHighScoreBuffSettingModel,
        'SELECT * FROM "story_event_high_score_buff_setting" WHERE "userId" = $1',
        user_id,
    )


def get_story_event_high_score_partys(
    user_id: int,
) -> SelectQuery[StoryEventHighScorePartyModel]:
    return SelectQuery(
        StoryEventHighScorePartyModel,
        'SELECT * FROM "story_event_high_score_party" WHERE "userId" = $1',
        user_id,
    )


def get_story_event_high_score_party_slots(
    user_id: int,
) -> SelectQuery[StoryEventHighScorePartySlotModel]:
    return SelectQuery(
        StoryEventHighScorePartySlotModel,
        'SELECT * FROM "story_event_high_score_party_slot" WHERE "userId" = $1',
        user_id,
    )


def get_connect_with_accounts(user_id: int) -> SelectQuery[ConnectWithAccountModel]:
    return SelectQuery(
        ConnectWithAccountModel,
        'SELECT * FROM "connect_with_account" WHERE "userId" = $1',
        user_id,
    )


def get_connect_with_passwords(user_id: int) -> SelectQuery[ConnectWithPasswordModel]:
    return SelectQuery(
        ConnectWithPasswordModel,
        'SELECT * FROM "connect_with_password" WHERE "userId" = $1',
        user_id,
    )


def get_tournament_details(user_id: int) -> SelectQuery[TournamentDetailModel]:
    return SelectQuery(
        TournamentDetailModel,
        'SELECT * FROM "tournament_detail" WHERE "userId" = $1',
        user_id,
    )


def get_gradual_mission_groups(user_id: int) -> SelectQuery[GradualMissionGroupModel]:
    return SelectQuery(
        GradualMissionGroupModel,
        'SELECT * FROM "gradual_mission_group" WHERE "userId" = $1',
        user_id,
    )


def get_photos(user_id: int) -> SelectQuery[PhotoModel]:
    return SelectQuery(PhotoModel, 'SELECT * FROM "photo" WHERE "userId" = $1', user_id)


def get_albums(user_id: int) -> SelectQuery[AlbumModel]:
    return SelectQuery(AlbumModel, 'SELECT * FROM "album" WHERE "userId" = $1', user_id)


def get_album_pages(user_id: int) -> SelectQuery[AlbumPageModel]:
    return SelectQuery(
        AlbumPageModel, 'SELECT * FROM "album_page" WHERE "userId" = $1', user_id
    )


def get_star_pass_statuss(user_id: int) -> SelectQuery[StarPassStatusModel]:
    return SelectQuery(
        StarPassStatusModel,
        'SELECT * FROM "star_pass_status" WHERE "userId" = $1',
        user_id,
    )


def get_login_pass_statuss(user_id: int) -> SelectQuery[LoginPassStatusModel]:
    return SelectQuery(
        LoginPassStatusModel,
        'SELECT * FROM "login_pass_status" WHERE "userId" = $1',
        user_id,
    )


def get_currencys(user_id: int) -> SelectQuery[CurrencyModel]:
    return SelectQuery(
        CurrencyModel, 'SELECT * FROM "currency" WHERE "userId" = $1', user_id
    )


def get_decorations(user_id: int) -> SelectQuery[DecorationModel]:
    return SelectQuery(
        DecorationModel, 'SELECT * FROM "decoration" WHERE "userId" = $1', user_id
    )


def get_live_achievements(user_id: int) -> SelectQuery[LiveAchievementModel]:
    return SelectQuery(
        LiveAchievementModel,
        'SELECT * FROM "live_achievement" WHERE "userId" = $1',
        user_id,
    )


def get_music_videos(user_id: int) -> SelectQuery[MusicVideoModel]:
    return SelectQuery(
        MusicVideoModel, 'SELECT * FROM "music_video" WHERE "userId" = $1', user_id
    )


def get_theater_storys(user_id: int) -> SelectQuery[TheaterStoryModel]:
    return SelectQuery(
        TheaterStoryModel, 'SELECT * FROM "theater_story" WHERE "userId" = $1', user_id
    )


def get_live_drop_cellings(user_id: int) -> SelectQuery[LiveDropCellingModel]:
    return SelectQuery(
        LiveDropCellingModel,
        'SELECT * FROM "live_drop_celling" WHERE "userId" = $1',
        user_id,
    )


def get_story_event_high_scores(user_id: int) -> SelectQuery[StoryEventHighScoreModel]:
    return SelectQuery(
        StoryEventHighScoreModel,
        'SELECT * FROM "story_event_high_score" WHERE "userId" = $1',
        user_id,
    )


def get_comics(user_id: int) -> SelectQuery[ComicModel]:
    return SelectQuery(ComicModel, 'SELECT * FROM "comic" WHERE "userId" = $1', user_id)


def get_comeback_campaigns(user_id: int) -> SelectQuery[ComebackCampaignModel]:
    return SelectQuery(
        ComebackCampaignModel,
        'SELECT * FROM "comeback_campaign" WHERE "userId" = $1',
        user_id,
    )


def get_concert_stages(user_id: int) -> SelectQuery[ConcertStageModel]:
    return SelectQuery(
        ConcertStageModel, 'SELECT * FROM "concert_stage" WHERE "userId" = $1', user_id
    )


def get_limits(user_id: int) -> SelectQuery[LimitModel]:
    return SelectQuery(LimitModel, 'SELECT * FROM "limit" WHERE "userId" = $1', user_id)


def get_gacha_selected_things(user_id: int) -> SelectQuery[GachaSelectedThingModel]:
    return SelectQuery(
        GachaSelectedThingModel,
        'SELECT * FROM "gacha_selected_thing" WHERE "userId" = $1',
        user_id,
    )


def get_total_point_events(user_id: int) -> SelectQuery[TotalPointEventModel]:
    return SelectQuery(
        TotalPointEventModel,
        'SELECT * FROM "total_point_event" WHERE "userId" = $1',
        user_id,
    )


def get_event_box_gachas(user_id: int) -> SelectQuery[EventBoxGachaModel]:
    return SelectQuery(
        EventBoxGachaModel,
        'SELECT * FROM "event_box_gacha" WHERE "userId" = $1',
        user_id,
    )


def get_event_box_gacha_box_things(
    user_id: int,
) -> SelectQuery[EventBoxGachaBoxThingModel]:
    return SelectQuery(
        EventBoxGachaBoxThingModel,
        'SELECT * FROM "event_box_gacha_box_thing" WHERE "userId" = $1',
        user_id,
    )


def get_special_events(user_id: int) -> SelectQuery[SpecialEventModel]:
    return SelectQuery(
        SpecialEventModel, 'SELECT * FROM "special_event" WHERE "userId" = $1', user_id
    )


def get_character_point_events(user_id: int) -> SelectQuery[CharacterPointEventModel]:
    return SelectQuery(
        CharacterPointEventModel,
        'SELECT * FROM "character_point_event" WHERE "userId" = $1',
        user_id,
    )


def get_another_notations(user_id: int) -> SelectQuery[AnotherNotationModel]:
    return SelectQuery(
        AnotherNotationModel,
        'SELECT * FROM "another_notation" WHERE "userId" = $1',
        user_id,
    )


def get_music_bookmarks(user_id: int) -> SelectQuery[MusicBookmarkModel]:
    return SelectQuery(
        MusicBookmarkModel,
        'SELECT * FROM "music_bookmark" WHERE "userId" = $1',
        user_id,
    )


def get_live_drop_limits(user_id: int) -> SelectQuery[LiveDropLimitModel]:
    return SelectQuery(
        LiveDropLimitModel,
        'SELECT * FROM "live_drop_limit" WHERE "userId" = $1',
        user_id,
    )


def get_restrictions(user_id: int) -> SelectQuery[RestrictionModel]:
    return SelectQuery(
        RestrictionModel, 'SELECT * FROM "restriction" WHERE "userId" = $1', user_id
    )


def get_permanent_market_things(user_id: int) -> SelectQuery[PermanentMarketThingModel]:
    return SelectQuery(
        PermanentMarketThingModel,
        'SELECT * FROM "permanent_market_thing" WHERE "userId" = $1',
        user_id,
    )


def get_time_limited_controls(user_id: int) -> SelectQuery[TimeLimitedControlModel]:
    return SelectQuery(
        TimeLimitedControlModel,
        'SELECT * FROM "time_limited_control" WHERE "userId" = $1',
        user_id,
    )


def get_flash_sale_stages(user_id: int) -> SelectQuery[FlashSaleStageModel]:
    return SelectQuery(
        FlashSaleStageModel,
        'SELECT * FROM "flash_sale_stage" WHERE "userId" = $1',
        user_id,
    )


def get_album_themes(user_id: int) -> SelectQuery[AlbumThemeModel]:
    return SelectQuery(
        AlbumThemeModel, 'SELECT * FROM "album_theme" WHERE "userId" = $1', user_id
    )


def get_circle_event_missions(user_id: int) -> SelectQuery[CircleEventMissionModel]:
    return SelectQuery(
        CircleEventMissionModel,
        'SELECT * FROM "circle_event_mission" WHERE "userId" = $1',
        user_id,
    )


def get_pickup_character_missions(
    user_id: int,
) -> SelectQuery[PickupCharacterMissionModel]:
    return SelectQuery(
        PickupCharacterMissionModel,
        'SELECT * FROM "pickup_character_mission" WHERE "userId" = $1',
        user_id,
    )


def get_league_season_results(user_id: int) -> SelectQuery[LeagueSeasonResultModel]:
    return SelectQuery(
        LeagueSeasonResultModel,
        'SELECT * FROM "league_season_result" WHERE "userId" = $1',
        user_id,
    )


def get_events(user_id: int) -> SelectQuery[EventModel]:
    return SelectQuery(EventModel, 'SELECT * FROM "event" WHERE "userId" = $1', user_id)


def get_bonus_lives(user_id: int) -> SelectQuery[BonusLiveModel]:
    return SelectQuery(
        BonusLiveModel, 'SELECT * FROM "bonus_live" WHERE "userId" = $1', user_id
    )


def get_bonus_live_stages(user_id: int) -> SelectQuery[BonusLiveStageModel]:
    return SelectQuery(
        BonusLiveStageModel,
        'SELECT * FROM "bonus_live_stage" WHERE "userId" = $1',
        user_id,
    )


def get_roulette_events(user_id: int) -> SelectQuery[RouletteEventModel]:
    return SelectQuery(
        RouletteEventModel,
        'SELECT * FROM "roulette_event" WHERE "userId" = $1',
        user_id,
    )


def get_roulettes(user_id: int) -> SelectQuery[RouletteModel]:
    return SelectQuery(
        RouletteModel, 'SELECT * FROM "roulette" WHERE "userId" = $1', user_id
    )


def get_home_b_g_ms(user_id: int) -> SelectQuery[HomeBGMModel]:
    return SelectQuery(
        HomeBGMModel, 'SELECT * FROM "home_b_g_m" WHERE "userId" = $1', user_id
    )


def get_link_characters(user_id: int) -> SelectQuery[LinkCharacterModel]:
    return SelectQuery(
        LinkCharacterModel,
        'SELECT * FROM "link_character" WHERE "userId" = $1',
        user_id,
    )


def get_music_courses(user_id: int) -> SelectQuery[MusicCourseModel]:
    return SelectQuery(
        MusicCourseModel, 'SELECT * FROM "music_course" WHERE "userId" = $1', user_id
    )


def get_tournament_qualifyings(user_id: int) -> SelectQuery[TournamentQualifyingModel]:
    return SelectQuery(
        TournamentQualifyingModel,
        'SELECT * FROM "tournament_qualifying" WHERE "userId" = $1',
        user_id,
    )


def get_lotterys(user_id: int) -> SelectQuery[LotteryModel]:
    return SelectQuery(
        LotteryModel, 'SELECT * FROM "lottery" WHERE "userId" = $1', user_id
    )


def get_triple_cast_partys(user_id: int) -> SelectQuery[TripleCastPartyModel]:
    return SelectQuery(
        TripleCastPartyModel,
        'SELECT * FROM "triple_cast_party" WHERE "userId" = $1',
        user_id,
    )


def get_triple_cast_party_slots(user_id: int) -> SelectQuery[TripleCastPartySlotModel]:
    return SelectQuery(
        TripleCastPartySlotModel,
        'SELECT * FROM "triple_cast_party_slot" WHERE "userId" = $1',
        user_id,
    )


def get_triple_cast_basics(user_id: int) -> SelectQuery[TripleCastBasicModel]:
    return SelectQuery(
        TripleCastBasicModel,
        'SELECT * FROM "triple_cast_basic" WHERE "userId" = $1',
        user_id,
    )


def get_triple_cast_groups(user_id: int) -> SelectQuery[TripleCastGroupModel]:
    return SelectQuery(
        TripleCastGroupModel,
        'SELECT * FROM "triple_cast_group" WHERE "userId" = $1',
        user_id,
    )


def get_triple_cast_group_members(
    user_id: int,
) -> SelectQuery[TripleCastGroupMemberModel]:
    return SelectQuery(
        TripleCastGroupMemberModel,
        'SELECT * FROM "triple_cast_group_member" WHERE "userId" = $1',
        user_id,
    )


def get_triple_cast_high_score_partys(
    user_id: int,
) -> SelectQuery[TripleCastHighScorePartyModel]:
    return SelectQuery(
        TripleCastHighScorePartyModel,
        'SELECT * FROM "triple_cast_high_score_party" WHERE "userId" = $1',
        user_id,
    )


def get_triple_cast_high_score_party_slots(
    user_id: int,
) -> SelectQuery[TripleCastHighScorePartySlotModel]:
    return SelectQuery(
        TripleCastHighScorePartySlotModel,
        'SELECT * FROM "triple_cast_high_score_party_slot" WHERE "userId" = $1',
        user_id,
    )


def get_triple_cast_season_results(
    user_id: int,
) -> SelectQuery[TripleCastSeasonResultModel]:
    return SelectQuery(
        TripleCastSeasonResultModel,
        'SELECT * FROM "triple_cast_season_result" WHERE "userId" = $1',
        user_id,
    )


def get_album_presets(user_id: int) -> SelectQuery[AlbumPresetModel]:
    return SelectQuery(
        AlbumPresetModel, 'SELECT * FROM "album_preset" WHERE "userId" = $1', user_id
    )


def get_gachas(user_id: int) -> SelectQuery[GachaModel]:
    return SelectQuery(GachaModel, 'SELECT * FROM "gacha" WHERE "userId" = $1', user_id)


def get_triple_cast_historys(user_id: int) -> SelectQuery[TripleCastHistoryModel]:
    return SelectQuery(
        TripleCastHistoryModel,
        'SELECT * FROM "triple_cast_history" WHERE "userId" = $1',
        user_id,
    )


def get_dugong_runs(user_id: int) -> SelectQuery[DugongRunModel]:
    return SelectQuery(
        DugongRunModel, 'SELECT * FROM "dugong_run" WHERE "userId" = $1', user_id
    )


def get_music_course_rankings(user_id: int) -> SelectQuery[MusicCourseRankingModel]:
    return SelectQuery(
        MusicCourseRankingModel,
        'SELECT * FROM "music_course_ranking" WHERE "userId" = $1',
        user_id,
    )


def get_friend_invitations(user_id: int) -> SelectQuery[FriendInvitationModel]:
    return SelectQuery(
        FriendInvitationModel,
        'SELECT * FROM "friend_invitation" WHERE "userId" = $1',
        user_id,
    )


def get_friend_invitation_missions(
    user_id: int,
) -> SelectQuery[FriendInvitationMissionModel]:
    return SelectQuery(
        FriendInvitationMissionModel,
        'SELECT * FROM "friend_invitation_mission" WHERE "userId" = $1',
        user_id,
    )


def get_name_base_colors(user_id: int) -> SelectQuery[NameBaseColorModel]:
    return SelectQuery(
        NameBaseColorModel,
        'SELECT * FROM "name_base_color" WHERE "userId" = $1',
        user_id,
    )


def get_icon_frames(user_id: int) -> SelectQuery[IconFrameModel]:
    return SelectQuery(
        IconFrameModel, 'SELECT * FROM "icon_frame" WHERE "userId" = $1', user_id
    )


def get_gacha_re_rolls(user_id: int) -> SelectQuery[GachaReRollModel]:
    return SelectQuery(
        GachaReRollModel, 'SELECT * FROM "gacha_re_roll" WHERE "userId" = $1', user_id
    )


def get_trial_party_events(user_id: int) -> SelectQuery[TrialPartyEventModel]:
    return SelectQuery(
        TrialPartyEventModel,
        'SELECT * FROM "trial_party_event" WHERE "userId" = $1',
        user_id,
    )


def get_trial_party_event_stages(
    user_id: int,
) -> SelectQuery[TrialPartyEventStageModel]:
    return SelectQuery(
        TrialPartyEventStageModel,
        'SELECT * FROM "trial_party_event_stage" WHERE "userId" = $1',
        user_id,
    )


def get_trial_party_event_stage_partys(
    user_id: int,
) -> SelectQuery[TrialPartyEventStagePartyModel]:
    return SelectQuery(
        TrialPartyEventStagePartyModel,
        'SELECT * FROM "trial_party_event_stage_party" WHERE "userId" = $1',
        user_id,
    )


def get_trial_party_event_stage_party_slots(
    user_id: int,
) -> SelectQuery[TrialPartyEventStagePartySlotModel]:
    return SelectQuery(
        TrialPartyEventStagePartySlotModel,
        'SELECT * FROM "trial_party_event_stage_party_slot" WHERE "userId" = $1',
        user_id,
    )


def get_user_blocks(user_id: int) -> SelectQuery[UserBlockModel]:
    return SelectQuery(
        UserBlockModel, 'SELECT * FROM "user_block" WHERE "userId" = $1', user_id
    )


def get_home_skins(user_id: int) -> SelectQuery[HomeSkinModel]:
    return SelectQuery(
        HomeSkinModel, 'SELECT * FROM "home_skin" WHERE "userId" = $1', user_id
    )


def get_accessory_auto_sells(user_id: int) -> SelectQuery[AccessoryAutoSellModel]:
    return SelectQuery(
        AccessoryAutoSellModel,
        'SELECT * FROM "accessory_auto_sell" WHERE "userId" = $1',
        user_id,
    )


def get_favorite_costumes(user_id: int) -> SelectQuery[FavoriteCostumeModel]:
    return SelectQuery(
        FavoriteCostumeModel,
        'SELECT * FROM "favorite_costume" WHERE "userId" = $1',
        user_id,
    )


def get_buff_item_statuss(user_id: int) -> SelectQuery[BuffItemStatusModel]:
    return SelectQuery(
        BuffItemStatusModel,
        'SELECT * FROM "buff_item_status" WHERE "userId" = $1',
        user_id,
    )


def get_multi_room_basics(user_id: int) -> SelectQuery[MultiRoomBasicModel]:
    return SelectQuery(
        MultiRoomBasicModel,
        'SELECT * FROM "multi_room_basic" WHERE "userId" = $1',
        user_id,
    )


def get_event_camps(user_id: int) -> SelectQuery[EventCampModel]:
    return SelectQuery(
        EventCampModel, 'SELECT * FROM "event_camp" WHERE "userId" = $1', user_id
    )
