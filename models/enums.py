from enum import IntEnum


class AccountDeletionErrorTypes(IntEnum):
    None_ = 0
    EnrolledCircle = 1


class AccountRegisterErrorTypes(IntEnum):
    None_ = 0
    NgWord = 1
    TooManyRegistrations = 2


class AchievementRateGrades(IntEnum):
    None_ = 0
    C = 1
    B = 2
    A = 3
    APlus = 4
    S = 5
    SPlus = 6
    SS = 7
    SSPlus = 8
    SSS = 9


class ActivityLogTypes(IntEnum):
    None_ = 0
    JoinCircle = 1
    LeaveCircle = 2
    ChangedPosition = 3
    GachaAcquiredCharacter = 4
    GachaAcquiredPoster = 5
    PlayerRate = 6
    FirstClearedAllPerfect = 7
    FirstClearedFullCombo = 8
    DonateSupportLevelLimit = 9
    ReleaseSupportLevelLimit = 10


class Attributes(IntEnum):
    Cute = 1
    Cool = 2
    Colorful = 3
    Cheerful = 4


class AuthenticationProviders(IntEnum):
    Google = 1
    Apple = 2


class BanLevels(IntEnum):
    Normal = 0
    Warning = 1
    Suspend = 2
    Delete = 3


class BloomBonusTypes(IntEnum):
    None_ = 0
    EffectDuringLive = 1
    StatusBonus = 2
    GrantItem = 3


class BonusAbilityEnableFlags(IntEnum):
    None_ = 0
    First = 1
    Second = 2
    Third = 4
    Fourth = 8
    Fifth = 16
    All = 31


class BranchConditionType(IntEnum):
    None_ = 0
    StarActFireCount = 1
    PartyPosition = 2
    CompanyMemberCount = 3
    CompanyCount = 4
    AttributeMemberCount = 5
    AttributeCount = 6
    PosterAppearanceMemberCount = 7
    LifeGuardCount = 8
    PosterAppearanceCompanyCount = 9
    StorageSenseLightCount = 10
    CharacterBaseGroup = 11
    SenseTriggeredCount = 12


class BranchConditionTypes(IntEnum):
    None_ = 0
    StarActFireCount = 1
    PartyPosition = 2
    CompanyMemberCount = 3
    CompanyCount = 4
    AttributeMemberCount = 5
    AttributeCount = 6
    PosterAppearanceMemberCount = 7
    LifeGuardCount = 8
    PosterAppearanceCompanyCount = 9
    StorageSenseLightCount = 10
    CharacterBaseGroup = 11
    SenseTriggeredCount = 12


class BranchJudgeTypes(IntEnum):
    None_ = 0
    Equal = 1
    MoreThan = 2
    LessThan = 3


class CalculationTypes(IntEnum):
    PercentageAddition = 1
    Multiplication = 2
    FixedAddition = 3


class CampTypes(IntEnum):
    None_ = 0
    Camp1 = 1
    Camp2 = 2


class CampaignEffectTypes(IntEnum):
    LiveReward = 1
    LessonReward = 2
    StarPoint = 3
    RankPoint = 4
    AccessoryDropRate = 5
    LessonCount = 6
    ForDisplay = 10


class CharacterBaseTypes(IntEnum):
    Initial = 1
    Collaboration = 900


class CharacterEpisodeOrder(IntEnum):
    None_ = 0
    First = 1
    Second = 2


class CharacterRarities(IntEnum):
    Rare1 = 1
    Rare2 = 2
    Rare3 = 3
    Rare4 = 4


class CharacterSelectionTypes(IntEnum):
    Primary = 1
    Secondary = 2
    Random = 99


class CircleAuthorities(IntEnum):
    None_ = 0
    Member = 1
    DeputyLeader = 2
    Leader = 3


class CircleAuthorityResultStatus(IntEnum):
    PermissionDenied = 1
    DeputyLeaderFullJoin = 2
    ChangeSuccess = 3
    LeaderChangeSuccess = 4
    DataNotFound = 5


class CircleAuthorityUpdateTypes(IntEnum):
    None_ = 0
    Promotion = 1
    Demotion = 2


class CircleDonateSupportCompanyResult(IntEnum):
    Success = 0
    ExceededQuantityReturned = 1
    Error = 99


