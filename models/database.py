from typing import Any, Optional

from pydantic import BaseModel


class AccountModel(BaseModel):
    userId: int
    credential: str
    apiToken: Optional[str] = None
    platform: str = "Android"
    banLevel: int = 0
    registeredAt: int = 0
    lastLoginAt: int = 0


class UserModel(BaseModel):
    userId: int
    id: int
    playerRank: int
    currentRankPoint: int
    currentStamina: int
    maxStaminaRestoredAt: int
    paidJewel: int
    freeJewel: int
    coin: int
    playerRankLimit: int
    staminaRecoverTimesWithJewel: int
    circleUsageRestrictionsEndTime: int
    circleId: Optional[str] = None
    gameStartAt: int
    hashUserId: Optional[str] = None
    banLevel: int
    tutorialStatus: int
    monthlyPayment: int
    splashLastDisplayedAt: int
    isCapedPlayerRank: bool
    requireCapedPlayerRankAnnounce: bool


class UserProfileModel(BaseModel):
    userId: int
    userName: Optional[str] = None
    trophyMasterId1: Optional[int] = None
    trophyMasterId2: Optional[int] = None
    trophyMasterId3: Optional[int] = None
    mainMCharacterId: int
    mainCharacterLevel: int
    characterDisplayAwakeningStatus: bool
    iconFrameMasterId: int


class UserPreferenceModel(BaseModel):
    userId: int
    id: int
    multiPartyId: int
    birthDate: Optional[int] = None


class HomeDisplayPreferenceModel(BaseModel):
    userId: int
    id: int
    homeCharacterBaseMasterId: Optional[int] = None
    memberCharacterBaseMasterId: Optional[int] = None
    storyCharacterBaseMasterId: Optional[int] = None
    shopCharacterBaseMasterId: Optional[int] = None
    homeCostumeMasterId: Optional[int] = None
    memberCostumeMasterId: Optional[int] = None
    storyCostumeMasterId: Optional[int] = None
    shopCostumeMasterId: Optional[int] = None
    illustCharacterMasterId: int
    displayAwakeningStatus: bool
    homeCharacterDisplayType: int
    loginBonusCharacterBaseMasterId: Optional[int] = None
    loginBonusCostumeMasterId: Optional[int] = None


class CharacterModel(BaseModel):
    userId: int
    id: int
    characterMasterId: int
    level: int
    currentExperience: int
    talentStage: int
    awakeningPhase: int
    characterBaseId: int
    senseLevel: int
    readEpisodeOrder: int
    releasedEpisodeOrder: int
    displayAwakeningStatus: bool
    secondaryCharacterBaseId: Optional[int] = None
    secondarySenseLevel: int
    selectionType: int
    isFavorite: bool


class CharacterBaseModel(BaseModel):
    userId: int
    id: int
    characterBaseMasterId: int
    starRank: int
    totalStarPoint: int
    costumeMasterId: Optional[int] = None
    keyMissionLevel: int
    portalCharacterId: int
    portalDisplayAwakeningStatus: bool


class PartyModel(BaseModel):
    userId: int
    id: int
    order: int
    name: Optional[str] = None
    leaderPosition: int


class CharacterMasterModel(BaseModel):
    userId: int
    id: int
    characterBaseMasterId: int
    name: Optional[str] = None
    description: Optional[str] = None
    assetId: Optional[str] = None
    rarity: int
    attribute: int
    minLevelStatus: Optional[Any] = None
    starActMasterId: int
    awakenStarActMasterId: Optional[int] = None
    senseMasterId: int
    forbidGenericItemBloom: bool
    bloomBonusGroupMasterId: int
    senseEnhanceItemGroupMasterId: int
    firstEpisodeReleaseItemGroupId: int
    secondEpisodeReleaseItemGroupId: int
    characterAwakeningItemGroupMasterId: Optional[int] = None
    displayStartAt: int
    displayEndAt: int
    unlockText: Optional[str] = None
    categories: Optional[Any] = None
    leaderSenseMasterId: Optional[int] = None
    maxTalentStage: int
    maxTalentStageReleaseDate: Optional[int] = None
    secondaryCharacterBaseMasterId: Optional[int] = None
    secondarySenseMasterId: Optional[int] = None
    secondaryAttribute: Optional[int] = None


class CharacterBaseMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    school: Optional[str] = None
    grade: Optional[int] = None
    birthMonth: Optional[int] = None
    birthDay: Optional[int] = None
    height: int
    hobby: Optional[str] = None
    companyMasterId: int
    nameRomanization: Optional[str] = None
    senseName: Optional[str] = None
    senseEffect: Optional[str] = None
    characterVoice: Optional[str] = None
    profileImageAssetId: Optional[str] = None
    age: Optional[int] = None
    familyNameRomanization: Optional[str] = None
    firstNameRomanization: Optional[str] = None
    pronounceFamilyName: Optional[str] = None
    pronounceFirstName: Optional[str] = None
    familyName: Optional[str] = None
    firstName: Optional[str] = None
    evoSenseName: Optional[str] = None
    evoSenseEffect: Optional[str] = None
    defaultCostumeMasterId: int
    characterBaseType: int


class CharacterLevelMasterModel(BaseModel):
    userId: int
    level: int
    experienceToLevelUp: int
    characterStatusLevel: int
    startDate: int


class PosterModel(BaseModel):
    userId: int
    id: int
    posterMasterId: int
    level: int
    breakthroughPhase: int
    releasedEpisode: int
    itemConsumeBreakThroughCount: int
    isFavorite: bool
    alternativeImagePattern: int


class AccessoryLevelPatternGroupMasterModel(BaseModel):
    userId: int
    id: int
    patterns: Optional[Any] = None


class AccessoryLevelPatternMasterModel(BaseModel):
    userId: int
    id: int
    accessoryLevelPatternGroupMasterId: int
    level: int
    requiredCoin: int
    items: Optional[Any] = None


class AccessoryMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    rarity: int
    accessoryLevelPatternGroupId: int
    fixedAccessoryEffects: Optional[Any] = None
    randomEffectGroups: Optional[Any] = None
    pronounceName: Optional[str] = None
    series: int
    maxLevel: int


class EpisodeMasterModel(BaseModel):
    userId: int
    id: int
    storyMasterId: int
    title: Optional[str] = None
    order: int
    episodeRewardPackageMasterId: int
    conditions: Optional[Any] = None
    preEpisodeMasterId: Optional[int] = None
    displayStartDate: Optional[int] = None
    displayEndDate: Optional[int] = None


class EpisodeRewardPackageMasterModel(BaseModel):
    userId: int
    id: int
    rewards: Optional[Any] = None


class LiveMasterModel(BaseModel):
    userId: int
    id: int
    difficulty: int
    musicMasterId: int
    level: int
    noteCount: int
    unlockCondition: int
    unlockValue: Optional[int] = None
    startDate: int
    endDate: int


class MusicMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    rewardRuleMasterId: int
    pronounceName: Optional[str] = None
    lyricWriter: Optional[str] = None
    composer: Optional[str] = None
    arranger: Optional[str] = None
    unlockText: Optional[str] = None
    isLongVersion: bool
    releasedAt: Optional[int] = None
    staminaConsumption: int
    musicTimeSecond: int
    invisible: bool
    sampleStartSeconds: float
    sampleEndSeconds: float
    delaySeconds: float
    vocalVersions: Optional[Any] = None
    unlockConditionType: int
    unlockConditionValue: Optional[int] = None
    musicVideoType: int
    musicCoverType: int
    storyEventMasterId: Optional[int] = None
    storyMasterId: Optional[int] = None
    eventMasterId: Optional[int] = None


class SenseMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    type: int
    preEffects: Optional[Any] = None
    branches: Optional[Any] = None
    acquirableGauge: int
    acquirableScorePercent: int
    scoreUpPerLevel: int
    lightCount: int
    coolTime: int
    branchCondition1: int
    conditionValue1: Optional[int] = None
    branchCondition2: int
    conditionValue2: Optional[int] = None
    subTypes: Optional[Any] = None


class StoryMasterModel(BaseModel):
    userId: int
    id: int
    type: int
    companyMasterId: Optional[int] = None
    eventMasterId: Optional[int] = None
    chapterOrder: int
    displayStartAt: int
    displayEndAt: int


class PosterLevelPatternGroupMasterModel(BaseModel):
    userId: int
    id: int
    patterns: Optional[Any] = None


class PosterLevelPatternMasterModel(BaseModel):
    userId: int
    id: int
    levelPatternGroupId: int
    level: int
    itemMasterId: int
    quantity: int


class PosterMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    organizeRestrictGroupId: Optional[int] = None
    rarity: int
    levelPatternGroupMasterId: int
    subTitlePositionX1: Optional[float] = None
    subTitlePositionY1: Optional[float] = None
    subTitlePositionX2: Optional[float] = None
    subTitlePositionY2: Optional[float] = None
    subTitlePositionX3: Optional[float] = None
    subTitlePositionY3: Optional[float] = None
    releaseItemGroupId: int
    pronounceName: Optional[str] = None
    costumes: Optional[Any] = None
    appearanceCharacterBaseMasterIds: Optional[Any] = None
    isRestrictItemBreakThrough: bool
    displayStartAt: int
    displayEndAt: int
    unlockText: Optional[str] = None
    orientation: int
    subTitleDisplayCondition: int
    subTitleDisplayConditionValue: Optional[int] = None
    posterBreakthroughMaxPhase: Optional[int] = None
    posterBreakthroughMaxPhaseReleaseDate: Optional[int] = None
    secondarySubTitleDisplayCondition: int
    secondarySubTitleDisplayConditionValue: Optional[int] = None
    alternateImagePositionX1: Optional[float] = None
    alternateImagePositionY1: Optional[float] = None
    alternateImageReleasePhase1: Optional[int] = None
    alternateImagePositionX2: Optional[float] = None
    alternateImagePositionY2: Optional[float] = None
    alternateImageReleasePhase2: Optional[int] = None
    alternateImagePositionX3: Optional[float] = None
    alternateImagePositionY3: Optional[float] = None
    alternateImageReleasePhase3: Optional[int] = None


class LiveModel(BaseModel):
    userId: int
    id: int
    liveMasterId: int
    timesCompleted: int
    achievementRate: float
    notationRate: float
    clearLamp: int
    status: int
    rateGrade: int


class MusicModel(BaseModel):
    userId: int
    id: int
    musicMasterId: int
    stellaReleased: bool
    vocalVersion: int
    olivierReleaseStatus: int
    isPossession: bool


class AccessoryModel(BaseModel):
    userId: int
    id: int
    accessoryMasterId: int
    level: int
    locked: bool
    accessoryEffects: Optional[Any] = None
    referenceCounting: int
    isFavorite: bool


class ItemModel(BaseModel):
    userId: int
    id: int
    itemMasterId: int
    stock: int


class AccessoryEffectMasterModel(BaseModel):
    userId: int
    id: int
    effectMasterId: int
    name: Optional[str] = None
    description: Optional[str] = None
    variety: Optional[int] = None


class CompanyMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    companies: int
    description: Optional[str] = None
    isOther: bool


class EffectDurationGroupMasterModel(BaseModel):
    userId: int
    id: int
    durations: Optional[Any] = None


class EffectMasterModel(BaseModel):
    userId: int
    id: int
    type: int
    range: int
    calculationType: int
    details: Optional[Any] = None
    conditions: Optional[Any] = None
    durationSecond: int
    triggers: Optional[Any] = None
    fireTimingType: int


class ItemMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    displayOrder: int
    displayEndDate: Optional[int] = None
    maxStock: int
    category: int
    consumable: bool
    jumpType: Optional[int] = None
    jumpTargetId: Optional[int] = None
    tabCategory: int
    rarity: int