class CircleResultStatus(IntEnum):
    RequestIllegal = 1
    LessThanNecessaryRank = 2
    CanJoinCircle = 3
    AlreadyJoinAnyCircle = 4
    AlreadyInvite = 5
    FreeEntry = 6
    AlreadyRequest = 7
    InviteSuccess = 8
    PreRequestSuccess = 9
    RequestSuccess = 10
    ApproveSuccess = 11
    JoinSuccess = 12
    EditSuccess = 13
    CreateSuccess = 14
    ExpulsionSuccess = 15
    ResignationSuccess = 16
    ReleaseSuccess = 17
    Error = 18
    DataNotFound = 19
    SearchSuccess = 20
    CancelSuccess = 21
    RejectSuccess = 22
    NgWord = 23
    MemberAmountUpperLimit = 24
    InvalidParameter = 25
    ReleaseFailureByEvent = 26


class ClearLamps(IntEnum):
    None_ = 0
    Clear = 1
    FullCombo = 2
    FullComboMulti1 = 3
    FullComboMulti2 = 4
    FullComboMulti3 = 5
    AllPerfect = 6
    AllPerfectMulti1 = 7
    AllPerfectMulti2 = 8
    AllPerfectMulti3 = 9


class Companies(IntEnum):
    None_ = 0
    Sirius = 1
    Eden = 2
    Gingaza = 3
    Denki = 4
    LoveLiveSunshine = 900


class DugongRunClearTypes(IntEnum):
    Failed = 0
    Clear = 1
    NoMisstake = 2


class EditTypes(IntEnum):
    SimpleEdit = 1
    DetailEdit = 2


class EffectConditions(IntEnum):
    CharacterBase = 1
    Company = 2
    Attribute = 3
    SenseType = 4
    Character = 5
    EquippedPoster = 6
    NeighborPosition = 7
    CharacterBaseGroup = 8


class EffectTargetRanges(IntEnum):
    None_ = 0
    Self = 1
    All = 2


class EffectTypes(IntEnum):
    BaseVocalUp = 1
    BaseExpressionUp = 2
    BaseConcentrationUp = 3
    BaseCorrection = 4
    VocalUp = 5
    ExpressionUp = 6
    ConcentrationUp = 7
    VocalLimitUp = 8
    ExpressionLimitUp = 9
    ConcentrationLimitUp = 10
    PerformanceUp = 11
    FinalPerformanceUpCancelSense = 12
    AddSenseLightSelf = 13
    AddSenseLightVariable = 14
    AddSenseLightSupport = 15
    AddSenseLightControl = 16
    AddSenseLightAmplification = 17
    AddSenseLightSpecial = 18
    ChangeWrongLightToSpLight = 19
    SenseRecastDown = 20
    SenseCoolTimeRecastDown = 21
    SenseAlternative = 22
    ScoreUpByHighLife = 23
    ScoreUpByLowLife = 24
    ScoreUpByBuff = 25
    BuffTimeExtend = 26
    LifeHealing = 27
    LifeFixedValue = 28
    LifeGuard = 29
    SenseScoreUp = 30
    StarActScoreUp = 31
    BaseScoreUp = 32
    ScoreGainOnScore = 33
    ScoreGainOnVocal = 34
    ScoreGainOnExpression = 35
    ScoreGainOnConcentration = 36
    PrincipalGaugeGain = 37
    RewardUp = 38
    LightGuard = 39
    PrincipalGaugeUp = 40
    PrincipalGaugeLimitUp = 41
    DecreaseRequireSupportLight = 42
    DecreaseRequireControlLight = 43
    DecreaseRequireAmplificationLight = 44
    DecreaseRequireSpecialLight = 45
    PerformanceLimitUp = 46
    ScoreGainOnPerformance = 47
    PrincipalGaugeBonus = 48
    PerformanceDuplicateUp = 49
    CombinationSense = 50
    PlayerRankPointUp = 51
    PrincipalGaugeGainPercentageOfLimit = 52
    StarActProcrastinate = 53


class EntryTypes(IntEnum):
    None_ = 0
    Free = 1
    Approval = 2


class EpisodeReleaseConditionTypes(IntEnum):
    TotalRankInCompany = 1
    CharacterRank = 2


class FireTimingTypes(IntEnum):
    StarAct = 1
    Sense = 2
    StartLive = 3
    Passive = 4


class FriendAcceptResultStatus(IntEnum):
    AcceptSuccess = 1
    RequestUserFriendsLimitOver = 2
    AcceptUserFriendsLimitOver = 3
    Canceled = 4


class FriendRequestResultStatus(IntEnum):
    RequestSuccess = 1
    IsFriends = 2
    IsApplying = 3
    IsMySelf = 4
    DataNotFound = 5
    IsFriendCountLimit = 6


class FriendSearchResultStatus(IntEnum):
    Friend = 1
    Request = 2
    None_ = 3
    User = 4
    ReceivedRequest = 5


class GachaCardTypes(IntEnum):
    Character = 1
    Poster = 2


class GachaEmissionFlags(IntEnum):
    Rare2 = 1
    Rare3 = 2
    Rare4 = 4


class GameVersions(IntEnum):
    Unknown = 0
    AppStore = 1
    GooglePlay = 2


class HighScoreTypes(IntEnum):
    Normal = 0
    Multi = 1
    TheaterLeague = 2
    Audition = 3


class HomeBGMSelectionTypes(IntEnum):
    UserSelect = 1
    Random = 2


class HomeCharacterDisplayTypes(IntEnum):
    CharacterModel = 0
    Illust = 1


class InvitationCodeResultStatuses(IntEnum):
    Success = 0
    InvalidInvitationCode = 1
    OwnInvitationCode = 2
    InviteUserNotFound = 3


class ItemCategories(IntEnum):
    StaminaRecovery = 11
    CharacterLevel = 12
    ConsumeItem = 13
    TalentBloom = 14
    CharacterMission = 16
    GachaTicket = 21
    ExchangeTicket = 22
    RouletteBall = 31
    ScratchCoin = 32
    GachaPoint = 41
    EventPoint = 42
    MissionPassPoint = 43
    Film = 51
    AlbumSkin = 52
    PlayerRankAwakening = 61
    LessonPartyQuantityLimitRelease = 62
    BuffItem = 71


class JumpTypes(IntEnum):
    None_ = 0
    Information = 1
    Shop = 2
    JewelShop = 3
    Gacha = 4
    Event = 5
    Live = 6
    Member = 7
    Photo = 8
    Story = 9
    WebLink = 10
    BeginnerMission = 11
    MusicShop = 12
    Spot = 13
    Mission = 14
    Concert = 15
    StarRank = 16
    Episode = 17
    SpecialEvent = 18
    TotalPointEventRanking = 19
    BoxGacha = 20
    TournamentEventTop = 21
    Lesson = 22
    League = 23


class LeagueClassChangeTypes(IntEnum):
    None_ = 0
    Up = 1
    Keep = 2
    Down = 3


class LeagueClassTypes(IntEnum):
    None_ = 0
    Rookie = 1
    Hope = 2
    Cast = 3
    Elite = 4
    Veteran = 5
    Star = 6
    DaiStar = 7


class LiveDropTypes(IntEnum):
    Normal = 0
    Special = 1


class LiveReleaseStatus(IntEnum):
    None_ = 0
    AvailableInShop = 1
    Playable = 2


class LiveTypes(IntEnum):
    Normal = 1
    Multi = 2
    Lesson = 3
    Audition = 4
    League = 5
    MultiCollectionEvent = 6
    Concert = 7
    BonusLive = 8
    CourseMode = 9
    TripleCast = 10
    GhostLive = 11
    Trial = 12
    MultiRoom = 13


class LiveUnlockConditionTypes(IntEnum):
    None_ = 0
    ExtraGoodCount = 13
    NotationShop = 14


class LoginBonusLayoutTypes(IntEnum):
    Normal = 1
    Special = 2


class LoginBonusSpineSelectType(IntEnum):
    Random = 1
    HomeCharacterBaseId = 2
    SelectedSpineCostume = 3


class LoginBonusTypes(IntEnum):
    Normal = 1
    Special = 2
    Comeback = 3


class LoginPassNotificationTypes(IntEnum):
    None_ = 0
    Purchasable = 1
    Invalided = 2


class MatchingResult(IntEnum):
    Win = 0
    Lose = 1
    Draw = 2