class RandomEffectGroupMasterModel(BaseModel):
    userId: int
    id: int
    accessoryEffects: Optional[Any] = None


class RewardRuleMasterModel(BaseModel):
    userId: int
    id: int
    achivementRateRewards: Optional[Any] = None


class SenseEffectMasterModel(BaseModel):
    userId: int
    order: int
    effectMasterId: int


class TrophyGroupMasterModel(BaseModel):
    userId: int
    id: int
    category: int


class TrophyMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    rarity: int
    order: int
    trophyGroupMasterId: int
    hidden: bool
    unlockText: Optional[str] = None


class CharacterLessonModel(BaseModel):
    userId: int
    characterBaseMasterId: int
    setCharacters: Optional[Any] = None
    bestScore: int
    leaderPosition: int
    rewardReceivedHighScore: int


class DailyLessonModel(BaseModel):
    userId: int
    timesLeft: int


class InboxModel(BaseModel):
    userId: int
    id: int
    thingType: int
    thingId: int
    thingQuantity: int
    isTimeLimited: bool
    hasReceived: bool
    title: Optional[str] = None
    description: Optional[str] = None
    sentAt: int
    receivedAt: Optional[int] = None
    receiveLimitAt: int


class BombModel(BaseModel):
    userId: int
    id: int
    bombMasterIds: Optional[Any] = None


class CostumeModel(BaseModel):
    userId: int
    id: int
    costumeMasterId: int


class NameColorModel(BaseModel):
    userId: int
    id: int
    nameColorMasterIds: Optional[Any] = None


class NameplateModel(BaseModel):
    userId: int
    id: int
    namePlateMasterId: int


class NoteModel(BaseModel):
    userId: int
    id: int
    noteMasterIds: Optional[Any] = None


class MissionModel(BaseModel):
    userId: int
    id: int
    isCleared: bool
    isRewardReceived: bool
    missionCurrentCount: int
    missionMasterId: int
    currentMissionStageMasterId: int


class AuditionMasterModel(BaseModel):
    userId: int
    id: int
    musicMasterId: int
    recommendedCompany: int
    canSkip: bool
    senseNotationMasterId: int
    maxPhase: Optional[str] = None
    displayStartAt: int
    displayEndAt: int
    vocalVersion: int
    auditionGroupNumber: int
    skipStartAt: int


class BombMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    order: int
    hidden: bool
    isDefault: bool


class CharacterStarRankMasterModel(BaseModel):
    userId: int
    rank: int
    nextRankPoint: int
    requiredLessonScore: int
    statusBonus: float


class CharacterStarRankRewardGroupMasterModel(BaseModel):
    userId: int
    id: int
    rewards: Optional[Any] = None


class CostumeMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    order: int
    isDefault: bool
    costumeGroupMasterId: int
    description: Optional[str] = None


class HomeCharacterVoiceMasterModel(BaseModel):
    userId: int
    id: int
    characterBaseMasterId: int
    text: Optional[str] = None
    weight: int
    characterVoicePeriodMasterId: Optional[int] = None
    isPlayerBirthDateVoice: bool
    voiceFileName1: Optional[str] = None
    voiceFileName2: Optional[str] = None
    voiceFileName3: Optional[str] = None
    voiceFileName4: Optional[str] = None
    voiceInterval1: float
    voiceInterval2: float
    voiceInterval3: float
    mouthMotionId1: Optional[str] = None
    mouthMotionId2: Optional[str] = None
    mouthMotionId3: Optional[str] = None
    mouthMotionId4: Optional[str] = None
    bodyMotionId1: Optional[str] = None
    bodyMotionId2: Optional[str] = None
    bodyMotionId3: Optional[str] = None
    bodyMotionId4: Optional[str] = None


class NameColorMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    order: int
    hidden: bool
    isDefault: bool
    unlockText: Optional[str] = None


class NameplateMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    order: int
    hidden: bool
    isDefault: bool
    details: Optional[Any] = None
    unlockText: Optional[str] = None
    changeType: int
    changeValue1: Optional[int] = None
    changeValue2: Optional[int] = None


class NoteMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    order: int
    hidden: bool
    isDefault: bool


class SpotConversationMasterModel(BaseModel):
    userId: int
    id: int
    spot: int
    characterId1: Optional[int] = None
    characterId2: Optional[int] = None
    characterId3: Optional[int] = None
    characterId4: Optional[int] = None
    characterId5: Optional[int] = None
    episodeMasterId: int
    costumeId1: Optional[int] = None
    costumeId2: Optional[int] = None
    costumeId3: Optional[int] = None
    costumeId4: Optional[int] = None
    costumeId5: Optional[int] = None
    title: Optional[str] = None


class StampMasterModel(BaseModel):
    userId: int
    id: int
    order: int
    isDefault: bool
    characterBaseMasterId: int
    type: int
    assetId: Optional[str] = None
    voiceAssetId: Optional[str] = None
    name: Optional[str] = None
    characterBaseMasterIds: Optional[Any] = None


class CharacterLessonSlotModel(BaseModel):
    userId: int
    position: int
    setCharacterId: Optional[int] = None


class TrophyModel(BaseModel):
    userId: int
    id: int
    trophyMasterId: int
    trophyGroupMasterId: int
    currentOrder: int


class MarketModel(BaseModel):
    userId: int
    id: int
    lastRefreshedAt: int
    refreshTimes: int


class ViewedShopModel(BaseModel):
    userId: int
    id: int
    exchangeShopMasterId: Optional[int] = None
    lastViewedAt: int
    viewedShopCategory: int


class UserBonusModel(BaseModel):
    userId: int
    id: int
    experienceBonus: float
    lessonStarRankBonus: float


class AuditionPhaseMasterModel(BaseModel):
    userId: int
    id: int
    auditionasterId: int
    phase: int
    recommendedPlayerRank: int
    clearScore: int
    starActCount: Optional[int] = None
    auditionRewardPackageMasterId: int


class AuditionRewardPackageMasterModel(BaseModel):
    userId: int
    id: int
    rewards: Optional[Any] = None