class MissionCategories(IntEnum):
    Beginner = 1
    Normal = 2
    Limit = 3
    Daily = 4
    Weekly = 5
    SiriusDay = 6
    TheaterSirius = 11
    TheaterEden = 12
    TheaterGingaza = 13
    TheaterDenki = 14


class MissionPassRewardStatus(IntEnum):
    NotReceived = 1
    Received = 2
    NotPaidSpItem = 3
    NotReachedPoint = 4
    ReceiveSuccess = 5


class MultiRoomPlayModes(IntEnum):
    AchievementRate = 0
    Score = 1


class MusicBookmarkFlags(IntEnum):
    None_ = 0
    Bookmark1 = 1
    Bookmark2 = 2
    Bookmark3 = 4


class MusicCourseCertificationGrade(IntEnum):
    None_ = 0
    Failed = 1
    NormalGaugeCertificate = 2
    HotGaugeCertificate = 3


class MusicCourseGaugeType(IntEnum):
    Normal = 0
    Hot = 1


class MusicCoverTypes(IntEnum):
    Original = 1
    Cover = 2


class MusicDifficulties(IntEnum):
    None_ = 0
    Normal = 1
    Hard = 2
    Extra = 3
    Stella = 4
    Olivier = 5


class MusicUnlockConditionTypes(IntEnum):
    Default = 1
    Distribute = 2
    Buy = 10
    ReadEpisodeAndBuy = 11
    ClearAudition = 12


class MusicVideoTypes(IntEnum):
    None_ = 0
    RealTimeRendering = 1
    Movie = 2


class NamePlateChangeTypes(IntEnum):
    None_ = 0
    DaiStarEnrollCount = 1
    TripleCastDaiStarEnrollCount = 2


class NotificationCategory(IntEnum):
    Notification = 1
    Update = 2
    Campaign = 3
    Event = 4
    Gacha = 5
    Bug = 6


class NotificationTabCategory(IntEnum):
    Important = 1
    UpdateInformation = 2
    BugInformation = 3


class OlivierReleaseStatuses(IntEnum):
    None_ = 0
    Challengeable = 1
    Purchasable = 2
    Released = 3


class PageCategories(IntEnum):
    TutorialIngame = 1
    Spot = 2
    Photo = 3
    Circle = 4
    Lesson = 5
    AuditionTop = 6
    AuditionConfirm = 7
    League = 8
    SpecialLive = 9
    MultiLive = 10
    LiveResult = 11
    OlivierLiveResult = 12
    Party = 13
    Enhancement = 14
    Costume = 15
    StarRank = 16
    SideStory = 17
    TrophyAndProfile = 18
    Shop = 19
    MedalExchangeShop = 20
    BeginnerMission = 21
    StaminaConsumption = 22
    CompanyIntroMovieSirius = 24
    CompanyIntroMovieEden = 25
    CompanyIntroMovieGingaza = 26
    CompanyIntroMovieDenki = 27
    SpotStoryArchive = 28
    PhotoTop = 29
    TeamChallenge = 30
    ActorPortal = 31
    MusicSelection = 32
    ConcertStageSelect = 33
    AlbumTop = 34
    CircleEvent = 35
    TournamentEventTop = 36
    CourseModeSelection = 37
    TripleCastLeague = 38
    TournamentCourseModeSelection = 39
    GhostLive = 40
    TrialPartyEvent = 41
    StellaConcours = 42
    MultiRoom = 43


class PhotoRarities(IntEnum):
    Rare1 = 1
    Rare2 = 2
    Rare3 = 3
    Rare4 = 4
    Rare5 = 5


class PlayTimeTypes(IntEnum):
    None_ = -1
    Zero = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Eleven = 11
    Twelve = 12
    Thirteen = 13
    Fourteen = 14
    Fifteen = 15
    Sixteen = 16
    Seventeen = 17
    Eighteen = 18
    Nineteen = 19
    Twenty = 20
    TwentyOne = 21
    TwentyTwo = 22
    TwentyThree = 23
    TwentyFour = 24
    TwentyFive = 25
    TwentySix = 26
    TwentySeven = 27
    TwentyEight = 28
    TwentyNine = 29


class PossessionRarities(IntEnum):
    R = 1
    SR = 2
    SSR = 3