class CampaignMasterModel(BaseModel):
    userId: int
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    iconImagePath: Optional[str] = None
    order: int
    startDate: int
    endDate: int
    comebackCampaignMasterId: Optional[int] = None
    campaignEffectType: int
    campaignEffectValue: int


class CharacterAwakeningItemMasterModel(BaseModel):
    userId: int
    id: int
    awakeningPhase: int
    itemMasterId: int
    requiredQuantity: int


class CharacterBloomBonusGroupMasterModel(BaseModel):
    userId: int
    id: int
    bloomBonuses: Optional[Any] = None
    bloomRewards: Optional[Any] = None


class CharacterBloomItemMasterModel(BaseModel):
    userId: int
    rarity: int
    currentStage: int
    requiredPieceAmount: int
    talentBloomItemType: int
    genericBloomItemMasterId: Optional[int] = None
    requiredItemMasterId: Optional[int] = None
    requiredItemAmount: Optional[int] = None


class CharacterExperienceItemMasterModel(BaseModel):
    userId: int
    id: int
    itemMasterId: int
    acquirableExperience: int
    acquirableExperienceBonus: float


class CharacterMissionMasterModel(BaseModel):
    userId: int
    id: int
    title: Optional[str] = None
    jumpType: Optional[int] = None
    jumpValue: Optional[int] = None
    stages: Optional[Any] = None


class CharacterMissionStageMasterModel(BaseModel):
    userId: int
    id: int
    characterMissionCategoryLevelMasterId: int
    characterMissionMasterId: int
    exclusionNoSenseCharacter: bool
    order: int
    stageOrder: int
    goalCount: int


class CharacterPieceMasterModel(BaseModel):
    userId: int
    itemMasterId: int
    characterMasterId: int
    dugongRequiredAmount: int
    talentBloomItemType: int


class CharacterSenseEnhanceItemGroupMasterModel(BaseModel):
    userId: int
    id: int
    items: Optional[Any] = None


class CostumeWearableCharacterGroupMasterModel(BaseModel):
    userId: int
    id: int
    characterBaseMasterIds: Optional[Any] = None


class ExchangeShopMasterModel(BaseModel):
    userId: int
    id: int
    isDisplayRequiredHavingItem: bool
    category: int
    name: Optional[str] = None
    displayThingType: int
    displayItemMasterId: Optional[int] = None
    bannerPath: Optional[str] = None
    startDate: Optional[int] = None
    endDate: Optional[int] = None
    lastRefreshedAt: int
    lineup: Optional[Any] = None
    order: int


class LiveSettingMasterModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    liveType: int
    liveDropFrameGroupMasterId: int


class MissionMasterModel(BaseModel):
    userId: int
    id: int
    missionCategory: int
    missionViewOrder: int
    title: Optional[str] = None
    description: Optional[str] = None
    eventMasterId: Optional[int] = None
    jumpType: int
    jumpTargetId: Optional[int] = None
    startDate: int
    endDate: int
    stages: Optional[Any] = None
    comebackCampaignMasterId: Optional[int] = None


class MusicVocalVersionMasterModel(BaseModel):
    userId: int
    id: int
    musicMasterId: int
    vocalVersion: int
    singer: Optional[str] = None
    name: Optional[str] = None
    musicTimeSecond: int
    sampleStartSeconds: float
    sampleEndSeconds: float
    musicVideoType: int
    characters: Optional[Any] = None


class PosterReleaseItemGroupMasterModel(BaseModel):
    userId: int
    id: int
    items: Optional[Any] = None
    itemConsumeApplyFlag: bool


class PosterReleaseItemMasterModel(BaseModel):
    userId: int
    currentPhase: int
    itemMasterId: int
    requiredQuantity: int


class PosterStoryMasterModel(BaseModel):
    userId: int
    id: int
    posterMasterId: int
    episodeType: int
    characterBaseMasterId: Optional[int] = None
    description: Optional[str] = None
    order: int
    characterIconId: Optional[int] = None
    characterName: Optional[str] = None


class StarRankRewardMasterModel(BaseModel):
    userId: int
    rank: int
    characterBaseMasterId: int
    characterStarRankRewardGroupMasterId: int


class AuditionClearModel(BaseModel):
    userId: int
    id: int
    auditionMasterId: int
    clearPhase: int
    auditionClearPartyId: int
    skipClearPhase: int


class SpRateModel(BaseModel):
    userId: int
    id: int
    liveMasterId: int
    point: int


class NotificationModel(BaseModel):
    userId: int
    id: int
    importantReadAt: int
    updateReadAt: int
    bugReadAt: int


class EpisodeModel(BaseModel):
    userId: int
    episodeMasterId: int
    hasReadAll: bool


class CharacterMissionModel(BaseModel):
    userId: int
    id: int
    characterBaseMasterId: int
    characterMissionMasterId: int
    currentStageMasterId: int
    currentCount: int
    clearedStageOrder: int
    rewardReceivedStageOrder: int
    completedLevel: int


class MissionPassModel(BaseModel):
    userId: int
    id: int
    missionPassMasterId: int
    paid: bool
    freeRewardReceivedPhase: Optional[int] = None
    spRewardReceivedPhase: Optional[int] = None
    terminated: bool
    freeRewardLoopCount: Optional[int] = None
    freeRewardLoopReceivedPhase: Optional[int] = None
    paidRewardLoopCount: Optional[int] = None
    paidRewardLoopReceivedPhase: Optional[int] = None


class MissionPassDetailMasterModel(BaseModel):
    userId: int
    id: int
    phase: int
    missionPassMasterId: Optional[int] = None
    clearPoint: int
    startDate: int
    endDate: int
    rewards: Optional[Any] = None


class MissionPassMasterModel(BaseModel):
    userId: int
    id: int
    itemMasterId: int
    startDate: int
    endDate: int


class LeagueBasicModel(BaseModel):
    userId: int
    myProperty: int
    starEnrollCount: int
    daiStarEnrollCount: int
    currentClassType: int
    bestClassType: int
    lastJoinedLeagueSeasonMasterId: Optional[int] = None


class StoryEventModel(BaseModel):
    userId: int
    id: int
    storyEventMasterId: int
    totalAcquiredPoint: int
    acquiredPointUpdatedDate: int
    lastRank: Optional[int] = None
    readTips: bool
    loginDays: int


class ExchangeLimitModel(BaseModel):
    userId: int
    id: int
    exchangeShopThingId: int
    replaceType: int
    specifiedNumberOfDaysLimit: Optional[int] = None
    exchangedCount: int
    until: Optional[int] = None


class LeagueGroupModel(BaseModel):
    userId: int
    leagueMasterId: int
    classType: int
    classOrder: int


class LeagueGroupMemberModel(BaseModel):
    userId: int
    leagueGroupId: int
    leagueMasterId: int
    bestScore: Optional[int] = None


class LeagueHistoryModel(BaseModel):
    userId: int
    leagueMasterId: int
    classType: int
    historyCount: int
    isSendedReward: bool
    isPlayed: bool
    classChangeType: int
    groupRank: int
    globalRank: int
    allClassGlobalRank: int


class JewelShopModel(BaseModel):
    userId: int
    id: int
    jewelShopItemMasterId: int
    purchaseCount: int
    totalPurchaseCount: int
    rePurchaseDate: Optional[int] = None


class DailyLimitModel(BaseModel):
    userId: int
    id: int
    autoPlayTimes: int
    dailyLessonTimes: int
    lastRefreshedAt: Optional[int] = None
    musicCourseFreeChallengeTimes: int


class LeagueHighScorePartyModel(BaseModel):
    userId: int
    id: int
    leagueMasterId: int
    highScore: int
    classType: int
    difficulty: int
    musicMasterId: int
    leagueGroupId: int
    slots: Optional[Any] = None
    userName: Optional[str] = None
    actingAbility: int
    leaderPosition: int


class LeagueHighScorePartySlotModel(BaseModel):
    userId: int
    id: int
    leagueHighScorePartyId: int
    position: int
    characterMasterId: int
    characterLevel: int
    posterMasterId: Optional[int] = None
    posterLevel: Optional[int] = None
    posterBreakthroughPhase: Optional[int] = None
    accessoryMasterId: Optional[int] = None
    accessoryLevel: Optional[int] = None
    currentStatus: Optional[Any] = None
    characterTalentStage: int
    characterAwakeningPhase: int
    characterDisplayAwakeningStatus: bool


class StoryEventCircleModel(BaseModel):
    userId: int
    id: int
    storyEventMasterId: int
    currentPoint: int
    highScore: int
    circleId: Optional[int] = None


class StoryEventCircleMissionModel(BaseModel):
    userId: int
    id: int
    storyEventCircleMissionMasterId: int
    currentCount: int


class StoryEventCircleMissionRewardModel(BaseModel):
    userId: int
    id: int
    storyEventMasterId: int
    storyEventCircleMissionRewardMasterId: int


class StoryEventHighScoreBuffSettingModel(BaseModel):
    userId: int
    storyEventHighScoreBuffSettingMasterId: int
    currentLevel: int


class StoryEventHighScorePartyModel(BaseModel):
    userId: int
    id: int
    storyEventMasterId: int
    highScore: int
    rateGrade: int
    difficulty: int
    highScoreType: int
    liveSettingMasterId: int
    slots: Optional[Any] = None
    leaderPosition: int


class StoryEventHighScorePartySlotModel(BaseModel):
    userId: int
    id: int
    storyEventHighScoreClearPartyId: int
    position: int
    characterMasterId: int
    characterLevel: int
    characterTalentStage: int
    characterAwakeningPhase: int
    posterMasterId: Optional[int] = None
    posterLevel: Optional[int] = None
    posterBreakthroughPhase: Optional[int] = None
    accessoryMasterId: Optional[int] = None
    accessoryLevel: Optional[int] = None
    currentStatus: Optional[Any] = None
    characterDisplayAwakeningStatus: bool


class ConnectWithAccountModel(BaseModel):
    userId: int
    id: int
    provider: int


class ConnectWithPasswordModel(BaseModel):
    userId: int
    id: int


class TournamentDetailModel(BaseModel):
    userId: int
    id: int
    tournamentDetailMasterId: int
    bestUniqueScore: int
    perfectStar: int
    perfect: int
    great: int
    good: int
    bad: int
    miss: int
    recordedAt: int


class GradualMissionGroupModel(BaseModel):
    userId: int
    id: int
    gradualMissionGroupMasterId: int
    startAt: int


class PhotoModel(BaseModel):
    userId: int
    id: int
    fileName: Optional[str] = None
    sasToken: Optional[str] = None
    photoEffectMasterId: Optional[int] = None
    lock: bool
    useAlbumPage: Optional[int] = None
    level: int
    rarity: int
    signMasterId: Optional[int] = None
    generatedAt: int
    thumbnailSasToken: Optional[str] = None
    appearedCharacterBaseMasterIds: Optional[Any] = None
    taggedCharacterBaseMasterIds: Optional[Any] = None
    useDecoPage: int


class AlbumModel(BaseModel):
    userId: int
    id: int
    level: int
    publishPageNumber: int
    currentPresetOrder: int


class AlbumPageModel(BaseModel):
    userId: int
    id: int
    page: int
    editType: int
    publishing: bool
    items: Optional[Any] = None
    albumThemeMasterId: Optional[int] = None


class StarPassStatusModel(BaseModel):
    userId: int
    id: int
    type: int
    totalPurchasedCount: int
    validUntil: int


class LoginPassStatusModel(BaseModel):
    userId: int
    id: int
    validUntil: int


class CurrencyModel(BaseModel):
    userId: int
    id: int
    coin: int
    freeJewel: int
    paidJewel: int


class DecorationModel(BaseModel):
    userId: int
    id: int
    decorationMasterId: int