class PossessionRarityFlag(IntEnum):
    None_ = 0
    R = 2
    SR = 4
    SSR = 8


class PosterEpisodeTypes(IntEnum):
    Information = 0
    Chapter1 = 1
    Chapter2 = 2
    Chapter3 = 3
    Chapter4 = 4
    AfterTalk = 5
    Sirius = 6
    Eden = 7
    Gingaza = 8
    Denki = 9


class PosterOrientation(IntEnum):
    Portrait = 1
    Landscape = 2


class PosterSubTitleDisplayConditions(IntEnum):
    None_ = 0
    BreakThroughPhase = 1


class ProcessPaymentTransactionResult(IntEnum):
    Success = 1
    TemporaryIssuesTryAgain = 2
    Failed = 3
    CouldNotConfirm = 4
    CouldNotAcknowledge = 5
    Pending = 6


class SearchCircleMemberConditionTypes(IntEnum):
    None_ = 0
    OneToFive = 1
    SixToNine = 2


class SenseFirePriority(IntEnum):
    Primary = 1
    Secondary = 2


class SenseLightTypes(IntEnum):
    Variable = 0
    Support = 1
    Control = 2
    Amplification = 3
    Special = 4


class SenseTypes(IntEnum):
    Support = 1
    Control = 2
    Amplification = 3
    Special = 4
    None_ = 9
    Alternative = 10


class ShopCategories(IntEnum):
    None_ = 0
    Normal = 1
    Medal = 2
    Event = 3
    Gacha = 4
    Special = 5
    Music = 6


class ShopReplaceTypes(IntEnum):
    None_ = 0
    Daily = 1
    Weekly = 2
    Monthly = 3
    DailyPassExpired = 10


class ShopUnlockTypes(IntEnum):
    ReadStory = 2
    RateReached = 8
    ClassReached = 9
    BuyItem = 10
    ReadFirstMainStory = 11
    AuditionReached = 12
    SelectedPickup = 17
    NotInPossession = 20


class SpotTypes(IntEnum):
    UtagawaHighSchool = 1
    HigashiUenoHighSchool = 2
    Park = 3
    Cafe = 4
    ElectricTown = 5
    ThemePark = 6


class StampType(IntEnum):
    Default = 1
    Animation = 2


class StarPassTypes(IntEnum):
    StarPass = 1
    DaiStarPass = 2


class StoryTypes(IntEnum):
    None_ = 0
    Main = 1
    Event = 2
    Side = 3
    Character = 4
    Special = 5


class TabCategories(IntEnum):
    Hidden = 0
    Normal = 1
    Raise = 2
    Ticket = 3
    Piece = 4


class TalentBloomItemTypes(IntEnum):
    ActorPiece = 1
    ActorDaiPiece = 2


class ThingTypes(IntEnum):
    Item = 1
    Character = 2
    Poster = 3
    Accessory = 4
    Costume = 5
    Trophy = 6
    Stamp = 7
    Nameplate = 8
    NameColor = 9
    Bomb = 10
    Note = 11
    Coin = 12
    Jewel = 13
    Music = 14
    Stamina = 15
    Decoration = 16
    AlbumTheme = 17
    NameBaseColor = 18
    IconFrame = 19
    HomeSkin = 20


class TimingTypes(IntEnum):
    None_ = 0
    MISS = 1
    BAD = 2
    GOOD = 3
    GREAT = 4
    PERFECT = 5
    PERFECT_STAR = 6


class TriggerType(IntEnum):
    OverLife = 1
    BelowLife = 2
    CharacterBase = 3
    Company = 4
    Attribute = 5
    SenseType = 6
    CompanyCount = 7
    AttributeCount = 8
    CharacterBaseGroup = 9
    AllMemberBelongingCompany = 10
    MaxMemberBelongingCompanyCount = 11
    MaxMemberBelongingAttributeCount = 12


class TriggerTypes(IntEnum):
    OverLife = 1
    BelowLife = 2
    CharacterBase = 3
    Company = 4
    Attribute = 5
    SenseType = 6
    CompanyCount = 7
    AttributeCount = 8
    CharacterBaseGroup = 9
    AllMemberBelongingCompany = 10
    MaxMemberBelongingCompanyCount = 11
    MaxMemberBelongingAttributeCount = 12