class LiveAchievementModel(BaseModel):
    userId: int
    id: int
    olivierReleasedCount: int
    olivierClearedLevel: int


class MusicVideoModel(BaseModel):
    userId: int
    id: int
    musicVideoMasterId: int


class TheaterStoryModel(BaseModel):
    userId: int
    id: int
    theaterStoryMasterId: int


class LiveDropCellingModel(BaseModel):
    userId: int
    id: int
    multiLiveScheduleMasterId: int
    count: int
    totalCellingCount: int


class StoryEventHighScoreModel(BaseModel):
    userId: int
    id: int
    storyEventMasterId: int
    currentEnhancementPoint: int
    totalAcquiredEnhancementPoint: int


class ComicModel(BaseModel):
    userId: int
    comicEpisodeMasterId: int


class ComebackCampaignModel(BaseModel):
    userId: int
    comebackCampaignMasterId: int
    activatedAt: int


class ConcertStageModel(BaseModel):
    userId: int
    concertStageMasterId: int


class LimitModel(BaseModel):
    userId: int
    id: int
    additionalAcquirablePhotoLimit: int
    acquirablePhotoLimitIncreasedTimes: int
    additionalAcquirableAccessoryLimit: int
    acquirableAccessoryLimitIncreasedTimes: int


class GachaSelectedThingModel(BaseModel):
    userId: int
    gachaMasterId: int
    gachaThingIds: Optional[Any] = None


class TotalPointEventModel(BaseModel):
    userId: int
    id: int
    totalPointEventMasterId: int
    totalAcquiredPoint: int
    receivedRewardOrder: int


class EventBoxGachaModel(BaseModel):
    userId: int
    id: int
    eventBoxGachaMasterId: int
    currentBoxCount: int


class EventBoxGachaBoxThingModel(BaseModel):
    userId: int
    id: int
    eventBoxGachaBoxThingMasterId: int
    hitCount: int


class SpecialEventModel(BaseModel):
    userId: int
    id: int
    specialEventMasterId: int
    readTips: bool


class CharacterPointEventModel(BaseModel):
    userId: int
    id: int
    characterPointEventMasterId: int
    characterBaseMasterId: Optional[int] = None
    totalAcquiredPoint: int
    lastRank: int
    readTips: bool


class AnotherNotationModel(BaseModel):
    userId: int
    id: int
    anotherNotationMasterId: int
    clearLamp: int
    rateGrade: int
    achievementRatePercentRecord: Optional[Any] = None


class MusicBookmarkModel(BaseModel):
    userId: int
    musicMasterId: int
    musicBookmarkFlag: int


class LiveDropLimitModel(BaseModel):
    userId: int
    multiLiveScheduleMasterId: int
    currentCount: int
    countLimit: int


class RestrictionModel(BaseModel):
    userId: int
    id: int
    multiLiveRestrictionFinishedAt: Optional[int] = None
    readMultiLiveRestrictionDialog: Optional[bool] = None


class PermanentMarketThingModel(BaseModel):
    userId: int
    permanentMarketThingMasterId: int
    purchaseCount: int


class TimeLimitedControlModel(BaseModel):
    userId: int
    id: int
    timeLimitedControlMasterId: int
    expiredAt: int


class FlashSaleStageModel(BaseModel):
    userId: int
    id: int
    flashSaleStageMasterId: int
    purchaseLimitedAt: Optional[int] = None
    isDefault: bool
    isCompleted: bool


class AlbumThemeModel(BaseModel):
    userId: int
    id: int
    albumThemeMasterId: int


class CircleEventMissionModel(BaseModel):
    userId: int
    circleEventMissionMasterId: int
    currentCount: int
    isActive: bool


class PickupCharacterMissionModel(BaseModel):
    userId: int
    pickupCharacterMissionMasterId: int
    receivedDetailMasterIds: Optional[Any] = None


class LeagueSeasonResultModel(BaseModel):
    userId: int
    leagueSeasonMasterId: int
    daiStarMaxEnrollCount: int


class EventModel(BaseModel):
    userId: int
    id: int
    eventMasterId: int
    totalAcquiredPoint: int
    acquiredPointUpdatedDate: int
    lastRank: Optional[int] = None
    readTips: bool
    loginDays: int


class BonusLiveModel(BaseModel):
    userId: int
    id: int
    bonusLiveMasterId: int
    clearedStageOrder: int
    readTips: bool
    dailyClearTimes: int


class BonusLiveStageModel(BaseModel):
    userId: int
    id: int
    bonusLiveMasterStageId: int
    clearTimes: int


class RouletteEventModel(BaseModel):
    userId: int
    id: int
    rouletteEventMasterId: int
    totalAcquiredPoint: int


class RouletteModel(BaseModel):
    userId: int
    id: int
    rouletteMasterId: int
    rollCount: int


class HomeBGMModel(BaseModel):
    userId: int
    homeBGMMasterId: int
    selectionType: int
    homeBGMDetailMasterId: Optional[int] = None


class LinkCharacterModel(BaseModel):
    userId: int
    id: int
    characterBaseMasterId: int
    companyMasterId: int
    linkedCharacterBaseMasterId: Optional[int] = None
    rewardReceivedMaxRank: int


class MusicCourseModel(BaseModel):
    userId: int
    id: int
    musicCourseMasterId: int
    clearLamp: int
    certificationGrade: int
    totalAchievementRatePercentRecord: Optional[Any] = None


class TournamentQualifyingModel(BaseModel):
    userId: int
    id: int
    tournamentQualifyingMasterId: int
    musicCourseMasterId: int
    currentChallengeCount: int
    perfectStar: int
    perfect: int
    great: int
    good: int
    bad: int
    miss: int
    totalAchievementRatePercentRecord: Optional[Any] = None
    bestRecordChallengeCount: int
    bestRecordDate: Optional[int] = None


class LotteryModel(BaseModel):
    userId: int
    lotteryMasterId: int
    results: Optional[Any] = None


class TripleCastPartyModel(BaseModel):
    userId: int
    id: int
    order: int
    name: Optional[str] = None
    leaderPosition: int


class TripleCastPartySlotModel(BaseModel):
    userId: int
    id: int
    partyId: int
    position: int
    characterId: int
    posterId: Optional[int] = None
    accessoryId: Optional[int] = None
    bonusAbilityEnableFlags: int


class TripleCastBasicModel(BaseModel):
    userId: int
    id: int
    starEnrollCount: int
    daiStarEnrollCount: int
    currentClassType: int
    bestClassType: int
    lastJoinedTripleCastSeasonMasterId: Optional[int] = None
    partyOrder1: Optional[int] = None
    partyOrder2: Optional[int] = None
    partyOrder3: Optional[int] = None


class TripleCastGroupModel(BaseModel):
    userId: int
    tripleCastMasterId: int
    classType: int
    classOrder: int


class TripleCastGroupMemberModel(BaseModel):
    userId: int
    tripleCastGroupId: int
    tripleCastMasterId: int
    bestScore: Optional[int] = None


class TripleCastHighScorePartyModel(BaseModel):
    userId: int
    id: int
    tripleCastMasterId: int
    order: int
    highScore: int
    slots: Optional[Any] = None
    actingAbility: int
    leaderPosition: int
    difficulty: int


class TripleCastHighScorePartySlotModel(BaseModel):
    userId: int
    id: int
    tripleCastHighScorePartyId: int
    position: int
    characterMasterId: int
    characterLevel: int
    posterMasterId: Optional[int] = None
    posterLevel: Optional[int] = None
    posterBreakthroughPhase: Optional[int] = None
    accessoryMasterId: Optional[int] = None
    accessoryLevel: Optional[int] = None
    currentStatus: Optional[Any] = None
    characterTalentStage: int
    characterAwakeningPhase: int
    characterDisplayAwakeningStatus: bool


class TripleCastSeasonResultModel(BaseModel):
    userId: int
    tripleCastSeasonMasterId: int
    daiStarMaxEnrollCount: int


class AlbumPresetModel(BaseModel):
    userId: int
    id: int
    name: Optional[str] = None
    order: int


class GachaModel(BaseModel):
    userId: int
    id: int
    gachaMasterId: int
    rollCount: int


class TripleCastHistoryModel(BaseModel):
    userId: int
    tripleCastMasterId: int
    classType: int
    historyCount: int
    isSendedReward: bool
    isPlayed: bool
    classChangeType: int
    groupRank: int
    globalRank: int
    allClassGlobalRank: int


class DugongRunModel(BaseModel):
    userId: int
    id: int
    clearedCourseIds: Optional[Any] = None
    noMistakeCourseIds: Optional[Any] = None
    dugongRunCourseGroupId: int


class MusicCourseRankingModel(BaseModel):
    userId: int
    id: int
    musicCourseMasterId: int
    currentChallengeCount: int
    perfectStar: int
    perfect: int
    great: int
    good: int
    bad: int
    miss: int
    totalAchievementRatePercentRecord: Optional[Any] = None
    bestRecordChallengeCount: int
    bestRecordDate: Optional[int] = None
    hasReceivedReward: bool


class FriendInvitationModel(BaseModel):
    userId: int
    id: int
    invitationCode: Optional[str] = None
    hasInputOtherInvitationCode: bool


class FriendInvitationMissionModel(BaseModel):
    userId: int
    id: int
    friendInvitationMissionMasterId: int
    friendInvitationMissionStageMasterId: int
    currentCount: int
    isCleared: bool
    isRewardReceived: bool


class NameBaseColorModel(BaseModel):
    userId: int
    id: int
    nameBaseColorMasterIds: Optional[Any] = None


class IconFrameModel(BaseModel):
    userId: int
    id: int
    iconFrameMasterIds: Optional[Any] = None


class GachaReRollModel(BaseModel):
    userId: int
    gachaMasterId: int
    rollCount: int
    isDecided: bool


class TrialPartyEventModel(BaseModel):
    userId: int
    id: int
    trialPartyEventMasterId: int
    currentStageOrder: int
    isCompleted: bool


class TrialPartyEventStageModel(BaseModel):
    userId: int
    id: int
    trialPartyEventStageMasterId: int
    isCleared: bool


class TrialPartyEventStagePartyModel(BaseModel):
    userId: int
    id: int
    trialPartyEventStageMasterId: int
    leaderPosition: int


class TrialPartyEventStagePartySlotModel(BaseModel):
    userId: int
    id: int
    trialPartyEventStagePartyId: int
    position: int
    trialPartyCharacterMasterId: int
    trialPartyPosterMasterId: Optional[int] = None
    trialPartyAccessoryMasterId: Optional[int] = None


class UserBlockModel(BaseModel):
    userId: int
    id: int
    blockUserId: Optional[str] = None


class AccessoryAutoSellModel(BaseModel):
    userId: int
    id: int
    autoSellRarity: int


class FavoriteCostumeModel(BaseModel):
    userId: int
    id: int
    characterBaseMasterId: int
    favoriteCostumeMasterIds: Optional[Any] = None


class BuffItemStatusModel(BaseModel):
    userId: int
    id: int
    effectType: int
    buffItemMasterId: int
    validUntil: int


class MultiRoomBasicModel(BaseModel):
    userId: int
    id: int
    ownerMultiRoomId: Optional[str] = None


class EventCampModel(BaseModel):
    userId: int
    id: int
    eventMasterId: int
    campType: int
    totalSupportPoint: int