class TripleCastGroupOrder(IntEnum):
    First = 0
    Second = 1
    Third = 2


class TrophyCategories(IntEnum):
    Character = 1
    Achievement = 2
    Event = 3
    Other = 4


class TutorialStatus(IntEnum):
    Start = 0
    TutorialDownLoad = 1
    MainScenario = 2
    TheaterMovie = 3
    Home = 4
    InGame = 5
    MiniTalk = 6
    Finish = 99


class UseDecoPageFlag(IntEnum):
    None_ = 0
    Page1 = 1
    Page2 = 2
    Page3 = 4
    Page4 = 8
    Page5 = 16
    Page6 = 32
    Page7 = 64
    Page8 = 128
    Page9 = 256
    Page10 = 512


class ViewedShopCategoryTypes(IntEnum):
    ExchangeShop = 0
    Music = 1
    Live = 2
    Gacha = 3
    Market = 4


__all__ = [
    "AccountDeletionErrorTypes",
    "AccountRegisterErrorTypes",
    "AchievementRateGrades",
    "ActivityLogTypes",
    "Attributes",
    "AuthenticationProviders",
    "BanLevels",
    "BloomBonusTypes",
    "BonusAbilityEnableFlags",
    "BranchConditionType",
    "BranchConditionTypes",
    "BranchJudgeTypes",
    "CalculationTypes",
    "CampTypes",
    "CampaignEffectTypes",
    "CharacterBaseTypes",
    "CharacterEpisodeOrder",
    "CharacterRarities",
    "CharacterSelectionTypes",
    "CircleAuthorities",
    "CircleAuthorityResultStatus",
    "CircleAuthorityUpdateTypes",
    "CircleDonateSupportCompanyResult",
    "CircleResultStatus",
    "ClearLamps",
    "Companies",
    "DugongRunClearTypes",
    "EditTypes",
    "EffectConditions",
    "EffectTargetRanges",
    "EffectTypes",
    "EntryTypes",
    "EpisodeReleaseConditionTypes",
    "FireTimingTypes",
    "FriendAcceptResultStatus",
    "FriendRequestResultStatus",
    "FriendSearchResultStatus",
    "GachaCardTypes",
    "GachaEmissionFlags",
    "GameVersions",
    "HighScoreTypes",
    "HomeBGMSelectionTypes",
    "HomeCharacterDisplayTypes",
    "InvitationCodeResultStatuses",
    "ItemCategories",
    "JumpTypes",
    "LeagueClassChangeTypes",
    "LeagueClassTypes",
    "LiveDropTypes",
    "LiveReleaseStatus",
    "LiveTypes",
    "LiveUnlockConditionTypes",
    "LoginBonusLayoutTypes",
    "LoginBonusSpineSelectType",
    "LoginBonusTypes",
    "LoginPassNotificationTypes",
    "MatchingResult",
    "MissionCategories",
    "MissionPassRewardStatus",
    "MultiRoomPlayModes",
    "MusicBookmarkFlags",
    "MusicCourseCertificationGrade",
    "MusicCourseGaugeType",
    "MusicCoverTypes",
    "MusicDifficulties",
    "MusicUnlockConditionTypes",
    "MusicVideoTypes",
    "NamePlateChangeTypes",
    "NotificationCategory",
    "NotificationTabCategory",
    "OlivierReleaseStatuses",
    "PageCategories",
    "PhotoRarities",
    "PlayTimeTypes",
    "PossessionRarities",
    "PossessionRarityFlag",
    "PosterEpisodeTypes",
    "PosterOrientation",
    "PosterSubTitleDisplayConditions",
    "ProcessPaymentTransactionResult",
    "SearchCircleMemberConditionTypes",
    "SenseFirePriority",
    "SenseLightTypes",
    "SenseTypes",
    "ShopCategories",
    "ShopReplaceTypes",
    "ShopUnlockTypes",
    "SpotTypes",
    "StampType",
    "StarPassTypes",
    "StoryTypes",
    "TabCategories",
    "TalentBloomItemTypes",
    "ThingTypes",
    "TimingTypes",
    "TriggerType",
    "TriggerTypes",
    "TripleCastGroupOrder",
    "TrophyCategories",
    "TutorialStatus",
    "UseDecoPageFlag",
    "ViewedShopCategoryTypes",
]