__all__ = ["AccountModel"] + [
    "UserModel",
    "UserProfileModel",
    "UserPreferenceModel",
    "HomeDisplayPreferenceModel",
    "CharacterModel",
    "CharacterBaseModel",
    "PartyModel",
    "CharacterMasterModel",
    "CharacterBaseMasterModel",
    "CharacterLevelMasterModel",
    "PosterModel",
    "AccessoryLevelPatternGroupMasterModel",
    "AccessoryLevelPatternMasterModel",
    "AccessoryMasterModel",
    "EpisodeMasterModel",
    "EpisodeRewardPackageMasterModel",
    "LiveMasterModel",
    "MusicMasterModel",
    "SenseMasterModel",
    "StoryMasterModel",
    "PosterLevelPatternGroupMasterModel",
    "PosterLevelPatternMasterModel",
    "PosterMasterModel",
    "LiveModel",
    "MusicModel",
    "AccessoryModel",
    "ItemModel",
    "AccessoryEffectMasterModel",
    "CompanyMasterModel",
    "EffectDurationGroupMasterModel",
    "EffectMasterModel",
    "ItemMasterModel",
    "RandomEffectGroupMasterModel",
    "RewardRuleMasterModel",
    "SenseEffectMasterModel",
    "TrophyGroupMasterModel",
    "TrophyMasterModel",
    "CharacterLessonModel",
    "DailyLessonModel",
    "InboxModel",
    "BombModel",
    "CostumeModel",
    "NameColorModel",
    "NameplateModel",
    "NoteModel",
    "MissionModel",
    "AuditionMasterModel",
    "BombMasterModel",
    "CharacterStarRankMasterModel",
    "CharacterStarRankRewardGroupMasterModel",
    "CostumeMasterModel",
    "HomeCharacterVoiceMasterModel",
    "NameColorMasterModel",
    "NameplateMasterModel",
    "NoteMasterModel",
    "SpotConversationMasterModel",
    "StampMasterModel",
    "CharacterLessonSlotModel",
    "TrophyModel",
    "MarketModel",
    "ViewedShopModel",
    "UserBonusModel",
    "AuditionPhaseMasterModel",
    "AuditionRewardPackageMasterModel",
    "CampaignMasterModel",
    "CharacterAwakeningItemMasterModel",
    "CharacterBloomBonusGroupMasterModel",
    "CharacterBloomItemMasterModel",
    "CharacterExperienceItemMasterModel",
    "CharacterMissionMasterModel",
    "CharacterMissionStageMasterModel",
    "CharacterPieceMasterModel",
    "CharacterSenseEnhanceItemGroupMasterModel",
    "CostumeWearableCharacterGroupMasterModel",
    "ExchangeShopMasterModel",
    "LiveSettingMasterModel",
    "MissionMasterModel",
    "MusicVocalVersionMasterModel",
    "PosterReleaseItemGroupMasterModel",
    "PosterReleaseItemMasterModel",
    "PosterStoryMasterModel",
    "StarRankRewardMasterModel",
    "AuditionClearModel",
    "SpRateModel",
    "NotificationModel",
    "EpisodeModel",
    "CharacterMissionModel",
    "MissionPassModel",
    "MissionPassDetailMasterModel",
    "MissionPassMasterModel",
    "LeagueBasicModel",
    "StoryEventModel",
    "ExchangeLimitModel",
    "LeagueGroupModel",
    "LeagueGroupMemberModel",
    "LeagueHistoryModel",
    "JewelShopModel",
    "DailyLimitModel",
    "LeagueHighScorePartyModel",
    "LeagueHighScorePartySlotModel",
    "StoryEventCircleModel",
    "StoryEventCircleMissionModel",
    "StoryEventCircleMissionRewardModel",
    "StoryEventHighScoreBuffSettingModel",
    "StoryEventHighScorePartyModel",
    "StoryEventHighScorePartySlotModel",
    "ConnectWithAccountModel",
    "ConnectWithPasswordModel",
    "TournamentDetailModel",
    "GradualMissionGroupModel",
    "PhotoModel",
    "AlbumModel",
    "AlbumPageModel",
    "StarPassStatusModel",
    "LoginPassStatusModel",
    "CurrencyModel",
    "DecorationModel",
    "LiveAchievementModel",
    "MusicVideoModel",
    "TheaterStoryModel",
    "LiveDropCellingModel",
    "StoryEventHighScoreModel",
    "ComicModel",
    "ComebackCampaignModel",
    "ConcertStageModel",
    "LimitModel",
    "GachaSelectedThingModel",
    "TotalPointEventModel",
    "EventBoxGachaModel",
    "EventBoxGachaBoxThingModel",
    "SpecialEventModel",
    "CharacterPointEventModel",
    "AnotherNotationModel",
    "MusicBookmarkModel",
    "LiveDropLimitModel",
    "RestrictionModel",
    "PermanentMarketThingModel",
    "TimeLimitedControlModel",
    "FlashSaleStageModel",
    "AlbumThemeModel",
    "CircleEventMissionModel",
    "PickupCharacterMissionModel",
    "LeagueSeasonResultModel",
    "EventModel",
    "BonusLiveModel",
    "BonusLiveStageModel",
    "RouletteEventModel",
    "RouletteModel",
    "HomeBGMModel",
    "LinkCharacterModel",
    "MusicCourseModel",
    "TournamentQualifyingModel",
    "LotteryModel",
    "TripleCastPartyModel",
    "TripleCastPartySlotModel",
    "TripleCastBasicModel",
    "TripleCastGroupModel",
    "TripleCastGroupMemberModel",
    "TripleCastHighScorePartyModel",
    "TripleCastHighScorePartySlotModel",
    "TripleCastSeasonResultModel",
    "AlbumPresetModel",
    "GachaModel",
    "TripleCastHistoryModel",
    "DugongRunModel",
    "MusicCourseRankingModel",
    "FriendInvitationModel",
    "FriendInvitationMissionModel",
    "NameBaseColorModel",
    "IconFrameModel",
    "GachaReRollModel",
    "TrialPartyEventModel",
    "TrialPartyEventStageModel",
    "TrialPartyEventStagePartyModel",
    "TrialPartyEventStagePartySlotModel",
    "UserBlockModel",
    "AccessoryAutoSellModel",
    "FavoriteCostumeModel",
    "BuffItemStatusModel",
    "MultiRoomBasicModel",
    "EventCampModel",
]
