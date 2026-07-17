"""Auto-generated request/response models for the WDS API.

263 MessagePack DTOs + 69 enums, extracted from Sirius.Entity /
Sirius.ApiClient (app 2.31.0). Each DTO serializes as a MessagePack array indexed by
its [Key(n)] number (gaps -> nil); base-class keys are merged in. Decode responses
with ``Model.from_array(arr)``. ``_FIELDS`` = ((key, name, base_type, is_array, kind), ...).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, List, Optional

from .models import MODEL_REGISTRY, ENUM_REGISTRY, MsgpackModel


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


class BonusAbilityEnableFlags(IntEnum):
    None_ = 0
    First = 1
    Second = 2
    Third = 4
    Fourth = 8
    Fifth = 16
    All = 31


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


class CampTypes(IntEnum):
    None_ = 0
    Camp1 = 1
    Camp2 = 2


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


class MusicCourseGaugeType(IntEnum):
    Normal = 0
    Hot = 1


class MusicDifficulties(IntEnum):
    None_ = 0
    Normal = 1
    Hard = 2
    Extra = 3
    Stella = 4
    Olivier = 5


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


class TutorialStatus(IntEnum):
    Start = 0
    TutorialDownLoad = 1
    MainScenario = 2
    TheaterMovie = 3
    Home = 4
    InGame = 5
    MiniTalk = 6
    Finish = 99


class ViewedShopCategoryTypes(IntEnum):
    ExchangeShop = 0
    Music = 1
    Live = 2
    Gacha = 3
    Market = 4


@dataclass
class AbilityVarietyUpPayload(MsgpackModel):
    photo_id: Optional[int] = None
    variety_to: Optional[int] = None
    item_master_id: Optional[int] = None

    _FIELDS = (
        (0, "photo_id", "long", False, "prim"),
        (1, "variety_to", "int", False, "prim"),
        (2, "item_master_id", "long", False, "prim"),
    )


@dataclass
class AccessoryAutoSellConvertThing(MsgpackModel):
    accessory_master_id: Optional[int] = None
    convert_thing: Optional["ReceivedThing"] = None

    _FIELDS = (
        (0, "accessory_master_id", "long", False, "prim"),
        (1, "convert_thing", "ReceivedThing", False, "model"),
    )


@dataclass
class AccessoryFavoritePayload(MsgpackModel):
    accessory_id: Optional[int] = None
    set_favorite: Optional[bool] = None

    _FIELDS = (
        (0, "accessory_id", "long", False, "prim"),
        (1, "set_favorite", "bool", False, "prim"),
    )


@dataclass
class AccountConnectPayload(MsgpackModel):
    provider: Optional[int] = None
    token: Optional[str] = None

    _FIELDS = (
        (0, "provider", "AuthenticationProviders", False, "enum"),
        (1, "token", "string", False, "prim"),
    )


@dataclass
class AccountDeletionResult(MsgpackModel):
    is_success: Optional[bool] = None
    error: Optional[int] = None

    _FIELDS = (
        (0, "is_success", "bool", False, "prim"),
        (1, "error", "AccountDeletionErrorTypes", False, "enum"),
    )


@dataclass
class AccountRegistResult(MsgpackModel):
    token: Optional[str] = None
    error_type: Optional[int] = None

    _FIELDS = (
        (0, "token", "string", False, "prim"),
        (1, "error_type", "AccountRegisterErrorTypes", False, "enum"),
    )


@dataclass
class AcquirableThing(MsgpackModel):
    id_: Optional[int] = None
    quantity: Optional[int] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (1, "quantity", "int", False, "prim"),
    )


@dataclass
class AcquirableThingsPayload(MsgpackModel):
    things: Optional[List["AcquirableThing"]] = None

    _FIELDS = ((0, "things", "AcquirableThing", True, "model"),)


@dataclass
class ActorPortalCharacterPayload(MsgpackModel):
    character_base_id: Optional[int] = None
    character_id: Optional[int] = None
    is_awakening: Optional[bool] = None

    _FIELDS = (
        (0, "character_base_id", "long", False, "prim"),
        (1, "character_id", "long", False, "prim"),
        (2, "is_awakening", "bool", False, "prim"),
    )


@dataclass
class AlbumArrangingPayload(MsgpackModel):
    publishing: Optional[bool] = None
    page: Optional[int] = None
    items: Optional[List[int]] = None
    m_album_theme_id: Optional[int] = None

    _FIELDS = (
        (0, "publishing", "bool", False, "prim"),
        (1, "page", "int", False, "prim"),
        (2, "items", "byte", True, "prim"),
        (3, "m_album_theme_id", "long", False, "prim"),
    )


@dataclass
class AlbumPageResult(MsgpackModel):
    album_page_id: Optional[int] = None
    album_id: Optional[int] = None
    level: Optional[int] = None
    page: Optional[int] = None
    edit_type: Optional[int] = None
    publishing: Optional[bool] = None
    items: Optional[List[int]] = None
    album_theme_master_id: Optional[int] = None

    _FIELDS = (
        (0, "album_page_id", "long", False, "prim"),
        (1, "album_id", "long", False, "prim"),
        (2, "level", "int", False, "prim"),
        (3, "page", "int", False, "prim"),
        (4, "edit_type", "EditTypes", False, "enum"),
        (5, "publishing", "bool", False, "prim"),
        (6, "items", "byte", True, "prim"),
        (7, "album_theme_master_id", "long", False, "prim"),
    )


@dataclass
class AlbumPageSearchResult(MsgpackModel):
    album_page_result: Optional["AlbumPageResult"] = None
    is_success: Optional[bool] = None

    _FIELDS = (
        (0, "album_page_result", "AlbumPageResult", False, "model"),
        (1, "is_success", "bool", False, "prim"),
    )


@dataclass
class AlbumPhotoPayload(MsgpackModel):
    photo_id: Optional[int] = None
    order: Optional[int] = None

    _FIELDS = (
        (0, "photo_id", "long", False, "prim"),
        (1, "order", "int", False, "prim"),
    )


@dataclass
class AuditionClearParty(MsgpackModel):
    id_: Optional[int] = None
    score: Optional[int] = None
    difficulty: Optional[int] = None
    slots: Optional[List["AuditionClearPartySlot"]] = None
    user_name: Optional[str] = None
    rate_grade: Optional[int] = None
    player_rank: Optional[str] = None
    leader_position: Optional[int] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (1, "score", "long", False, "prim"),
        (2, "difficulty", "MusicDifficulties", False, "enum"),
        (3, "slots", "AuditionClearPartySlot", True, "model"),
        (4, "user_name", "string", False, "prim"),
        (5, "rate_grade", "AchievementRateGrades", False, "enum"),
        (9, "player_rank", "string", False, "prim"),
        (10, "leader_position", "int", False, "prim"),
    )


@dataclass
class AuditionClearPartySlot(MsgpackModel):
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
    current_status: Optional["Status"] = None
    character_display_awakening_status: Optional[bool] = None

    _FIELDS = (
        (0, "position", "int", False, "prim"),
        (1, "character_master_id", "long", False, "prim"),
        (2, "character_level", "int", False, "prim"),
        (3, "character_talent_stage", "int", False, "prim"),
        (4, "character_awakening_phase", "int", False, "prim"),
        (5, "poster_master_id", "long", False, "prim"),
        (6, "poster_level", "int", False, "prim"),
        (7, "poster_breakthrough_phase", "int", False, "prim"),
        (8, "accessory_master_id", "long", False, "prim"),
        (9, "accessory_level", "int", False, "prim"),
        (10, "star_rank", "int", False, "prim"),
        (11, "talent_stage", "int", False, "prim"),
        (12, "awakening_phase", "long", False, "prim"),
        (13, "current_status", "Status", False, "model"),
        (14, "character_display_awakening_status", "bool", False, "prim"),
    )


@dataclass
class AuditionClearedInformationParties(MsgpackModel):
    parties: Optional[List["AuditionClearParty"]] = None
    cleared_phase: Optional[int] = None

    _FIELDS = (
        (0, "parties", "AuditionClearParty", True, "model"),
        (1, "cleared_phase", "byte", False, "prim"),
    )


@dataclass
class AuditionClearedInformationResult(MsgpackModel):
    parties_phases: Optional[List["AuditionClearedInformationParties"]] = None

    _FIELDS = (
        (0, "parties_phases", "AuditionClearedInformationParties", True, "model"),
    )


@dataclass
class AuthenticatePayload(MsgpackModel):
    login_token: Optional[str] = None
    game_version: Optional[int] = None
    apk_hash: Optional[str] = None
    apk_application_signature: Optional[str] = None
    application_version: Optional[str] = None

    _FIELDS = (
        (0, "login_token", "string", False, "prim"),
        (1, "game_version", "GameVersions", False, "enum"),
        (2, "apk_hash", "string", False, "prim"),
        (3, "apk_application_signature", "string", False, "prim"),
        (4, "application_version", "string", False, "prim"),
    )


@dataclass
class AuthenticateResult(MsgpackModel):
    token: Optional[str] = None
    ban_level: Optional[int] = None
    warned_until: Optional[str] = None

    _FIELDS = (
        (0, "token", "string", False, "prim"),
        (1, "ban_level", "BanLevels", False, "enum"),
        (2, "warned_until", "DateTime", False, "prim"),
    )


@dataclass
class BannerPayload(MsgpackModel):
    circle_hashed_id: Optional[str] = None
    poster_master_id: Optional[int] = None
    x1: Optional[float] = None
    y1: Optional[float] = None
    x2: Optional[float] = None
    y2: Optional[float] = None
    rotation_angle: Optional[int] = None
    display_poster_string: Optional[bool] = None
    banner_ratio: Optional[float] = None

    _FIELDS = (
        (0, "circle_hashed_id", "string", False, "prim"),
        (1, "poster_master_id", "long", False, "prim"),
        (2, "x1", "float", False, "prim"),
        (3, "y1", "float", False, "prim"),
        (4, "x2", "float", False, "prim"),
        (5, "y2", "float", False, "prim"),
        (6, "rotation_angle", "int", False, "prim"),
        (7, "display_poster_string", "bool", False, "prim"),
        (8, "banner_ratio", "float", False, "prim"),
    )


@dataclass
class BaseScoreBlock(MsgpackModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    note_id: Optional[int] = None
    timing_type: Optional[int] = None
    combo: Optional[int] = None

    _FIELDS = (
        (0, "hash", "long", False, "prim"),
        (1, "score", "long", False, "prim"),
        (2, "life", "int", False, "prim"),
        (3, "note_id", "long", False, "prim"),
        (4, "timing_type", "TimingTypes", False, "enum"),
        (5, "combo", "int", False, "prim"),
    )


@dataclass
class BlockListResult(MsgpackModel):
    results: Optional[List["FriendResult"]] = None

    _FIELDS = ((0, "results", "FriendResult", True, "model"),)


@dataclass
class BonusLiveResult(MsgpackModel):
    rewards: Optional[List["ReceivedThing"]] = None

    _FIELDS = ((0, "rewards", "ReceivedThing", True, "model"),)


@dataclass
class BooleanResult(MsgpackModel):
    is_success: Optional[bool] = None

    _FIELDS = ((0, "is_success", "bool", False, "prim"),)


@dataclass
class BulkLevelUpPayload(MsgpackModel):
    character_id: Optional[int] = None
    order: Optional[int] = None

    _FIELDS = (
        (0, "character_id", "long", False, "prim"),
        (1, "order", "int", False, "prim"),
    )


@dataclass
class BulkReceivePayload(MsgpackModel):
    inbox_ids: Optional[List[int]] = None

    _FIELDS = ((0, "inbox_ids", "long", True, "prim"),)


@dataclass
class CalculateLessonTimeEventPayload(MsgpackModel):
    music_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None

    _FIELDS = (
        (0, "music_master_id", "long", False, "prim"),
        (1, "character_base_master_id", "long", False, "prim"),
    )


@dataclass
class CalculateTimeEventPayload(MsgpackModel):
    music_master_id: Optional[int] = None
    sense_notation_master_id: Optional[int] = None
    party_id: Optional[int] = None
    vocal_version: Optional[int] = None
    is_story_event_challenge: Optional[bool] = None

    _FIELDS = (
        (0, "music_master_id", "long", False, "prim"),
        (1, "sense_notation_master_id", "long", False, "prim"),
        (2, "party_id", "long", False, "prim"),
        (3, "vocal_version", "int", False, "prim"),
        (4, "is_story_event_challenge", "bool", False, "prim"),
    )


@dataclass
class ChangeNamePayload(MsgpackModel):
    name: Optional[str] = None

    _FIELDS = ((0, "name", "string", False, "prim"),)


@dataclass
class ChangePhotoAbilityPayload(MsgpackModel):
    photo_id: Optional[int] = None
    item_master_id: Optional[int] = None
    photo_effect_type_group_master_id: Optional[int] = None

    _FIELDS = (
        (0, "photo_id", "long", False, "prim"),
        (1, "item_master_id", "long", False, "prim"),
        (2, "photo_effect_type_group_master_id", "long", False, "prim"),
    )


@dataclass
class CharacterBaseStarPointResult(MsgpackModel):
    character_base_master_id: Optional[int] = None
    star_point_result: Optional["StarPointResult"] = None
    link_character_received_reward: Optional[List["ReceivedThing"]] = None

    _FIELDS = (
        (0, "character_base_master_id", "long", False, "prim"),
        (1, "star_point_result", "StarPointResult", False, "model"),
        (2, "link_character_received_reward", "ReceivedThing", True, "model"),
    )


@dataclass
class CharacterFavoritePayload(MsgpackModel):
    character_id: Optional[int] = None
    set_favorite: Optional[bool] = None

    _FIELDS = (
        (0, "character_id", "long", False, "prim"),
        (1, "set_favorite", "bool", False, "prim"),
    )


@dataclass
class CharacterLineupResult(MsgpackModel):
    normal_probabilities: Optional[List["CharacterRarityProbability"]] = None
    fixed_probabilities: Optional[List["CharacterRarityProbability"]] = None
    normal_lineup_items: Optional[List["GachaLineupItemProbability"]] = None
    fixed_lineup_items: Optional[List["GachaLineupItemProbability"]] = None

    _FIELDS = (
        (0, "normal_probabilities", "CharacterRarityProbability", True, "model"),
        (1, "fixed_probabilities", "CharacterRarityProbability", True, "model"),
        (2, "normal_lineup_items", "GachaLineupItemProbability", True, "model"),
        (3, "fixed_lineup_items", "GachaLineupItemProbability", True, "model"),
    )


@dataclass
class CharacterPointEventInformationResult(MsgpackModel):
    current_total_point: Optional[int] = None
    overall_rank: Optional[int] = None
    character_rank: Optional[int] = None

    _FIELDS = (
        (0, "current_total_point", "long", False, "prim"),
        (1, "overall_rank", "int", False, "prim"),
        (2, "character_rank", "int", False, "prim"),
    )


@dataclass
class CharacterPointEventRankingResult(MsgpackModel):
    raw_ranking: Optional[List["RawRankingWithLongPoint"]] = None
    user_profiles: Optional[List["UserProfile"]] = None

    _FIELDS = (
        (0, "raw_ranking", "RawRankingWithLongPoint", True, "model"),
        (1, "user_profiles", "UserProfile", True, "model"),
    )


@dataclass
class CharacterRank(MsgpackModel):
    m_character_base_id: Optional[int] = None
    rank: Optional[int] = None

    _FIELDS = (
        (0, "m_character_base_id", "long", False, "prim"),
        (1, "rank", "int", False, "prim"),
    )


@dataclass
class CharacterRarityProbability(MsgpackModel):
    rarity: Optional[int] = None
    probability: Optional[float] = None

    _FIELDS = (
        (0, "rarity", "CharacterRarities", False, "enum"),
        (1, "probability", "double", False, "prim"),
    )


@dataclass
class ChatworkSendMessagePayload(MsgpackModel):
    message: Optional[str] = None

    _FIELDS = ((0, "message", "string", False, "prim"),)


@dataclass
class CircleAuthorityChangePayload(MsgpackModel):
    circle_hashed_id: Optional[str] = None
    user_id: Optional[str] = None
    authority: Optional[int] = None

    _FIELDS = (
        (0, "circle_hashed_id", "string", False, "prim"),
        (1, "user_id", "string", False, "prim"),
        (2, "authority", "CircleAuthorities", False, "enum"),
    )


@dataclass
class CircleAuthorityResult(MsgpackModel):
    result_status: Optional[int] = None

    _FIELDS = ((0, "result_status", "CircleAuthorityResultStatus", False, "enum"),)


@dataclass
class CircleBanner(MsgpackModel):
    poster_master_id: Optional[int] = None
    x1: Optional[float] = None
    y1: Optional[float] = None
    x2: Optional[float] = None
    y2: Optional[float] = None
    rotation_angle: Optional[int] = None
    display_poster_string: Optional[bool] = None
    banner_ratio: Optional[float] = None

    _FIELDS = (
        (0, "poster_master_id", "long", False, "prim"),
        (1, "x1", "float", False, "prim"),
        (2, "y1", "float", False, "prim"),
        (3, "x2", "float", False, "prim"),
        (4, "y2", "float", False, "prim"),
        (5, "rotation_angle", "int", False, "prim"),
        (6, "display_poster_string", "bool", False, "prim"),
        (7, "banner_ratio", "float", False, "prim"),
    )


@dataclass
class CircleEventCircleMissionProgress(MsgpackModel):
    circle_event_mission_master_id: Optional[int] = None
    current_count: Optional[int] = None

    _FIELDS = (
        (0, "circle_event_mission_master_id", "long", False, "prim"),
        (1, "current_count", "long", False, "prim"),
    )


@dataclass
class CircleEventInformationResult(MsgpackModel):
    circle_point: Optional[int] = None
    user_point: Optional[int] = None
    last_received_circle_point: Optional[int] = None
    mission_refresh_count: Optional[int] = None
    progresses: Optional[List["CircleEventCircleMissionProgress"]] = None

    _FIELDS = (
        (0, "circle_point", "long", False, "prim"),
        (1, "user_point", "long", False, "prim"),
        (2, "last_received_circle_point", "long", False, "prim"),
        (3, "mission_refresh_count", "int", False, "prim"),
        (4, "progresses", "CircleEventCircleMissionProgress", True, "model"),
    )


@dataclass
class CircleEventRanking(MsgpackModel):
    circle_raw_rankings: Optional[List["CircleRawRanking"]] = None
    circle_profiles: Optional[List["CircleProfile"]] = None

    _FIELDS = (
        (0, "circle_raw_rankings", "CircleRawRanking", True, "model"),
        (1, "circle_profiles", "CircleProfile", True, "model"),
    )


@dataclass
class CircleInformationResult(MsgpackModel):
    u_circle_hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: Optional[int] = None
    play_time_end_type: Optional[int] = None
    entry_type: Optional[int] = None
    member_count: Optional[int] = None
    invite_id: Optional[int] = None
    result_status: Optional[int] = None
    circle_banner: Optional["CircleBanner"] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    icon_fame_master_id: Optional[int] = None

    _FIELDS = (
        (0, "u_circle_hashed_id", "string", False, "prim"),
        (1, "name", "string", False, "prim"),
        (2, "comment", "string", False, "prim"),
        (3, "play_time_start_type", "PlayTimeTypes", False, "enum"),
        (4, "play_time_end_type", "PlayTimeTypes", False, "enum"),
        (5, "entry_type", "EntryTypes", False, "enum"),
        (6, "member_count", "int", False, "prim"),
        (7, "invite_id", "long", False, "prim"),
        (9, "result_status", "CircleResultStatus", False, "enum"),
        (10, "circle_banner", "CircleBanner", False, "model"),
        (11, "main_character_master_id", "long", False, "prim"),
        (12, "display_awakening_status", "bool", False, "prim"),
        (13, "company_master_id", "long", False, "prim"),
        (14, "character_base_master_id", "long", False, "prim"),
        (15, "icon_fame_master_id", "long", False, "prim"),
    )


@dataclass
class CircleInviteResult(MsgpackModel):
    result_status: Optional[int] = None
    invite_id: Optional[int] = None

    _FIELDS = (
        (0, "result_status", "CircleResultStatus", False, "enum"),
        (1, "invite_id", "long", False, "prim"),
    )


@dataclass
class CircleMemberInfoParameters(MsgpackModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    player_rank: Optional[int] = None
    last_login_at: Optional[str] = None
    authority: Optional[int] = None
    main_u_character: Optional["MainCharacter"] = None
    invite_id: Optional[int] = None
    request_id: Optional[int] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    player_rate: Optional["Decimal"] = None
    is_public_player_rate: Optional[bool] = None
    league_class: Optional[int] = None
    icon_fame_master_id: Optional[int] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "user_name", "string", False, "prim"),
        (2, "player_rank", "int", False, "prim"),
        (3, "last_login_at", "DateTime", False, "prim"),
        (4, "authority", "CircleAuthorities", False, "enum"),
        (5, "main_u_character", "MainCharacter", False, "model"),
        (6, "invite_id", "long", False, "prim"),
        (7, "request_id", "long", False, "prim"),
        (8, "trophy_master_id1", "long", False, "prim"),
        (9, "trophy_master_id2", "long", False, "prim"),
        (10, "trophy_master_id3", "long", False, "prim"),
        (11, "main_character_master_id", "long", False, "prim"),
        (12, "display_awakening_status", "bool", False, "prim"),
        (13, "player_rate", "Decimal", False, "model"),
        (14, "is_public_player_rate", "bool", False, "prim"),
        (15, "league_class", "LeagueClassTypes", False, "enum"),
        (16, "icon_fame_master_id", "long", False, "prim"),
    )


@dataclass
class CircleMemberInfoResult(MsgpackModel):
    parameters: Optional[List["CircleMemberInfoParameters"]] = None
    result_status: Optional[int] = None
    circle_banner: Optional["CircleBanner"] = None

    _FIELDS = (
        (0, "parameters", "CircleMemberInfoParameters", True, "model"),
        (1, "result_status", "CircleResultStatus", False, "enum"),
        (2, "circle_banner", "CircleBanner", False, "model"),
    )


@dataclass
class CircleMemberParameters(MsgpackModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    player_rank: Optional[int] = None
    last_login_at: Optional[str] = None
    authority: Optional[int] = None
    main_u_character: Optional["MainCharacter"] = None
    invite_id: Optional[int] = None
    request_id: Optional[int] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    icon_fame_master_id: Optional[int] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "user_name", "string", False, "prim"),
        (2, "player_rank", "int", False, "prim"),
        (3, "last_login_at", "DateTime", False, "prim"),
        (4, "authority", "CircleAuthorities", False, "enum"),
        (5, "main_u_character", "MainCharacter", False, "model"),
        (6, "invite_id", "long", False, "prim"),
        (7, "request_id", "long", False, "prim"),
        (8, "trophy_master_id1", "long", False, "prim"),
        (9, "trophy_master_id2", "long", False, "prim"),
        (10, "trophy_master_id3", "long", False, "prim"),
        (11, "main_character_master_id", "long", False, "prim"),
        (12, "display_awakening_status", "bool", False, "prim"),
        (16, "icon_fame_master_id", "long", False, "prim"),
    )


@dataclass
class CirclePayload(MsgpackModel):
    hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: Optional[int] = None
    play_time_end_type: Optional[int] = None
    entry_type: Optional[int] = None
    member_type: Optional[int] = None
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None

    _FIELDS = (
        (0, "hashed_id", "string", False, "prim"),
        (1, "name", "string", False, "prim"),
        (2, "comment", "string", False, "prim"),
        (3, "play_time_start_type", "PlayTimeTypes", False, "enum"),
        (4, "play_time_end_type", "PlayTimeTypes", False, "enum"),
        (5, "entry_type", "EntryTypes", False, "enum"),
        (6, "member_type", "SearchCircleMemberConditionTypes", False, "enum"),
        (7, "company_master_id", "long", False, "prim"),
        (8, "character_base_master_id", "long", False, "prim"),
    )


@dataclass
class CircleProfile(MsgpackModel):
    circle_id: Optional[str] = None
    name: Optional[str] = None
    member_count: Optional[int] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    icon_frame_master_id: Optional[int] = None

    _FIELDS = (
        (0, "circle_id", "string", False, "prim"),
        (1, "name", "string", False, "prim"),
        (2, "member_count", "int", False, "prim"),
        (3, "main_character_master_id", "long", False, "prim"),
        (4, "display_awakening_status", "bool", False, "prim"),
        (5, "icon_frame_master_id", "long", False, "prim"),
    )


@dataclass
class CircleRawRanking(MsgpackModel):
    rank: Optional[int] = None
    point: Optional[int] = None
    circle_id: Optional[str] = None

    _FIELDS = (
        (0, "rank", "int", False, "prim"),
        (1, "point", "int", False, "prim"),
        (2, "circle_id", "string", False, "prim"),
    )


@dataclass
class CircleResult(MsgpackModel):
    result_status: Optional[int] = None

    _FIELDS = ((0, "result_status", "CircleResultStatus", False, "enum"),)


@dataclass
class CircleSearchIdResult(MsgpackModel):
    parameters: Optional["CircleMemberParameters"] = None
    result_status: Optional[int] = None

    _FIELDS = (
        (0, "parameters", "CircleMemberParameters", False, "model"),
        (1, "result_status", "CircleResultStatus", False, "enum"),
    )


@dataclass
class CircleSearchResult(MsgpackModel):
    parameters: Optional[List["CircleMemberParameters"]] = None
    result_status: Optional[int] = None
    circle_banner: Optional["CircleBanner"] = None

    _FIELDS = (
        (0, "parameters", "CircleMemberParameters", True, "model"),
        (1, "result_status", "CircleResultStatus", False, "enum"),
        (2, "circle_banner", "CircleBanner", False, "model"),
    )


@dataclass
class ConcertResult(MsgpackModel):
    rewards: Optional[List["ReceivedThing"]] = None

    _FIELDS = ((0, "rewards", "ReceivedThing", True, "model"),)


@dataclass
class ConcoursDetailInformationResult(MsgpackModel):
    concours_detail_master_id: Optional[int] = None
    rank: Optional[int] = None

    _FIELDS = (
        (0, "concours_detail_master_id", "long", False, "prim"),
        (1, "rank", "int", False, "prim"),
    )


@dataclass
class ConcoursInfomationResult(MsgpackModel):
    details: Optional[List["ConcoursDetailInformationResult"]] = None
    current_point: Optional[int] = None

    _FIELDS = (
        (0, "details", "ConcoursDetailInformationResult", True, "model"),
        (1, "current_point", "int", False, "prim"),
    )


@dataclass
class ConvertedThingResult(MsgpackModel):
    exchange_shop_master_id: Optional[int] = None
    original_quantity: Optional[int] = None
    received_thing: Optional["ReceivedThing"] = None

    _FIELDS = (
        (0, "exchange_shop_master_id", "long", False, "prim"),
        (1, "original_quantity", "int", False, "prim"),
        (2, "received_thing", "ReceivedThing", False, "model"),
    )


@dataclass
class CostumeFavoritePayload(MsgpackModel):
    costume_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    set_favorite: Optional[bool] = None

    _FIELDS = (
        (0, "costume_master_id", "long", False, "prim"),
        (1, "character_base_master_id", "long", False, "prim"),
        (2, "set_favorite", "bool", False, "prim"),
    )


@dataclass
class CourseRankingResult(MsgpackModel):
    rank: Optional[int] = None
    user_id: Optional[int] = None
    user_profile: Optional["UserProfile"] = None
    course_result: Optional["CourseResult"] = None
    note_result: Optional["NoteResult"] = None

    _FIELDS = (
        (0, "rank", "int", False, "prim"),
        (1, "user_id", "long", False, "prim"),
        (2, "user_profile", "UserProfile", False, "model"),
        (3, "course_result", "CourseResult", False, "model"),
        (4, "note_result", "NoteResult", False, "model"),
    )


@dataclass
class CourseResult(MsgpackModel):
    total_achievement_rate_percent_record: Optional["Decimal"] = None
    best_record_challenge_count: Optional[int] = None
    best_record_date: Optional[str] = None

    _FIELDS = (
        (0, "total_achievement_rate_percent_record", "Decimal", False, "model"),
        (1, "best_record_challenge_count", "int", False, "prim"),
        (2, "best_record_date", "DateTime", False, "prim"),
    )


@dataclass
class CreateCircleResult(MsgpackModel):
    result_status: Optional[int] = None
    circle_hashed_id: Optional[str] = None

    _FIELDS = (
        (0, "result_status", "CircleResultStatus", False, "enum"),
        (1, "circle_hashed_id", "string", False, "prim"),
    )


@dataclass
class CreateMultiRoomPayload(MsgpackModel):
    room_name: Optional[str] = None
    password: Optional[str] = None
    can_join_max_member: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    play_mode: Optional[int] = None
    live_master_id1: Optional[int] = None
    live_master_id2: Optional[int] = None
    live_master_id3: Optional[int] = None

    _FIELDS = (
        (0, "room_name", "string", False, "prim"),
        (1, "password", "string", False, "prim"),
        (2, "can_join_max_member", "int", False, "prim"),
        (3, "start_date", "DateTime", False, "prim"),
        (4, "end_date", "DateTime", False, "prim"),
        (5, "play_mode", "MultiRoomPlayModes", False, "enum"),
        (6, "live_master_id1", "long", False, "prim"),
        (7, "live_master_id2", "long", False, "prim"),
        (8, "live_master_id3", "long", False, "prim"),
    )


@dataclass
class DebugAlbumSimpleArrangingPayload(MsgpackModel):
    publishing: Optional[bool] = None
    page: Optional[int] = None
    photos: Optional[List["AlbumPhotoPayload"]] = None
    m_album_theme_id: Optional[int] = None

    _FIELDS = (
        (0, "publishing", "bool", False, "prim"),
        (1, "page", "int", False, "prim"),
        (2, "photos", "AlbumPhotoPayload", True, "model"),
        (3, "m_album_theme_id", "long", False, "prim"),
    )


@dataclass
class DebugEditLeagueBasicPayload(MsgpackModel):
    current_class_type: Optional[int] = None
    best_class_type: Optional[int] = None

    _FIELDS = (
        (0, "current_class_type", "LeagueClassTypes", False, "enum"),
        (1, "best_class_type", "LeagueClassTypes", False, "enum"),
    )


@dataclass
class DebugLinkageCodeResult(MsgpackModel):
    password: Optional[str] = None
    take_over_code_result: Optional["TakeOverCodeResult"] = None

    _FIELDS = (
        (0, "password", "string", False, "prim"),
        (1, "take_over_code_result", "TakeOverCodeResult", False, "model"),
    )


@dataclass
class DebugModifyCharacterEnhanceInformationPayload(MsgpackModel):
    m_character_id: Optional[int] = None
    actor_level: Optional[int] = None
    is_awaken: Optional[bool] = None
    sense_level: Optional[int] = None
    talent_bloom_stage: Optional[int] = None

    _FIELDS = (
        (0, "m_character_id", "long", False, "prim"),
        (1, "actor_level", "int", False, "prim"),
        (2, "is_awaken", "bool", False, "prim"),
        (3, "sense_level", "int", False, "prim"),
        (4, "talent_bloom_stage", "int", False, "prim"),
    )


@dataclass
class DebugModifyPosterEnhanceInformationPayload(MsgpackModel):
    m_poster_id: Optional[int] = None
    level: Optional[int] = None
    release_phase: Optional[int] = None

    _FIELDS = (
        (0, "m_poster_id", "long", False, "prim"),
        (1, "level", "int", False, "prim"),
        (2, "release_phase", "int", False, "prim"),
    )


@dataclass
class DebugPrepareLeagueGroupUserPayload(MsgpackModel):
    league_master_id: Optional[int] = None
    class_type: Optional[int] = None
    user_ids: Optional[List[int]] = None

    _FIELDS = (
        (0, "league_master_id", "long", False, "prim"),
        (1, "class_type", "LeagueClassTypes", False, "enum"),
        (2, "user_ids", "long", True, "prim"),
    )


@dataclass
class DebugUserIdResult(MsgpackModel):
    user_id: Optional[str] = None
    hashed_user_id: Optional[str] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "hashed_user_id", "string", False, "prim"),
    )


@dataclass
class Decimal(MsgpackModel):
    pass

    _FIELDS = ()


@dataclass
class Dictionary(MsgpackModel):
    pass

    _FIELDS = ()


@dataclass
class DonateSupportCompanyResult(MsgpackModel):
    my_circle_information: Optional["MyCircleInformationResult"] = None
    result_status: Optional[int] = None

    _FIELDS = (
        (0, "my_circle_information", "MyCircleInformationResult", False, "model"),
        (1, "result_status", "CircleDonateSupportCompanyResult", False, "enum"),
    )


@dataclass
class DonateSupportLevelLimitDetail(MsgpackModel):
    order: Optional[int] = None
    quantity: Optional[int] = None

    _FIELDS = (
        (0, "order", "int", False, "prim"),
        (1, "quantity", "int", False, "prim"),
    )


@dataclass
class DonateSupportLevelLimitPayload(MsgpackModel):
    company: Optional[int] = None
    next_level_limit: Optional[int] = None
    coin_quantity: Optional[int] = None
    details: Optional[List["DonateSupportLevelLimitDetail"]] = None

    _FIELDS = (
        (0, "company", "Companies", False, "enum"),
        (1, "next_level_limit", "int", False, "prim"),
        (2, "coin_quantity", "int", False, "prim"),
        (3, "details", "DonateSupportLevelLimitDetail", True, "model"),
    )


@dataclass
class EditBookmarkPayload(MsgpackModel):
    music_master_id: Optional[int] = None
    bookmark_flag: Optional[int] = None

    _FIELDS = (
        (0, "music_master_id", "long", False, "prim"),
        (1, "bookmark_flag", "MusicBookmarkFlags", False, "enum"),
    )


@dataclass
class EditPartyPayload(MsgpackModel):
    party_slots: Optional[List["EditPartySlotPayload"]] = None
    sense_notation_master_id: Optional[int] = None
    music_master_id: Optional[int] = None
    vocal_version: Optional[int] = None
    is_high_score_challenge: Optional[bool] = None
    leader_position: Optional[int] = None

    _FIELDS = (
        (0, "party_slots", "EditPartySlotPayload", True, "model"),
        (1, "sense_notation_master_id", "long", False, "prim"),
        (2, "music_master_id", "long", False, "prim"),
        (3, "vocal_version", "int", False, "prim"),
        (4, "is_high_score_challenge", "bool", False, "prim"),
        (5, "leader_position", "int", False, "prim"),
    )


@dataclass
class EditPartySlotPayload(MsgpackModel):
    u_party_slot_id: Optional[int] = None
    u_character_id: Optional[int] = None
    u_accessory_id: Optional[int] = None
    u_poster_id: Optional[int] = None
    bonus_ability_enable_flags: Optional[int] = None

    _FIELDS = (
        (0, "u_party_slot_id", "long", False, "prim"),
        (1, "u_character_id", "long", False, "prim"),
        (2, "u_accessory_id", "long", False, "prim"),
        (3, "u_poster_id", "long", False, "prim"),
        (4, "bonus_ability_enable_flags", "BonusAbilityEnableFlags", False, "enum"),
    )


@dataclass
class EditPositionPayload(MsgpackModel):
    slots: Optional[List["EditPositionSlotPayload"]] = None

    _FIELDS = ((0, "slots", "EditPositionSlotPayload", True, "model"),)


@dataclass
class EditPositionSlotPayload(MsgpackModel):
    u_party_slot_id: Optional[int] = None
    position: Optional[int] = None

    _FIELDS = (
        (0, "u_party_slot_id", "long", False, "prim"),
        (1, "position", "int", False, "prim"),
    )


@dataclass
class EditTrialPartyEventStagePartyPayload(MsgpackModel):
    trial_party_event_stage_master_id: Optional[int] = None
    slots: Optional[List["EditTrialPartyEventStagePartyPayloadSlot"]] = None
    leader_position: Optional[int] = None

    _FIELDS = (
        (0, "trial_party_event_stage_master_id", "long", False, "prim"),
        (1, "slots", "EditTrialPartyEventStagePartyPayloadSlot", True, "model"),
        (2, "leader_position", "int", False, "prim"),
    )


@dataclass
class EditTrialPartyEventStagePartyPayloadSlot(MsgpackModel):
    position: Optional[int] = None
    trial_party_character_master_id: Optional[int] = None
    trial_party_poster_master_id: Optional[int] = None
    trial_party_accessory_master_id: Optional[int] = None

    _FIELDS = (
        (0, "position", "int", False, "prim"),
        (1, "trial_party_character_master_id", "long", False, "prim"),
        (2, "trial_party_poster_master_id", "long", False, "prim"),
        (3, "trial_party_accessory_master_id", "long", False, "prim"),
    )


@dataclass
class EditUserProfilePayload(MsgpackModel):
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

    _FIELDS = (
        (0, "name", "string", False, "prim"),
        (1, "introduction", "string", False, "prim"),
        (2, "main_u_character_id", "long", False, "prim"),
        (3, "m_nameplate_id", "long", False, "prim"),
        (4, "m_name_color_id", "long", False, "prim"),
        (5, "m_trophy_id1", "long", False, "prim"),
        (6, "m_trophy_id2", "long", False, "prim"),
        (7, "m_trophy_id3", "long", False, "prim"),
        (8, "is_public_player_rate", "bool", False, "prim"),
        (9, "display_awakening_status", "bool", False, "prim"),
        (10, "main_character_master_id", "long", False, "prim"),
        (11, "name_base_color_masterid", "long", False, "prim"),
        (12, "icon_frame_master_id", "long", False, "prim"),
        (13, "home_skin_master_id", "long", False, "prim"),
    )


@dataclass
class EexternalPaymentResult(MsgpackModel):
    received_jewel_shop_item_master_ids: Optional[List[int]] = None

    _FIELDS = ((0, "received_jewel_shop_item_master_ids", "long", True, "prim"),)


@dataclass
class Effect(MsgpackModel):
    order: Optional[int] = None
    master_id: Optional[int] = None
    effect_types: Optional[int] = None
    triggers: Optional[List["EffectTrigger"]] = None
    targets: Optional[List["EffectTargetValue"]] = None
    duration: Optional[int] = None

    _FIELDS = (
        (0, "order", "int", False, "prim"),
        (1, "master_id", "long", False, "prim"),
        (2, "effect_types", "EffectTypes", False, "enum"),
        (3, "triggers", "EffectTrigger", True, "model"),
        (4, "targets", "EffectTargetValue", True, "model"),
        (5, "duration", "int", False, "prim"),
    )


@dataclass
class EffectBranch(MsgpackModel):
    condition_value: Optional[int] = None
    judge_types: Optional[int] = None
    sense_effects: Optional[List["Effect"]] = None

    _FIELDS = (
        (0, "condition_value", "long", False, "prim"),
        (1, "judge_types", "BranchJudgeTypes", False, "enum"),
        (2, "sense_effects", "Effect", True, "model"),
    )


@dataclass
class EffectTargetValue(MsgpackModel):
    target_actor_id: Optional[int] = None
    value: Optional[float] = None

    _FIELDS = (
        (0, "target_actor_id", "long", False, "prim"),
        (1, "value", "double", False, "prim"),
    )


@dataclass
class EffectTrigger(MsgpackModel):
    type: Optional[int] = None
    value: Optional[int] = None

    _FIELDS = (
        (0, "type", "TriggerTypes", False, "enum"),
        (1, "value", "long", False, "prim"),
    )


@dataclass
class EnvironmentResult(MsgpackModel):
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

    _FIELDS = (
        (0, "application_version", "string", False, "prim"),
        (1, "asset_version", "string", False, "prim"),
        (2, "api_endpoint", "string", False, "prim"),
        (3, "maintenance_api_endpoint", "string", False, "prim"),
        (4, "news_api_endpoint", "string", False, "prim"),
        (5, "is_maintenance", "bool", False, "prim"),
        (6, "master_data_url", "string", False, "prim"),
        (7, "static_content_url", "string", False, "prim"),
        (8, "asset_url", "string", False, "prim"),
        (9, "is_app_review", "bool", False, "prim"),
        (10, "photo_content_url", "string", False, "prim"),
        (11, "multi_real_time_server_url", "string", False, "prim"),
        (12, "external_payment_url", "string", False, "prim"),
    )


@dataclass
class EpisodeResult(MsgpackModel):
    episode_title: Optional[str] = None
    story_type: Optional[int] = None
    episode_order: Optional[int] = None
    episode_detail_asset_source: Optional[str] = None

    _FIELDS = (
        (0, "episode_title", "string", False, "prim"),
        (1, "story_type", "StoryTypes", False, "enum"),
        (2, "episode_order", "int", False, "prim"),
        (3, "episode_detail_asset_source", "string", False, "prim"),
    )


@dataclass
class EventBoxGachaRollResult(MsgpackModel):
    received_things: Optional[List["ReceivedThing"]] = None
    has_reset: Optional[bool] = None
    drawn_event_box_gacha_box_thing_master_ids: Optional[List[int]] = None

    _FIELDS = (
        (0, "received_things", "ReceivedThing", True, "model"),
        (1, "has_reset", "bool", False, "prim"),
        (2, "drawn_event_box_gacha_box_thing_master_ids", "long", True, "prim"),
    )


@dataclass
class EventResult(MsgpackModel):
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

    _FIELDS = (
        (0, "acquired_event_point", "int", False, "prim"),
        (1, "attached_story_event_master_id", "long", False, "prim"),
        (2, "circle_event_high_score", "long", False, "prim"),
        (3, "circle_event_high_score_multiplier_percent", "int", False, "prim"),
        (4, "circle_event_before_high_score", "long", False, "prim"),
        (5, "high_score_before", "long", False, "prim"),
        (6, "high_score_after", "long", False, "prim"),
        (7, "before_rank", "long", False, "prim"),
        (8, "after_rank", "long", False, "prim"),
        (9, "story_event_master_id", "long", False, "prim"),
        (10, "event_master_id", "long", False, "prim"),
        (11, "this_time_support_point", "int", False, "prim"),
        (12, "camp_before_rank", "long", False, "prim"),
        (13, "camp_after_rank", "long", False, "prim"),
    )


@dataclass
class ExchangeShopThingPayload(MsgpackModel):
    m_exchange_shop_thing_id: Optional[int] = None
    quantity: Optional[int] = None

    _FIELDS = (
        (0, "m_exchange_shop_thing_id", "long", False, "prim"),
        (1, "quantity", "int", False, "prim"),
    )


@dataclass
class FavoriteStampOrderPayload(MsgpackModel):
    stamp_master_ids: Optional[List[int]] = None

    _FIELDS = ((0, "stamp_master_ids", "long", True, "prim"),)


@dataclass
class FinishAnotherNotationLivePayload(MsgpackModel):
    base_score_blocks: Optional[List["BaseScoreBlock"]] = None
    sense_score_blocks: Optional[List["SenseScoreBlock"]] = None
    star_act_score_blocks: Optional[List["StarActScoreBlock"]] = None
    multi_live_additional_score_blocks: Optional[
        List["MultiLiveAdditionalScoreBlock"]
    ] = None
    another_notation_master_id: Optional[int] = None
    is_auto_play: Optional[bool] = None

    _FIELDS = (
        (0, "base_score_blocks", "BaseScoreBlock", True, "model"),
        (1, "sense_score_blocks", "SenseScoreBlock", True, "model"),
        (2, "star_act_score_blocks", "StarActScoreBlock", True, "model"),
        (
            3,
            "multi_live_additional_score_blocks",
            "MultiLiveAdditionalScoreBlock",
            True,
            "model",
        ),
        (4, "another_notation_master_id", "long", False, "prim"),
        (5, "is_auto_play", "bool", False, "prim"),
    )


@dataclass
class FinishLessonPayload(MsgpackModel):
    score: Optional[int] = None
    max_combo: Optional[int] = None
    judges: Optional[List["NoteJudgePayload"]] = None

    _FIELDS = (
        (0, "score", "long", False, "prim"),
        (1, "max_combo", "int", False, "prim"),
        (2, "judges", "NoteJudgePayload", True, "model"),
    )


@dataclass
class FinishLivePayload(MsgpackModel):
    score: Optional[int] = None
    max_combo: Optional[int] = None
    judges: Optional[List["NoteJudgePayload"]] = None
    is_cleared: Optional[bool] = None
    base_score_blocks: Optional[List["BaseScoreBlock"]] = None
    sense_score_blocks: Optional[List["SenseScoreBlock"]] = None
    star_act_score_blocks: Optional[List["StarActScoreBlock"]] = None
    multi_live_additional_score_blocks: Optional[
        List["MultiLiveAdditionalScoreBlock"]
    ] = None
    triple_cast_party_scores: Optional[List["TripleCastPartyScore"]] = None
    trial_party_event_stage_result: Optional["TrialPartyEventStageResult"] = None

    _FIELDS = (
        (0, "score", "long", False, "prim"),
        (1, "max_combo", "int", False, "prim"),
        (2, "judges", "NoteJudgePayload", True, "model"),
        (3, "is_cleared", "bool", False, "prim"),
        (4, "base_score_blocks", "BaseScoreBlock", True, "model"),
        (5, "sense_score_blocks", "SenseScoreBlock", True, "model"),
        (6, "star_act_score_blocks", "StarActScoreBlock", True, "model"),
        (
            7,
            "multi_live_additional_score_blocks",
            "MultiLiveAdditionalScoreBlock",
            True,
            "model",
        ),
        (8, "triple_cast_party_scores", "TripleCastPartyScore", True, "model"),
        (
            9,
            "trial_party_event_stage_result",
            "TrialPartyEventStageResult",
            False,
            "model",
        ),
    )


@dataclass
class FinishLiveResult(MsgpackModel):
    league_rewards: Optional[List["ReceivedThing"]] = None
    rate_result: Optional["RateResult"] = None
    player_rank_point_result: Optional["PlayerRankPointResult"] = None
    clear_lamp: Optional[int] = None
    rate_grade: Optional[int] = None
    is_high_score: Optional[bool] = None
    audition_before_phase: Optional[int] = None
    audition_after_phase: Optional[int] = None
    audition_rewards: Optional[List["ReceivedThing"]] = None
    story_event_rewards: Optional[List["ReceivedThing"]] = None
    achievement_rate_average: Optional[float] = None
    audition_master_id: Optional[int] = None
    sp_rate_update_result: Optional["SpRateUpdateResult"] = None
    tournament_result: Optional["TournamentResult"] = None
    celling_max_count: Optional[int] = None
    celling_user_count: Optional[int] = None
    before_clear_lamp: Optional[int] = None
    poster_drop_up_percent: Optional[int] = None
    event_result: Optional["EventResult"] = None
    live_drop_things: Optional[List["LiveDropThing"]] = None
    lesson_result: Optional["LessonResult"] = None
    league_result: Optional["LeagueResult"] = None
    concert_result: Optional["ConcertResult"] = None
    bonus_live_result: Optional["BonusLiveResult"] = None
    ghost_live_result: Optional["GhostLiveResult"] = None
    trial_party_event_result: Optional["TrialPartyEventResult"] = None
    accessory_auto_sell_convert_things: Optional[
        List["AccessoryAutoSellConvertThing"]
    ] = None

    _FIELDS = (
        (1, "league_rewards", "ReceivedThing", True, "model"),
        (2, "rate_result", "RateResult", False, "model"),
        (3, "player_rank_point_result", "PlayerRankPointResult", False, "model"),
        (5, "clear_lamp", "ClearLamps", False, "enum"),
        (6, "rate_grade", "AchievementRateGrades", False, "enum"),
        (8, "is_high_score", "bool", False, "prim"),
        (9, "audition_before_phase", "byte", False, "prim"),
        (10, "audition_after_phase", "byte", False, "prim"),
        (11, "audition_rewards", "ReceivedThing", True, "model"),
        (12, "story_event_rewards", "ReceivedThing", True, "model"),
        (13, "achievement_rate_average", "double", False, "prim"),
        (14, "audition_master_id", "long", False, "prim"),
        (16, "sp_rate_update_result", "SpRateUpdateResult", False, "model"),
        (17, "tournament_result", "TournamentResult", False, "model"),
        (18, "celling_max_count", "int", False, "prim"),
        (19, "celling_user_count", "int", False, "prim"),
        (20, "before_clear_lamp", "ClearLamps", False, "enum"),
        (21, "poster_drop_up_percent", "int", False, "prim"),
        (22, "event_result", "EventResult", False, "model"),
        (23, "live_drop_things", "LiveDropThing", True, "model"),
        (24, "lesson_result", "LessonResult", False, "model"),
        (25, "league_result", "LeagueResult", False, "model"),
        (26, "concert_result", "ConcertResult", False, "model"),
        (27, "bonus_live_result", "BonusLiveResult", False, "model"),
        (28, "ghost_live_result", "GhostLiveResult", False, "model"),
        (29, "trial_party_event_result", "TrialPartyEventResult", False, "model"),
        (
            30,
            "accessory_auto_sell_convert_things",
            "AccessoryAutoSellConvertThing",
            True,
            "model",
        ),
    )


@dataclass
class FlashSaleReadStagePayload(MsgpackModel):
    read_flash_sale_stage_ids: Optional[List[int]] = None

    _FIELDS = ((0, "read_flash_sale_stage_ids", "long", True, "prim"),)


@dataclass
class FriendAcceptResult(MsgpackModel):
    result_status: Optional[int] = None

    _FIELDS = ((0, "result_status", "FriendAcceptResultStatus", False, "enum"),)


@dataclass
class FriendFavoritePayload(MsgpackModel):
    target_user_id: Optional[str] = None
    set_favorite: Optional[bool] = None

    _FIELDS = (
        (0, "target_user_id", "string", False, "prim"),
        (1, "set_favorite", "bool", False, "prim"),
    )


@dataclass
class FriendInvitationMissionPayload(MsgpackModel):
    friend_invitation_mission_master_ids: Optional[List[int]] = None

    _FIELDS = ((0, "friend_invitation_mission_master_ids", "long", True, "prim"),)


@dataclass
class FriendInvitationUserInfoResult(MsgpackModel):
    hashed_user_id: Optional[str] = None
    name: Optional[str] = None
    player_rank: Optional[int] = None
    result_status: Optional[int] = None

    _FIELDS = (
        (0, "hashed_user_id", "string", False, "prim"),
        (1, "name", "string", False, "prim"),
        (2, "player_rank", "long", False, "prim"),
        (3, "result_status", "InvitationCodeResultStatuses", False, "enum"),
    )


@dataclass
class FriendListResult(MsgpackModel):
    results: Optional[List["FriendResult"]] = None
    current_friend_count: Optional[int] = None

    _FIELDS = (
        (0, "results", "FriendResult", True, "model"),
        (1, "current_friend_count", "int", False, "prim"),
    )


@dataclass
class FriendRequestResult(MsgpackModel):
    result_status: Optional[int] = None

    _FIELDS = ((0, "result_status", "FriendRequestResultStatus", False, "enum"),)


@dataclass
class FriendResult(MsgpackModel):
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
    league_class: Optional[int] = None
    character_ranks: Optional[List["CharacterRank"]] = None
    is_public_album_main_page: Optional[bool] = None
    main_character_master_id: Optional[int] = None
    display_awakening_status: Optional[bool] = None
    icon_frame_master_id: Optional[int] = None
    is_favorite: Optional[bool] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (2, "player_rank", "int", False, "prim"),
        (3, "trophy_master_id1", "long", False, "prim"),
        (4, "trophy_master_id2", "long", False, "prim"),
        (5, "trophy_master_id3", "long", False, "prim"),
        (6, "introduction", "string", False, "prim"),
        (7, "last_logged_in_at", "DateTime", False, "prim"),
        (8, "name", "string", False, "prim"),
        (9, "player_rate", "double", False, "prim"),
        (10, "is_public_player_rate", "bool", False, "prim"),
        (11, "league_class", "LeagueClassTypes", False, "enum"),
        (12, "character_ranks", "CharacterRank", True, "model"),
        (13, "is_public_album_main_page", "bool", False, "prim"),
        (15, "main_character_master_id", "long", False, "prim"),
        (16, "display_awakening_status", "bool", False, "prim"),
        (17, "icon_frame_master_id", "long", False, "prim"),
        (18, "is_favorite", "bool", False, "prim"),
    )


@dataclass
class FriendSearchResult(MsgpackModel):
    friend_result: Optional["FriendResult"] = None
    result_status: Optional[int] = None

    _FIELDS = (
        (0, "friend_result", "FriendResult", False, "model"),
        (1, "result_status", "FriendSearchResultStatus", False, "enum"),
    )


@dataclass
class GachaHistoryResult(MsgpackModel):
    master_id: Optional[int] = None
    created_at: Optional[str] = None

    _FIELDS = (
        (0, "master_id", "long", False, "prim"),
        (1, "created_at", "DateTime", False, "prim"),
    )


@dataclass
class GachaInfoResult(MsgpackModel):
    id_: Optional[int] = None
    roll_limits: Optional[List["GachaRollLimit"]] = None
    normal_emission_flags: Optional[int] = None
    fixed_emission_flags: Optional[int] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (1, "roll_limits", "GachaRollLimit", True, "model"),
        (2, "normal_emission_flags", "GachaEmissionFlags", False, "enum"),
        (3, "fixed_emission_flags", "GachaEmissionFlags", False, "enum"),
    )


@dataclass
class GachaLineupItemProbability(MsgpackModel):
    id_: Optional[int] = None
    probability: Optional[float] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (2, "probability", "double", False, "prim"),
    )


@dataclass
class GachaRollLimit(MsgpackModel):
    gacha_detail_master_id: Optional[int] = None
    roll_left: Optional[int] = None

    _FIELDS = (
        (0, "gacha_detail_master_id", "long", False, "prim"),
        (1, "roll_left", "int", False, "prim"),
    )


@dataclass
class GachaRollResult(MsgpackModel):
    m_gacha_master_id: Optional[int] = None
    received_things: Optional[List["GachaThingResult"]] = None
    received_bonus_things: Optional[List["ReceivedThing"]] = None
    received_detail_bonus_things: Optional[List["ReceivedThing"]] = None
    received_roll_bonus_things: Optional[List["ReceivedThing"]] = None

    _FIELDS = (
        (0, "m_gacha_master_id", "long", False, "prim"),
        (1, "received_things", "GachaThingResult", True, "model"),
        (2, "received_bonus_things", "ReceivedThing", True, "model"),
        (3, "received_detail_bonus_things", "ReceivedThing", True, "model"),
        (4, "received_roll_bonus_things", "ReceivedThing", True, "model"),
    )


@dataclass
class GachaSelectedThingsResult(MsgpackModel):
    selected_gacha_thing_ids: Optional[List[int]] = None

    _FIELDS = ((0, "selected_gacha_thing_ids", "long", True, "prim"),)


@dataclass
class GachaThingResult(MsgpackModel):
    received_things: Optional[List["ReceivedThing"]] = None
    additional_received_things: Optional[List["ReceivedThing"]] = None
    movie_costume_master_id: Optional[int] = None

    _FIELDS = (
        (0, "received_things", "ReceivedThing", True, "model"),
        (1, "additional_received_things", "ReceivedThing", True, "model"),
        (2, "movie_costume_master_id", "long", False, "prim"),
    )


@dataclass
class GenerateLotteryResultPayload(MsgpackModel):
    prize: Optional[int] = None
    amount: Optional[int] = None

    _FIELDS = (
        (0, "prize", "int", False, "prim"),
        (1, "amount", "int", False, "prim"),
    )


@dataclass
class GeneratePhotoPayload(MsgpackModel):
    character_base_master_id: Optional[int] = None
    item_master_id: Optional[int] = None
    image_data: Optional[List[int]] = None
    thumbnail_image_data: Optional[List[int]] = None
    appeared_characters: Optional[List["PhotoAppearedCharacter"]] = None

    _FIELDS = (
        (0, "character_base_master_id", "long", False, "prim"),
        (1, "item_master_id", "long", False, "prim"),
        (2, "image_data", "byte", True, "prim"),
        (3, "thumbnail_image_data", "byte", True, "prim"),
        (4, "appeared_characters", "PhotoAppearedCharacter", True, "model"),
    )


@dataclass
class GeneratePhotoResult(MsgpackModel):
    photo_id: Optional[int] = None
    file_name: Optional[str] = None
    sas_token: Optional[str] = None
    rarity: Optional[int] = None
    sign_master_id: Optional[int] = None
    photo_effect_master_id: Optional[int] = None

    _FIELDS = (
        (0, "photo_id", "long", False, "prim"),
        (1, "file_name", "string", False, "prim"),
        (2, "sas_token", "string", False, "prim"),
        (3, "rarity", "PhotoRarities", False, "enum"),
        (4, "sign_master_id", "long", False, "prim"),
        (5, "photo_effect_master_id", "long", False, "prim"),
    )


@dataclass
class GeneratePhotosPayload(MsgpackModel):
    payloads: Optional[List["GeneratePhotoPayload"]] = None

    _FIELDS = ((0, "payloads", "GeneratePhotoPayload", True, "model"),)


@dataclass
class GhostLiveInfo(MsgpackModel):
    leader_position: Optional[int] = None
    party_slot: Optional[List["PartySlotDetail"]] = None

    _FIELDS = (
        (0, "leader_position", "int", False, "prim"),
        (1, "party_slot", "PartySlotDetail", True, "model"),
    )


@dataclass
class GhostLiveResult(MsgpackModel):
    ghost_user_profile: Optional["UserProfileDetail"] = None
    ghost_user_score: Optional[int] = None
    total_battle_win_count: Optional[int] = None
    matching_result: Optional[int] = None
    display_character_master_id: Optional[int] = None
    display_character_awakening_status: Optional[bool] = None

    _FIELDS = (
        (0, "ghost_user_profile", "UserProfileDetail", False, "model"),
        (1, "ghost_user_score", "long", False, "prim"),
        (2, "total_battle_win_count", "long", False, "prim"),
        (3, "matching_result", "MatchingResult", False, "enum"),
        (4, "display_character_master_id", "long", False, "prim"),
        (5, "display_character_awakening_status", "bool", False, "prim"),
    )


@dataclass
class HighScoreBuff(MsgpackModel):
    user_id: Optional[str] = None
    buffs: Optional[List["HighScoreBuffSetting"]] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "buffs", "HighScoreBuffSetting", True, "model"),
    )


@dataclass
class HighScoreBuffSetting(MsgpackModel):
    story_event_high_score_buff_setting_id: Optional[int] = None
    current_level: Optional[int] = None

    _FIELDS = (
        (0, "story_event_high_score_buff_setting_id", "long", False, "prim"),
        (1, "current_level", "int", False, "prim"),
    )


@dataclass
class HighScoreParty(MsgpackModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    party_name: Optional[str] = None
    slots: Optional[List["HighScorePartySlot"]] = None
    difficulty: Optional[int] = None
    leader_position: Optional[int] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "user_name", "string", False, "prim"),
        (2, "party_name", "string", False, "prim"),
        (3, "slots", "HighScorePartySlot", True, "model"),
        (4, "difficulty", "MusicDifficulties", False, "enum"),
        (5, "leader_position", "int", False, "prim"),
    )


@dataclass
class HighScorePartySlot(MsgpackModel):
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
    current_status: Optional["Status"] = None
    character_display_awakening_status: Optional[bool] = None

    _FIELDS = (
        (0, "position", "int", False, "prim"),
        (1, "character_master_id", "long", False, "prim"),
        (2, "character_level", "int", False, "prim"),
        (3, "character_talent_stage", "int", False, "prim"),
        (4, "character_awakening_phase", "int", False, "prim"),
        (5, "poster_master_id", "long", False, "prim"),
        (6, "poster_level", "int", False, "prim"),
        (7, "poster_breakthrough_phase", "int", False, "prim"),
        (8, "accessory_master_id", "long", False, "prim"),
        (9, "accessory_level", "int", False, "prim"),
        (10, "current_status", "Status", False, "model"),
        (11, "character_display_awakening_status", "bool", False, "prim"),
    )


@dataclass
class InboxReceiveResult(MsgpackModel):
    received_things: Optional[List["ReceivedThing"]] = None
    has_not_receive_things: Optional[bool] = None

    _FIELDS = (
        (0, "received_things", "ReceivedThing", True, "model"),
        (1, "has_not_receive_things", "bool", False, "prim"),
    )


@dataclass
class InviteMultiRoomPayload(MsgpackModel):
    hashed_user_ids: Optional[List[str]] = None

    _FIELDS = ((0, "hashed_user_ids", "string", True, "prim"),)


@dataclass
class JoinMultiRoomPayload(MsgpackModel):
    hashed_room_id: Optional[str] = None
    password: Optional[str] = None

    _FIELDS = (
        (0, "hashed_room_id", "string", False, "prim"),
        (1, "password", "string", False, "prim"),
    )


@dataclass
class LeaguePartyAndRankingResult(MsgpackModel):
    rank: Optional[int] = None
    user_id: Optional[str] = None
    best_score: Optional[int] = None
    league_master_id: Optional[int] = None
    class_type: Optional[int] = None
    user_name: Optional[str] = None
    acting_ability: Optional[int] = None
    slots: Optional[List["LeaguePartySlotResult"]] = None
    difficulty: Optional[int] = None

    _FIELDS = (
        (0, "rank", "int", False, "prim"),
        (1, "user_id", "string", False, "prim"),
        (2, "best_score", "long", False, "prim"),
        (3, "league_master_id", "long", False, "prim"),
        (4, "class_type", "LeagueClassTypes", False, "enum"),
        (5, "user_name", "string", False, "prim"),
        (6, "acting_ability", "int", False, "prim"),
        (7, "slots", "LeaguePartySlotResult", True, "model"),
        (8, "difficulty", "MusicDifficulties", False, "enum"),
    )


@dataclass
class LeaguePartySlotResult(MsgpackModel):
    slot_position: Optional[int] = None
    character_master_id: Optional[int] = None
    attribute: Optional[int] = None
    character_rarity: Optional[int] = None
    character_level: Optional[int] = None
    poster_master_id: Optional[int] = None
    poster_rarity: Optional[int] = None
    poster_level: Optional[int] = None
    poster_breakthrough_phase: Optional[int] = None
    accessory_master_id: Optional[int] = None
    accessory_rarity: Optional[int] = None
    accessory_level: Optional[int] = None
    current_status: Optional["Status"] = None
    position: Optional[int] = None
    character_talent_stage: Optional[int] = None
    character_awakening_phase: Optional[int] = None
    character_display_awakening_status: Optional[bool] = None

    _FIELDS = (
        (0, "slot_position", "int", False, "prim"),
        (1, "character_master_id", "long", False, "prim"),
        (2, "attribute", "Attributes", False, "enum"),
        (4, "character_rarity", "CharacterRarities", False, "enum"),
        (6, "character_level", "int", False, "prim"),
        (7, "poster_master_id", "long", False, "prim"),
        (8, "poster_rarity", "PossessionRarities", False, "enum"),
        (9, "poster_level", "int", False, "prim"),
        (10, "poster_breakthrough_phase", "int", False, "prim"),
        (11, "accessory_master_id", "long", False, "prim"),
        (12, "accessory_rarity", "PossessionRarities", False, "enum"),
        (13, "accessory_level", "int", False, "prim"),
        (14, "current_status", "Status", False, "model"),
        (15, "position", "int", False, "prim"),
        (16, "character_talent_stage", "int", False, "prim"),
        (17, "character_awakening_phase", "int", False, "prim"),
        (18, "character_display_awakening_status", "bool", False, "prim"),
    )


@dataclass
class LeagueReceiveResults(MsgpackModel):
    class_reward_received_things: Optional[List["ReceivedThing"]] = None
    class_reward_type: Optional[int] = None
    first_achieve_received_things: Optional[List["ReceivedThing"]] = None
    group_rank_received_things: Optional[List["ReceivedThing"]] = None
    is_first_time_enrolled_class: Optional[bool] = None
    all_class_global_rank_received_things: Optional[List["ReceivedThing"]] = None

    _FIELDS = (
        (0, "class_reward_received_things", "ReceivedThing", True, "model"),
        (1, "class_reward_type", "LeagueClassChangeTypes", False, "enum"),
        (2, "first_achieve_received_things", "ReceivedThing", True, "model"),
        (3, "group_rank_received_things", "ReceivedThing", True, "model"),
        (4, "is_first_time_enrolled_class", "bool", False, "prim"),
        (5, "all_class_global_rank_received_things", "ReceivedThing", True, "model"),
    )


@dataclass
class LeagueResult(MsgpackModel):
    before_group_ranking: Optional[int] = None
    after_group_ranking: Optional[int] = None
    lowest_up_border_score: Optional[int] = None
    lowest_keep_border_score: Optional[int] = None
    enrolled_group_number: Optional[int] = None
    is_in_counting: Optional[bool] = None

    _FIELDS = (
        (0, "before_group_ranking", "int", False, "prim"),
        (1, "after_group_ranking", "int", False, "prim"),
        (2, "lowest_up_border_score", "long", False, "prim"),
        (3, "lowest_keep_border_score", "long", False, "prim"),
        (4, "enrolled_group_number", "int", False, "prim"),
        (5, "is_in_counting", "bool", False, "prim"),
    )


@dataclass
class LeagueTopMenuInformationResult(MsgpackModel):
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

    _FIELDS = (
        (0, "display_start_at", "DateTime", False, "prim"),
        (1, "counting_start_at", "DateTime", False, "prim"),
        (2, "display_end_at", "DateTime", False, "prim"),
        (3, "music_master_id", "long", False, "prim"),
        (6, "league_group_ranking", "int", False, "prim"),
        (8, "up_class_border_score", "long", False, "prim"),
        (9, "up_class_border_ranking", "int", False, "prim"),
        (10, "keep_class_border_score", "long", False, "prim"),
        (11, "keep_class_border_ranking", "int", False, "prim"),
        (12, "group_lowest_rank", "int", False, "prim"),
        (13, "is_participated", "bool", False, "prim"),
        (14, "enrolled_group_number", "int", False, "prim"),
    )


@dataclass
class LessonResult(MsgpackModel):
    character_base_master_id: Optional[int] = None
    star_point_result: Optional["StarPointResult"] = None
    high_score_rewards: Optional[List["ReceivedThing"]] = None
    high_score_before: Optional[int] = None
    high_score_after: Optional[int] = None

    _FIELDS = (
        (0, "character_base_master_id", "long", False, "prim"),
        (1, "star_point_result", "StarPointResult", False, "model"),
        (2, "high_score_rewards", "ReceivedThing", True, "model"),
        (3, "high_score_before", "long", False, "prim"),
        (4, "high_score_after", "long", False, "prim"),
    )


@dataclass
class LevelUpPhotoPayload(MsgpackModel):
    photo_id: Optional[int] = None
    after_level: Optional[int] = None

    _FIELDS = (
        (0, "photo_id", "long", False, "prim"),
        (1, "after_level", "int", False, "prim"),
    )


@dataclass
class LevelUpPhotoResult(MsgpackModel):
    photo_id: Optional[int] = None
    before_level: Optional[int] = None
    after_level: Optional[int] = None

    _FIELDS = (
        (0, "photo_id", "long", False, "prim"),
        (1, "before_level", "int", False, "prim"),
        (2, "after_level", "int", False, "prim"),
    )


@dataclass
class LiveDropThing(MsgpackModel):
    received_thing: Optional["ReceivedThing"] = None
    order: Optional[int] = None
    live_drop_type: Optional[int] = None
    is_fixed_drop: Optional[bool] = None

    _FIELDS = (
        (0, "received_thing", "ReceivedThing", False, "model"),
        (1, "order", "long", False, "prim"),
        (2, "live_drop_type", "LiveDropTypes", False, "enum"),
        (3, "is_fixed_drop", "bool", False, "prim"),
    )


@dataclass
class LiveTimeEvent(MsgpackModel):
    timings: Optional[List["SenseTimingEvent"]] = None
    cool_times: Optional[List["SenseCoolTime"]] = None

    _FIELDS = (
        (0, "timings", "SenseTimingEvent", True, "model"),
        (1, "cool_times", "SenseCoolTime", True, "model"),
    )


@dataclass
class LiveUnit(MsgpackModel):
    actors: Optional["Dictionary"] = None
    time_events: Optional["Dictionary"] = None
    possible_senses: Optional[List["Sense"]] = None
    start_effects: Optional[List["Effect"]] = None
    star_act: Optional["StarAct"] = None
    total_status: Optional[int] = None
    star_act_sense_light_count: Optional[int] = None
    max_principal: Optional[int] = None
    is_first_play_olivier: Optional[bool] = None
    base_score_percentage: Optional[int] = None
    base_score_difficulty_auto_coefficient: Optional[float] = None
    u_active_live_id: Optional[int] = None

    _FIELDS = (
        (0, "actors", "Dictionary", False, "model"),
        (1, "time_events", "Dictionary", False, "model"),
        (2, "possible_senses", "Sense", True, "model"),
        (3, "start_effects", "Effect", True, "model"),
        (4, "star_act", "StarAct", False, "model"),
        (5, "total_status", "int", False, "prim"),
        (6, "star_act_sense_light_count", "int", False, "prim"),
        (7, "max_principal", "int", False, "prim"),
        (8, "is_first_play_olivier", "bool", False, "prim"),
        (9, "base_score_percentage", "int", False, "prim"),
        (10, "base_score_difficulty_auto_coefficient", "double", False, "prim"),
        (11, "u_active_live_id", "long", False, "prim"),
    )


@dataclass
class LiveUnitWithOrder(MsgpackModel):
    actors: Optional["Dictionary"] = None
    time_events: Optional["Dictionary"] = None
    possible_senses: Optional[List["Sense"]] = None
    start_effects: Optional[List["Effect"]] = None
    star_act: Optional["StarAct"] = None
    total_status: Optional[int] = None
    star_act_sense_light_count: Optional[int] = None
    max_principal: Optional[int] = None
    is_first_play_olivier: Optional[bool] = None
    base_score_percentage: Optional[int] = None
    base_score_difficulty_auto_coefficient: Optional[float] = None
    u_active_live_id: Optional[int] = None
    order: Optional[int] = None

    _FIELDS = (
        (0, "actors", "Dictionary", False, "model"),
        (1, "time_events", "Dictionary", False, "model"),
        (2, "possible_senses", "Sense", True, "model"),
        (3, "start_effects", "Effect", True, "model"),
        (4, "star_act", "StarAct", False, "model"),
        (5, "total_status", "int", False, "prim"),
        (6, "star_act_sense_light_count", "int", False, "prim"),
        (7, "max_principal", "int", False, "prim"),
        (8, "is_first_play_olivier", "bool", False, "prim"),
        (9, "base_score_percentage", "int", False, "prim"),
        (10, "base_score_difficulty_auto_coefficient", "double", False, "prim"),
        (11, "u_active_live_id", "long", False, "prim"),
        (12, "order", "int", False, "prim"),
    )


@dataclass
class LoginBonusDetail(MsgpackModel):
    thing_type: Optional[int] = None
    thing_id: Optional[int] = None
    thing_quantity: Optional[int] = None
    login_count: Optional[int] = None

    _FIELDS = (
        (0, "thing_type", "ThingTypes", False, "enum"),
        (1, "thing_id", "long", False, "prim"),
        (2, "thing_quantity", "int", False, "prim"),
        (3, "login_count", "int", False, "prim"),
    )


@dataclass
class LoginBonusResult(MsgpackModel):
    login_bonus_id: Optional[int] = None
    current_login_count: Optional[int] = None
    received_things: Optional[List["ReceivedThing"]] = None
    title: Optional[str] = None
    type: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    message_template: Optional[str] = None
    background_image_path: Optional[str] = None
    cardboard_image_path: Optional[str] = None
    logo_image_path: Optional[str] = None
    total_days: Optional[int] = None
    is_loop: Optional[bool] = None
    order: Optional[int] = None
    details: Optional[List["LoginBonusDetail"]] = None
    navigation_spine_id: Optional[str] = None
    voice_asset_id: Optional[str] = None
    head_motion_master_id: Optional[int] = None
    facial_expression_master_id: Optional[int] = None
    head_direction_master_id: Optional[int] = None
    body_motion_master_id: Optional[int] = None
    lip_sync_master_id: Optional[int] = None
    layout_type: Optional[int] = None
    comeback_campaign_master_id: Optional[int] = None
    login_bonus_spine_group: Optional["LoginBonusSpineGroup"] = None

    _FIELDS = (
        (0, "login_bonus_id", "long", False, "prim"),
        (1, "current_login_count", "int", False, "prim"),
        (2, "received_things", "ReceivedThing", True, "model"),
        (3, "title", "string", False, "prim"),
        (4, "type", "LoginBonusTypes", False, "enum"),
        (5, "start_date", "DateTime", False, "prim"),
        (6, "end_date", "DateTime", False, "prim"),
        (10, "message_template", "string", False, "prim"),
        (11, "background_image_path", "string", False, "prim"),
        (12, "cardboard_image_path", "string", False, "prim"),
        (13, "logo_image_path", "string", False, "prim"),
        (14, "total_days", "int", False, "prim"),
        (15, "is_loop", "bool", False, "prim"),
        (16, "order", "int", False, "prim"),
        (17, "details", "LoginBonusDetail", True, "model"),
        (18, "navigation_spine_id", "string", False, "prim"),
        (19, "voice_asset_id", "string", False, "prim"),
        (20, "head_motion_master_id", "long", False, "prim"),
        (21, "facial_expression_master_id", "long", False, "prim"),
        (22, "head_direction_master_id", "long", False, "prim"),
        (23, "body_motion_master_id", "long", False, "prim"),
        (24, "lip_sync_master_id", "long", False, "prim"),
        (25, "layout_type", "LoginBonusLayoutTypes", False, "enum"),
        (26, "comeback_campaign_master_id", "long", False, "prim"),
        (27, "login_bonus_spine_group", "LoginBonusSpineGroup", False, "model"),
    )


@dataclass
class LoginBonusSpineDetail(MsgpackModel):
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

    _FIELDS = (
        (0, "target_value1", "long", False, "prim"),
        (1, "target_value2", "long", False, "prim"),
        (2, "message_template", "string", False, "prim"),
        (3, "navigation_spine_id", "string", False, "prim"),
        (4, "voice_asset_id", "string", False, "prim"),
        (5, "head_motion_master_id", "long", False, "prim"),
        (6, "facial_expression_master_id", "long", False, "prim"),
        (7, "head_direction_master_id", "long", False, "prim"),
        (8, "body_motion_master_id", "long", False, "prim"),
        (9, "lip_sync_master_id", "long", False, "prim"),
    )


@dataclass
class LoginBonusSpineGroup(MsgpackModel):
    spine_select_type: Optional[int] = None
    details: Optional[List["LoginBonusSpineDetail"]] = None

    _FIELDS = (
        (0, "spine_select_type", "LoginBonusSpineSelectType", False, "enum"),
        (1, "details", "LoginBonusSpineDetail", True, "model"),
    )


@dataclass
class LoginPayload(MsgpackModel):
    push_notification_token: Optional[str] = None

    _FIELDS = ((0, "push_notification_token", "string", False, "prim"),)


@dataclass
class LoginResult(MsgpackModel):
    invalided_star_passes: Optional[List[int]] = None
    login_pass_notification: Optional[int] = None
    is_approaching_login_pass_invalided: Optional[bool] = None
    invalided_item_master_ids: Optional[List[int]] = None
    approaching_item_master_ids: Optional[List[int]] = None
    story_event_point_exchange_result: Optional[
        List["StoryEventPointExchangeResult"]
    ] = None
    invalided_buff_item_master_ids: Optional[List[int]] = None

    _FIELDS = (
        (0, "invalided_star_passes", "StarPassTypes", True, "enum"),
        (1, "login_pass_notification", "LoginPassNotificationTypes", False, "enum"),
        (2, "is_approaching_login_pass_invalided", "bool", False, "prim"),
        (3, "invalided_item_master_ids", "long", True, "prim"),
        (4, "approaching_item_master_ids", "long", True, "prim"),
        (
            5,
            "story_event_point_exchange_result",
            "StoryEventPointExchangeResult",
            True,
            "model",
        ),
        (6, "invalided_buff_item_master_ids", "long", True, "prim"),
    )


@dataclass
class MainCharacter(MsgpackModel):
    character_master_id: Optional[int] = None
    awakening_phase: Optional[int] = None
    talent_stage: Optional[int] = None
    level: Optional[int] = None
    display_awakening_status: Optional[bool] = None

    _FIELDS = (
        (0, "character_master_id", "long", False, "prim"),
        (1, "awakening_phase", "int", False, "prim"),
        (2, "talent_stage", "int", False, "prim"),
        (3, "level", "int", False, "prim"),
        (4, "display_awakening_status", "bool", False, "prim"),
    )


@dataclass
class MarketResult(MsgpackModel):
    things: Optional[List["MarketThing"]] = None
    required_jewel_for_refresh: Optional[int] = None

    _FIELDS = (
        (0, "things", "MarketThing", True, "model"),
        (1, "required_jewel_for_refresh", "int", False, "prim"),
    )


@dataclass
class MarketThing(MsgpackModel):
    frame_number: Optional[int] = None
    market_frame_thing_master_id: Optional[int] = None
    has_purchased: Optional[bool] = None
    discount_percent: Optional[int] = None

    _FIELDS = (
        (0, "frame_number", "long", False, "prim"),
        (1, "market_frame_thing_master_id", "long", False, "prim"),
        (4, "has_purchased", "bool", False, "prim"),
        (5, "discount_percent", "int", False, "prim"),
    )


@dataclass
class MasterDataManifest(MsgpackModel):
    uri: Optional[str] = None
    sas_token: Optional[str] = None
    version: Optional[str] = None
    publish_timestamp: Optional[int] = None

    _FIELDS = (
        (0, "uri", "string", False, "prim"),
        (1, "sas_token", "string", False, "prim"),
        (2, "version", "string", False, "prim"),
        (3, "publish_timestamp", "long", False, "prim"),
    )


@dataclass
class MatchingGhostLiveResult(MsgpackModel):
    ghost_live_master_id: Optional[int] = None
    ghost_user_profile: Optional["UserProfileDetail"] = None
    ghost_live_info: Optional["GhostLiveInfo"] = None

    _FIELDS = (
        (0, "ghost_live_master_id", "long", False, "prim"),
        (1, "ghost_user_profile", "UserProfileDetail", False, "model"),
        (2, "ghost_live_info", "GhostLiveInfo", False, "model"),
    )


@dataclass
class MissionPassRewardsResult(MsgpackModel):
    mission_pass_rewards: Optional[List["ReceivedThing"]] = None
    reward_result: Optional[int] = None

    _FIELDS = (
        (0, "mission_pass_rewards", "ReceivedThing", True, "model"),
        (1, "reward_result", "MissionPassRewardStatus", False, "enum"),
    )


@dataclass
class MultiLiveAdditionalScoreBlock(MsgpackModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    time_event_second: Optional[int] = None
    combo: Optional[int] = None

    _FIELDS = (
        (0, "hash", "long", False, "prim"),
        (1, "score", "long", False, "prim"),
        (2, "life", "int", False, "prim"),
        (3, "time_event_second", "int", False, "prim"),
        (4, "combo", "int", False, "prim"),
    )


@dataclass
class MultiLiveInformation(MsgpackModel):
    scores: Optional["Dictionary"] = None

    _FIELDS = ((0, "scores", "Dictionary", False, "model"),)


@dataclass
class MultiRoomCreateResult(MsgpackModel):
    hashed_multi_room_id: Optional[str] = None
    room_detail: Optional["MultiRoomDetailResult"] = None

    _FIELDS = (
        (0, "hashed_multi_room_id", "string", False, "prim"),
        (1, "room_detail", "MultiRoomDetailResult", False, "model"),
    )


@dataclass
class MultiRoomDetailResult(MsgpackModel):
    multi_room_information_result: Optional["MultiRoomInformationResult"] = None
    multi_room_rankings: Optional[List["MultiRoomRanking"]] = None
    is_finished: Optional[bool] = None
    password: Optional[str] = None

    _FIELDS = (
        (
            0,
            "multi_room_information_result",
            "MultiRoomInformationResult",
            False,
            "model",
        ),
        (1, "multi_room_rankings", "MultiRoomRanking", True, "model"),
        (2, "is_finished", "bool", False, "prim"),
        (3, "password", "string", False, "prim"),
    )


@dataclass
class MultiRoomInformationResult(MsgpackModel):
    hashed_multi_room_id: Optional[str] = None
    room_name: Optional[str] = None
    play_mode: Optional[int] = None
    joined_member_count: Optional[int] = None
    can_join_max_member: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    live_master_id1: Optional[int] = None
    live_master_id2: Optional[int] = None
    live_master_id3: Optional[int] = None
    has_password: Optional[bool] = None

    _FIELDS = (
        (0, "hashed_multi_room_id", "string", False, "prim"),
        (1, "room_name", "string", False, "prim"),
        (2, "play_mode", "MultiRoomPlayModes", False, "enum"),
        (3, "joined_member_count", "int", False, "prim"),
        (4, "can_join_max_member", "int", False, "prim"),
        (5, "start_date", "DateTime", False, "prim"),
        (6, "end_date", "DateTime", False, "prim"),
        (7, "live_master_id1", "long", False, "prim"),
        (8, "live_master_id2", "long", False, "prim"),
        (9, "live_master_id3", "long", False, "prim"),
        (10, "has_password", "bool", False, "prim"),
    )


@dataclass
class MultiRoomInvitedResult(MsgpackModel):
    owner_user_name: Optional[str] = None
    multi_room_information_result: Optional["MultiRoomInformationResult"] = None

    _FIELDS = (
        (0, "owner_user_name", "string", False, "prim"),
        (
            1,
            "multi_room_information_result",
            "MultiRoomInformationResult",
            False,
            "model",
        ),
    )


@dataclass
class MultiRoomJoinnedResult(MsgpackModel):
    my_rank: Optional[int] = None
    my_score: Optional[int] = None
    my_total_achievement_rate_percent_record: Optional["Decimal"] = None
    multi_room_information_result: Optional["MultiRoomInformationResult"] = None

    _FIELDS = (
        (0, "my_rank", "int", False, "prim"),
        (1, "my_score", "long", False, "prim"),
        (2, "my_total_achievement_rate_percent_record", "Decimal", False, "model"),
        (
            3,
            "multi_room_information_result",
            "MultiRoomInformationResult",
            False,
            "model",
        ),
    )


@dataclass
class MultiRoomPartySlot(MsgpackModel):
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
    current_status: Optional["Status"] = None

    _FIELDS = (
        (0, "position", "int", False, "prim"),
        (1, "character_master_id", "long", False, "prim"),
        (2, "character_level", "int", False, "prim"),
        (3, "character_talent_stage", "int", False, "prim"),
        (4, "character_awakening_phase", "int", False, "prim"),
        (5, "character_display_awakening_status", "bool", False, "prim"),
        (6, "poster_master_id", "long", False, "prim"),
        (7, "poster_level", "int", False, "prim"),
        (8, "poster_breakthrough_phase", "int", False, "prim"),
        (9, "accessory_master_id", "long", False, "prim"),
        (10, "accessory_level", "int", False, "prim"),
        (11, "u_accessory_id", "long", False, "prim"),
        (12, "current_status", "Status", False, "model"),
    )


@dataclass
class MultiRoomRanking(MsgpackModel):
    user_id: Optional[str] = None
    rank: Optional[int] = None
    is_owner: Optional[bool] = None
    score: Optional[int] = None
    total_achievement_rate_percent_record: Optional["Decimal"] = None
    best_record_challenge_count: Optional[int] = None
    best_record_date: Optional[str] = None
    user_profile: Optional["UserProfile"] = None
    party_info: Optional["PartyInfo"] = None
    note_result: Optional["NoteResult"] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "rank", "int", False, "prim"),
        (2, "is_owner", "bool", False, "prim"),
        (3, "score", "long", False, "prim"),
        (4, "total_achievement_rate_percent_record", "Decimal", False, "model"),
        (5, "best_record_challenge_count", "int", False, "prim"),
        (6, "best_record_date", "DateTime", False, "prim"),
        (7, "user_profile", "UserProfile", False, "model"),
        (8, "party_info", "PartyInfo", False, "model"),
        (9, "note_result", "NoteResult", False, "model"),
    )


@dataclass
class MusicCourseRandomSelectResult(MsgpackModel):
    details: Optional[List["MusicCourseRandomSelectResultDetail"]] = None

    _FIELDS = ((0, "details", "MusicCourseRandomSelectResultDetail", True, "model"),)


@dataclass
class MusicCourseRandomSelectResultDetail(MsgpackModel):
    set_list_number: Optional[int] = None
    live_master_id: Optional[int] = None

    _FIELDS = (
        (0, "set_list_number", "int", False, "prim"),
        (1, "live_master_id", "long", False, "prim"),
    )


@dataclass
class MusicCourseRankingPayload(MsgpackModel):
    user_id: Optional[int] = None
    current_challenge_count: Optional[int] = None
    perfect_star: Optional[int] = None
    perfect: Optional[int] = None
    great: Optional[int] = None
    good: Optional[int] = None
    bad: Optional[int] = None
    miss: Optional[int] = None
    total_achievement_rate_percent_record: Optional["Decimal"] = None
    best_record_challenge_count: Optional[int] = None
    best_record_date: Optional[str] = None

    _FIELDS = (
        (0, "user_id", "long", False, "prim"),
        (1, "current_challenge_count", "int", False, "prim"),
        (2, "perfect_star", "int", False, "prim"),
        (3, "perfect", "int", False, "prim"),
        (4, "great", "int", False, "prim"),
        (5, "good", "int", False, "prim"),
        (6, "bad", "int", False, "prim"),
        (7, "miss", "int", False, "prim"),
        (8, "total_achievement_rate_percent_record", "Decimal", False, "model"),
        (9, "best_record_challenge_count", "int", False, "prim"),
        (10, "best_record_date", "DateTime", False, "prim"),
    )


@dataclass
class MyCircleInformationResult(MsgpackModel):
    u_circle_hashed_id: Optional[str] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    play_time_start_type: Optional[int] = None
    play_time_end_type: Optional[int] = None
    entry_type: Optional[int] = None
    member_count: Optional[int] = None
    my_authority: Optional[int] = None
    result_status: Optional[int] = None
    circle_banner: Optional["CircleBanner"] = None
    company_master_id: Optional[int] = None
    character_base_master_id: Optional[int] = None
    support_company_information: Optional["SupportCompanyInformation"] = None
    support_company: Optional[int] = None
    daily_added_support_point: Optional[int] = None
    is_publish_ranking: Optional[bool] = None
    stamina_last_received_at: Optional[str] = None
    circle_authority_update_type: Optional[int] = None

    _FIELDS = (
        (0, "u_circle_hashed_id", "string", False, "prim"),
        (1, "name", "string", False, "prim"),
        (2, "comment", "string", False, "prim"),
        (3, "play_time_start_type", "PlayTimeTypes", False, "enum"),
        (4, "play_time_end_type", "PlayTimeTypes", False, "enum"),
        (5, "entry_type", "EntryTypes", False, "enum"),
        (6, "member_count", "int", False, "prim"),
        (7, "my_authority", "CircleAuthorities", False, "enum"),
        (8, "result_status", "CircleResultStatus", False, "enum"),
        (9, "circle_banner", "CircleBanner", False, "model"),
        (10, "company_master_id", "long", False, "prim"),
        (11, "character_base_master_id", "long", False, "prim"),
        (
            12,
            "support_company_information",
            "SupportCompanyInformation",
            False,
            "model",
        ),
        (13, "support_company", "Companies", False, "enum"),
        (14, "daily_added_support_point", "int", False, "prim"),
        (15, "is_publish_ranking", "bool", False, "prim"),
        (16, "stamina_last_received_at", "DateTime", False, "prim"),
        (
            17,
            "circle_authority_update_type",
            "CircleAuthorityUpdateTypes",
            False,
            "enum",
        ),
    )


@dataclass
class NoteJudgePayload(MsgpackModel):
    timing: Optional[int] = None
    count: Optional[int] = None

    _FIELDS = (
        (0, "timing", "TimingTypes", False, "enum"),
        (1, "count", "int", False, "prim"),
    )


@dataclass
class NoteResult(MsgpackModel):
    perfect_star: Optional[int] = None
    perfect: Optional[int] = None
    great: Optional[int] = None
    good: Optional[int] = None
    bad: Optional[int] = None
    miss: Optional[int] = None

    _FIELDS = (
        (0, "perfect_star", "int", False, "prim"),
        (1, "perfect", "int", False, "prim"),
        (2, "great", "int", False, "prim"),
        (3, "good", "int", False, "prim"),
        (4, "bad", "int", False, "prim"),
        (5, "miss", "int", False, "prim"),
    )


@dataclass
class NotificationContentResult(MsgpackModel):
    id_: Optional[int] = None
    body: Optional[str] = None
    title: Optional[str] = None
    posting_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    notification_tab_category: Optional[int] = None
    notification_category: Optional[int] = None
    banner_path: Optional[str] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (1, "body", "string", False, "prim"),
        (2, "title", "string", False, "prim"),
        (3, "posting_at", "DateTime", False, "prim"),
        (4, "last_updated_at", "DateTime", False, "prim"),
        (5, "notification_tab_category", "NotificationTabCategory", False, "enum"),
        (6, "notification_category", "NotificationCategory", False, "enum"),
        (7, "banner_path", "string", False, "prim"),
    )


@dataclass
class NotificationResult(MsgpackModel):
    id_: Optional[int] = None
    banner_path: Optional[str] = None
    title: Optional[str] = None
    posting_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    notification_tab_category: Optional[int] = None
    notification_category: Optional[int] = None
    is_confirmation: Optional[bool] = None
    order: Optional[int] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (1, "banner_path", "string", False, "prim"),
        (2, "title", "string", False, "prim"),
        (3, "posting_at", "DateTime", False, "prim"),
        (4, "last_updated_at", "DateTime", False, "prim"),
        (5, "notification_tab_category", "NotificationTabCategory", False, "enum"),
        (6, "notification_category", "NotificationCategory", False, "enum"),
        (7, "is_confirmation", "bool", False, "prim"),
        (8, "order", "int", False, "prim"),
    )


@dataclass
class PartyInfo(MsgpackModel):
    leader_position: Optional[int] = None
    multi_room_party_slots: Optional[List["MultiRoomPartySlot"]] = None

    _FIELDS = (
        (0, "leader_position", "int", False, "prim"),
        (1, "multi_room_party_slots", "MultiRoomPartySlot", True, "model"),
    )


@dataclass
class PartyPayload(MsgpackModel):
    leader_position: Optional[int] = None
    party_slot_payload: Optional[List["PartySlotPayload"]] = None

    _FIELDS = (
        (0, "leader_position", "int", False, "prim"),
        (1, "party_slot_payload", "PartySlotPayload", True, "model"),
    )


@dataclass
class PartySlotAccessoryPayload(MsgpackModel):
    m_accessory_id: Optional[int] = None
    level: Optional[int] = None
    m_accessory_effect_id1: Optional[int] = None
    m_accessory_effect_id2: Optional[int] = None
    m_accessory_effect_id3: Optional[int] = None

    _FIELDS = (
        (0, "m_accessory_id", "long", False, "prim"),
        (1, "level", "int", False, "prim"),
        (2, "m_accessory_effect_id1", "long", False, "prim"),
        (3, "m_accessory_effect_id2", "long", False, "prim"),
        (4, "m_accessory_effect_id3", "long", False, "prim"),
    )


@dataclass
class PartySlotCharacterPayload(MsgpackModel):
    m_character_id: Optional[int] = None
    talent_stage: Optional[int] = None
    awakening_phase: Optional[int] = None
    level: Optional[int] = None
    sense_level: Optional[int] = None
    current_experience: Optional[int] = None
    released_episode_order: Optional[int] = None
    read_episode_order: Optional[int] = None
    display_awakening_status: Optional[bool] = None

    _FIELDS = (
        (0, "m_character_id", "long", False, "prim"),
        (1, "talent_stage", "int", False, "prim"),
        (2, "awakening_phase", "int", False, "prim"),
        (3, "level", "int", False, "prim"),
        (4, "sense_level", "int", False, "prim"),
        (5, "current_experience", "int", False, "prim"),
        (6, "released_episode_order", "CharacterEpisodeOrder", False, "enum"),
        (7, "read_episode_order", "CharacterEpisodeOrder", False, "enum"),
        (8, "display_awakening_status", "bool", False, "prim"),
    )


@dataclass
class PartySlotDetail(MsgpackModel):
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

    _FIELDS = (
        (0, "position", "int", False, "prim"),
        (1, "character_master_id", "long", False, "prim"),
        (2, "character_level", "int", False, "prim"),
        (3, "character_talent_stage", "int", False, "prim"),
        (4, "character_awakening_phase", "int", False, "prim"),
        (5, "character_display_awakening_status", "bool", False, "prim"),
        (6, "poster_master_id", "long", False, "prim"),
        (7, "poster_level", "int", False, "prim"),
        (8, "poster_breakthrough_phase", "int", False, "prim"),
        (9, "accessory_master_id", "long", False, "prim"),
        (10, "accessory_level", "int", False, "prim"),
        (11, "current_status_vocal", "int", False, "prim"),
        (12, "current_status_expression", "int", False, "prim"),
        (13, "current_status_concentration", "int", False, "prim"),
        (14, "u_accessory_id", "long", False, "prim"),
    )


@dataclass
class PartySlotPayload(MsgpackModel):
    position: Optional[int] = None
    party_slot_character_payload: Optional["PartySlotCharacterPayload"] = None
    party_slot_poster_payload: Optional["PartySlotPosterPayload"] = None
    party_slot_accessory_payload: Optional["PartySlotAccessoryPayload"] = None

    _FIELDS = (
        (0, "position", "int", False, "prim"),
        (
            1,
            "party_slot_character_payload",
            "PartySlotCharacterPayload",
            False,
            "model",
        ),
        (2, "party_slot_poster_payload", "PartySlotPosterPayload", False, "model"),
        (
            3,
            "party_slot_accessory_payload",
            "PartySlotAccessoryPayload",
            False,
            "model",
        ),
    )


@dataclass
class PartySlotPosterPayload(MsgpackModel):
    m_poster_id: Optional[int] = None
    level: Optional[int] = None
    phase: Optional[int] = None
    released_episode: Optional[int] = None

    _FIELDS = (
        (0, "m_poster_id", "long", False, "prim"),
        (1, "level", "int", False, "prim"),
        (2, "phase", "int", False, "prim"),
        (3, "released_episode", "PosterEpisodeTypes", False, "enum"),
    )


@dataclass
class PhotoAppearedCharacter(MsgpackModel):
    character_base_master_id: Optional[int] = None
    is_main_character: Optional[bool] = None

    _FIELDS = (
        (0, "character_base_master_id", "long", False, "prim"),
        (1, "is_main_character", "bool", False, "prim"),
    )


@dataclass
class PlayerRankPointResult(MsgpackModel):
    rank_before: Optional[int] = None
    rank_after: Optional[int] = None
    rank_point_before: Optional[int] = None
    rank_point_after: Optional[int] = None
    rank_point_acquired: Optional[int] = None
    stamina_before: Optional[int] = None

    _FIELDS = (
        (0, "rank_before", "int", False, "prim"),
        (1, "rank_after", "int", False, "prim"),
        (2, "rank_point_before", "int", False, "prim"),
        (3, "rank_point_after", "int", False, "prim"),
        (4, "rank_point_acquired", "int", False, "prim"),
        (5, "stamina_before", "int", False, "prim"),
    )


@dataclass
class PosterAlternativeImagePayload(MsgpackModel):
    poster_id: Optional[int] = None
    pattern: Optional[int] = None

    _FIELDS = (
        (0, "poster_id", "long", False, "prim"),
        (1, "pattern", "int", False, "prim"),
    )


@dataclass
class PosterFavoritePayload(MsgpackModel):
    poster_id: Optional[int] = None
    set_favorite: Optional[bool] = None

    _FIELDS = (
        (0, "poster_id", "long", False, "prim"),
        (1, "set_favorite", "bool", False, "prim"),
    )


@dataclass
class PosterLineupResult(MsgpackModel):
    normal_probabilities: Optional[List["PosterRarityProbability"]] = None
    fixed_probabilities: Optional[List["PosterRarityProbability"]] = None
    normal_lineup_items: Optional[List["GachaLineupItemProbability"]] = None
    fixed_lineup_items: Optional[List["GachaLineupItemProbability"]] = None

    _FIELDS = (
        (0, "normal_probabilities", "PosterRarityProbability", True, "model"),
        (1, "fixed_probabilities", "PosterRarityProbability", True, "model"),
        (2, "normal_lineup_items", "GachaLineupItemProbability", True, "model"),
        (3, "fixed_lineup_items", "GachaLineupItemProbability", True, "model"),
    )


@dataclass
class PosterRarityProbability(MsgpackModel):
    rarity: Optional[int] = None
    probability: Optional[float] = None

    _FIELDS = (
        (0, "rarity", "PossessionRarities", False, "enum"),
        (1, "probability", "double", False, "prim"),
    )


@dataclass
class ProcessPaymentResult(MsgpackModel):
    result: Optional[int] = None

    _FIELDS = ((0, "result", "ProcessPaymentTransactionResult", False, "enum"),)


@dataclass
class PurchaseItemPayload(MsgpackModel):
    m_jewel_shop_item_id: Optional[int] = None

    _FIELDS = ((0, "m_jewel_shop_item_id", "long", False, "prim"),)


@dataclass
class RateResult(MsgpackModel):
    achievement_rate_result: Optional["RateUpdateResult"] = None
    live_rate_result: Optional["RateUpdateResult"] = None
    total_rate_before: Optional[float] = None
    total_rate_after: Optional[float] = None

    _FIELDS = (
        (0, "achievement_rate_result", "RateUpdateResult", False, "model"),
        (1, "live_rate_result", "RateUpdateResult", False, "model"),
        (2, "total_rate_before", "double", False, "prim"),
        (3, "total_rate_after", "double", False, "prim"),
    )


@dataclass
class RateUpdateResult(MsgpackModel):
    best_ever: Optional[float] = None
    this_time: Optional[float] = None

    _FIELDS = (
        (0, "best_ever", "double", False, "prim"),
        (1, "this_time", "double", False, "prim"),
    )


@dataclass
class RawHighScoreRankingResult(MsgpackModel):
    raw_ranking: Optional[List["RawRankingWithLongPoint"]] = None
    high_score_parties: Optional[List["HighScoreParty"]] = None
    high_score_buffs: Optional[List["HighScoreBuff"]] = None
    user_profiles: Optional[List["UserProfile"]] = None

    _FIELDS = (
        (0, "raw_ranking", "RawRankingWithLongPoint", True, "model"),
        (1, "high_score_parties", "HighScoreParty", True, "model"),
        (2, "high_score_buffs", "HighScoreBuff", True, "model"),
        (3, "user_profiles", "UserProfile", True, "model"),
    )


@dataclass
class RawRanking(MsgpackModel):
    rank: Optional[int] = None
    point: Optional[int] = None
    user_id: Optional[str] = None
    group_value: Optional[int] = None

    _FIELDS = (
        (0, "rank", "int", False, "prim"),
        (1, "point", "int", False, "prim"),
        (2, "user_id", "string", False, "prim"),
        (3, "group_value", "int", False, "prim"),
    )


@dataclass
class RawRankingResult(MsgpackModel):
    raw_ranking: Optional[List["RawRanking"]] = None
    user_profiles: Optional[List["UserProfile"]] = None

    _FIELDS = (
        (0, "raw_ranking", "RawRanking", True, "model"),
        (1, "user_profiles", "UserProfile", True, "model"),
    )


@dataclass
class RawRankingWithLongPoint(MsgpackModel):
    rank: Optional[int] = None
    point: Optional[int] = None
    user_id: Optional[str] = None

    _FIELDS = (
        (0, "rank", "int", False, "prim"),
        (1, "point", "long", False, "prim"),
        (2, "user_id", "string", False, "prim"),
    )


@dataclass
class ReadNotificationPayload(MsgpackModel):
    tab_category: Optional[int] = None
    read_at: Optional[str] = None

    _FIELDS = (
        (0, "tab_category", "NotificationTabCategory", False, "enum"),
        (1, "read_at", "DateTime", False, "prim"),
    )


@dataclass
class ReceivedThing(MsgpackModel):
    type: Optional[int] = None
    id_: Optional[int] = None
    quantity: Optional[int] = None
    original_type: Optional[int] = None
    original_id: Optional[int] = None
    after_phase: Optional[int] = None
    sent_inbox: Optional[bool] = None

    _FIELDS = (
        (0, "type", "ThingTypes", False, "enum"),
        (1, "id_", "long", False, "prim"),
        (2, "quantity", "int", False, "prim"),
        (3, "original_type", "ThingTypes", False, "enum"),
        (4, "original_id", "long", False, "prim"),
        (5, "after_phase", "int", False, "prim"),
        (6, "sent_inbox", "bool", False, "prim"),
    )


@dataclass
class RegisterAppStorePaymentPayload(MsgpackModel):
    receipt_base64: Optional[str] = None

    _FIELDS = ((0, "receipt_base64", "string", False, "prim"),)


@dataclass
class RegisterBirthDayPayload(MsgpackModel):
    birth_date: Optional[str] = None

    _FIELDS = ((0, "birth_date", "DateTime", False, "prim"),)


@dataclass
class RegisterGooglePlayPaymentPayload(MsgpackModel):
    json: Optional[str] = None

    _FIELDS = ((0, "json", "string", False, "prim"),)


@dataclass
class RegisterPayload(MsgpackModel):
    name: Optional[str] = None

    _FIELDS = ((0, "name", "string", False, "prim"),)


@dataclass
class RegisterTakeOverPasswordPayload(MsgpackModel):
    password: Optional[str] = None

    _FIELDS = ((0, "password", "string", False, "prim"),)


@dataclass
class RollResult(MsgpackModel):
    roll_order: Optional[int] = None
    selected_slot: Optional[int] = None
    roulette_prize_master_id: Optional[int] = None

    _FIELDS = (
        (0, "roll_order", "int", False, "prim"),
        (1, "selected_slot", "int", False, "prim"),
        (2, "roulette_prize_master_id", "long", False, "prim"),
    )


@dataclass
class RouletteRollResult(MsgpackModel):
    roll_results: Optional[List["RollResult"]] = None

    _FIELDS = ((0, "roll_results", "RollResult", True, "model"),)


@dataclass
class ScoreWithDateResult(MsgpackModel):
    score: Optional[int] = None
    date: Optional[str] = None

    _FIELDS = (
        (0, "score", "long", False, "prim"),
        (1, "date", "DateTime", False, "prim"),
    )


@dataclass
class SelectMusicCourseRandomMusicPayload(MsgpackModel):
    music_course_master_id: Optional[int] = None
    music_course_gauge_type: Optional[int] = None

    _FIELDS = (
        (0, "music_course_master_id", "long", False, "prim"),
        (1, "music_course_gauge_type", "MusicCourseGaugeType", False, "enum"),
    )


@dataclass
class SellAccessoryPayload(MsgpackModel):
    u_accessory_ids: Optional[List[int]] = None

    _FIELDS = ((0, "u_accessory_ids", "long", True, "prim"),)


@dataclass
class Sense(MsgpackModel):
    id_: Optional[int] = None
    actor_id: Optional[int] = None
    cool_time: Optional[int] = None
    sense_type: Optional[int] = None
    acquirable_lights: Optional[List[int]] = None
    pre_sense_effect: Optional[List["Effect"]] = None
    sense_effect: Optional["SenseEffect"] = None
    poster_effect: Optional[List["Effect"]] = None
    accessory_effect: Optional[List["Effect"]] = None
    combination_sense_id: Optional[List[int]] = None
    sense_master_id: Optional[int] = None
    original_actor_id: Optional[int] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (1, "actor_id", "long", False, "prim"),
        (3, "cool_time", "int", False, "prim"),
        (4, "sense_type", "SenseTypes", False, "enum"),
        (5, "acquirable_lights", "SenseLightTypes", True, "enum"),
        (6, "pre_sense_effect", "Effect", True, "model"),
        (7, "sense_effect", "SenseEffect", False, "model"),
        (8, "poster_effect", "Effect", True, "model"),
        (9, "accessory_effect", "Effect", True, "model"),
        (10, "combination_sense_id", "long", True, "prim"),
        (11, "sense_master_id", "long", False, "prim"),
        (12, "original_actor_id", "long", False, "prim"),
    )


@dataclass
class SenseCoolTime(MsgpackModel):
    position: Optional[int] = None
    cool_time: Optional[int] = None

    _FIELDS = (
        (0, "position", "int", False, "prim"),
        (1, "cool_time", "int", False, "prim"),
    )


@dataclass
class SenseEffect(MsgpackModel):
    score_factor: Optional[int] = None
    principal: Optional[int] = None
    branch_condition: Optional[int] = None
    effect_branches: Optional[List["EffectBranch"]] = None

    _FIELDS = (
        (0, "score_factor", "int", False, "prim"),
        (1, "principal", "int", False, "prim"),
        (2, "branch_condition", "BranchConditionTypes", False, "enum"),
        (3, "effect_branches", "EffectBranch", True, "model"),
    )


@dataclass
class SenseScoreBlock(MsgpackModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    time_event_second: Optional[int] = None
    sense_id: Optional[int] = None
    combo: Optional[int] = None

    _FIELDS = (
        (0, "hash", "long", False, "prim"),
        (1, "score", "long", False, "prim"),
        (2, "life", "int", False, "prim"),
        (3, "time_event_second", "int", False, "prim"),
        (4, "sense_id", "long", False, "prim"),
        (5, "combo", "int", False, "prim"),
    )


@dataclass
class SenseTimingEvent(MsgpackModel):
    timing_seconds: Optional[int] = None
    position: Optional[int] = None
    event: Optional["TimingEvent"] = None

    _FIELDS = (
        (0, "timing_seconds", "int", False, "prim"),
        (1, "position", "int", False, "prim"),
        (2, "event", "TimingEvent", False, "model"),
    )


@dataclass
class SetAlbumPublishingPayload(MsgpackModel):
    publishing: Optional[bool] = None
    publish_page_number: Optional[int] = None

    _FIELDS = (
        (0, "publishing", "bool", False, "prim"),
        (1, "publish_page_number", "int", False, "prim"),
    )


@dataclass
class SetLessonPartyPayload(MsgpackModel):
    slots: Optional[List["SetLessonPartySlotPayload"]] = None

    _FIELDS = ((0, "slots", "SetLessonPartySlotPayload", True, "model"),)


@dataclass
class SetLessonPartySlotPayload(MsgpackModel):
    order: Optional[int] = None
    character_id: Optional[int] = None

    _FIELDS = (
        (0, "order", "int", False, "prim"),
        (1, "character_id", "long", False, "prim"),
    )


@dataclass
class SetPhotoTagPayload(MsgpackModel):
    photo_id: Optional[int] = None
    character_base_ids: Optional[List[int]] = None

    _FIELDS = (
        (0, "photo_id", "long", False, "prim"),
        (1, "character_base_ids", "long", True, "prim"),
    )


@dataclass
class SetSelectedThingsPayload(MsgpackModel):
    gacha_thing_ids: Optional[List[int]] = None

    _FIELDS = ((0, "gacha_thing_ids", "long", True, "prim"),)


@dataclass
class SpRateUpdateResult(MsgpackModel):
    best_ever: Optional[int] = None
    this_time: Optional[int] = None
    best_ever_total: Optional[int] = None
    this_time_total: Optional[int] = None

    _FIELDS = (
        (0, "best_ever", "int", False, "prim"),
        (1, "this_time", "int", False, "prim"),
        (2, "best_ever_total", "int", False, "prim"),
        (3, "this_time_total", "int", False, "prim"),
    )


@dataclass
class StarAct(MsgpackModel):
    score_factor: Optional[int] = None
    actor_id: Optional[int] = None
    branch_condition: Optional[int] = None
    effect_branches: Optional[List["EffectBranch"]] = None

    _FIELDS = (
        (0, "score_factor", "int", False, "prim"),
        (1, "actor_id", "long", False, "prim"),
        (2, "branch_condition", "BranchConditionTypes", False, "enum"),
        (3, "effect_branches", "EffectBranch", True, "model"),
    )


@dataclass
class StarActScoreBlock(MsgpackModel):
    hash: Optional[int] = None
    score: Optional[int] = None
    life: Optional[int] = None
    time_event_second: Optional[int] = None
    combo: Optional[int] = None

    _FIELDS = (
        (0, "hash", "long", False, "prim"),
        (1, "score", "long", False, "prim"),
        (2, "life", "int", False, "prim"),
        (3, "time_event_second", "int", False, "prim"),
        (4, "combo", "int", False, "prim"),
    )


@dataclass
class StarPointResult(MsgpackModel):
    rank_before: Optional[int] = None
    rank_after: Optional[int] = None
    star_point_before: Optional[int] = None
    star_point_after: Optional[int] = None
    star_point_acquired: Optional[int] = None
    received_reward: Optional[List["ReceivedThing"]] = None

    _FIELDS = (
        (0, "rank_before", "int", False, "prim"),
        (1, "rank_after", "int", False, "prim"),
        (2, "star_point_before", "int", False, "prim"),
        (3, "star_point_after", "int", False, "prim"),
        (4, "star_point_acquired", "int", False, "prim"),
        (5, "received_reward", "ReceivedThing", True, "model"),
    )


@dataclass
class StartLessonPayload(MsgpackModel):
    character_base_master_id: Optional[int] = None
    live_master_id: Optional[int] = None

    _FIELDS = (
        (0, "character_base_master_id", "int", False, "prim"),
        (1, "live_master_id", "long", False, "prim"),
    )


@dataclass
class StartLivePayload(MsgpackModel):
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
    music_course_gauge_type: Optional[int] = None
    ghost_live_master_id: Optional[int] = None
    trial_party_event_stage_master_id: Optional[int] = None

    _FIELDS = (
        (0, "party_id", "long", False, "prim"),
        (1, "live_master_id", "long", False, "prim"),
        (2, "audition_master_id", "long", False, "prim"),
        (3, "league_master_id", "long", False, "prim"),
        (4, "use_stamina", "bool", False, "prim"),
        (5, "stamina_consumption_ratio", "int", False, "prim"),
        (6, "live_setting_master_id", "long", False, "prim"),
        (7, "is_auto_play", "bool", False, "prim"),
        (8, "is_story_event_challenge", "bool", False, "prim"),
        (9, "concert_stage_master_id", "long", False, "prim"),
        (10, "bonus_live_stage_master_id", "long", False, "prim"),
        (11, "music_course_detail_master_id", "long", False, "prim"),
        (12, "music_course_gauge_type", "MusicCourseGaugeType", False, "enum"),
        (13, "ghost_live_master_id", "long", False, "prim"),
        (14, "trial_party_event_stage_master_id", "long", False, "prim"),
    )


@dataclass
class StartMultiLivePayload(MsgpackModel):
    live_master_id: Optional[int] = None
    multi_live_id: Optional[int] = None
    use_stamina: Optional[bool] = None
    stamina_consumption_ratio: Optional[int] = None
    party_id: Optional[int] = None

    _FIELDS = (
        (0, "live_master_id", "long", False, "prim"),
        (1, "multi_live_id", "long", False, "prim"),
        (2, "use_stamina", "bool", False, "prim"),
        (3, "stamina_consumption_ratio", "int", False, "prim"),
        (4, "party_id", "long", False, "prim"),
    )


@dataclass
class StartMultiRoomLivePayload(MsgpackModel):
    hashed_multi_room_id: Optional[str] = None
    live_master_id: Optional[int] = None
    party_id: Optional[int] = None

    _FIELDS = (
        (0, "hashed_multi_room_id", "string", False, "prim"),
        (1, "live_master_id", "long", False, "prim"),
        (2, "party_id", "long", False, "prim"),
    )


@dataclass
class StartTournamentPayload(MsgpackModel):
    tournament_detail_master_id: Optional[int] = None
    party_id: Optional[int] = None
    stamina_consumption_ratio: Optional[int] = None

    _FIELDS = (
        (0, "tournament_detail_master_id", "long", False, "prim"),
        (1, "party_id", "long", False, "prim"),
        (2, "stamina_consumption_ratio", "int", False, "prim"),
    )


@dataclass
class StartTripleCastLivePayload(MsgpackModel):
    m_live_id: Optional[int] = None
    m_triple_cast_id: Optional[int] = None

    _FIELDS = (
        (0, "m_live_id", "long", False, "prim"),
        (1, "m_triple_cast_id", "long", False, "prim"),
    )


@dataclass
class StartTripleCastLiveResult(MsgpackModel):
    live_units: Optional[List["LiveUnitWithOrder"]] = None

    _FIELDS = ((0, "live_units", "LiveUnitWithOrder", True, "model"),)


@dataclass
class Status(MsgpackModel):
    concentration: Optional[int] = None
    expression: Optional[int] = None
    vocal: Optional[int] = None
    total_status: Optional[int] = None

    _FIELDS = (
        (0, "concentration", "int", False, "prim"),
        (1, "expression", "int", False, "prim"),
        (2, "vocal", "int", False, "prim"),
        (3, "total_status", "int", False, "prim"),
    )


@dataclass
class StoryEventCampInfo(MsgpackModel):
    raw_ranking: Optional["RawRanking"] = None
    camp1_total_point: Optional[int] = None
    camp2_total_point: Optional[int] = None

    _FIELDS = (
        (0, "raw_ranking", "RawRanking", False, "model"),
        (1, "camp1_total_point", "long", False, "prim"),
        (2, "camp2_total_point", "long", False, "prim"),
    )


@dataclass
class StoryEventMissionCircleProgress(MsgpackModel):
    story_event_circle_mission_master_id: Optional[int] = None
    current_count: Optional[int] = None

    _FIELDS = (
        (0, "story_event_circle_mission_master_id", "long", False, "prim"),
        (1, "current_count", "int", False, "prim"),
    )


@dataclass
class StoryEventMissionCircleProgressResult(MsgpackModel):
    is_success: Optional[bool] = None
    progresses: Optional[List["StoryEventMissionCircleProgress"]] = None

    _FIELDS = (
        (0, "is_success", "bool", False, "prim"),
        (1, "progresses", "StoryEventMissionCircleProgress", True, "model"),
    )


@dataclass
class StoryEventPointExchangeResult(MsgpackModel):
    story_event_master_id: Optional[int] = None
    before_story_event_point_amount: Optional[int] = None
    after_coin_amount: Optional[int] = None

    _FIELDS = (
        (0, "story_event_master_id", "long", False, "prim"),
        (1, "before_story_event_point_amount", "int", False, "prim"),
        (2, "after_coin_amount", "int", False, "prim"),
    )


@dataclass
class SupportCompanyInformation(MsgpackModel):
    sirius: Optional["SupportCompanyLevelStatus"] = None
    eden: Optional["SupportCompanyLevelStatus"] = None
    gingaza: Optional["SupportCompanyLevelStatus"] = None
    denki: Optional["SupportCompanyLevelStatus"] = None

    _FIELDS = (
        (0, "sirius", "SupportCompanyLevelStatus", False, "model"),
        (1, "eden", "SupportCompanyLevelStatus", False, "model"),
        (2, "gingaza", "SupportCompanyLevelStatus", False, "model"),
        (3, "denki", "SupportCompanyLevelStatus", False, "model"),
    )


@dataclass
class SupportCompanyLevelLimitDetail(MsgpackModel):
    order: Optional[int] = None
    quantity: Optional[int] = None

    _FIELDS = (
        (0, "order", "int", False, "prim"),
        (1, "quantity", "long", False, "prim"),
    )


@dataclass
class SupportCompanyLevelLimitPayload(MsgpackModel):
    company: Optional[int] = None
    coin_quantity: Optional[int] = None
    details: Optional[List["SupportCompanyLevelLimitDetail"]] = None

    _FIELDS = (
        (0, "company", "Companies", False, "enum"),
        (1, "coin_quantity", "long", False, "prim"),
        (2, "details", "SupportCompanyLevelLimitDetail", True, "model"),
    )


@dataclass
class SupportCompanyLevelLimitStatus(MsgpackModel):
    current_coin_quantity: Optional[int] = None
    details: Optional[List["SupportCompanyLevelLimitStatusDetail"]] = None

    _FIELDS = (
        (0, "current_coin_quantity", "long", False, "prim"),
        (1, "details", "SupportCompanyLevelLimitStatusDetail", True, "model"),
    )


@dataclass
class SupportCompanyLevelLimitStatusDetail(MsgpackModel):
    order: Optional[int] = None
    current_quantity: Optional[int] = None

    _FIELDS = (
        (0, "order", "int", False, "prim"),
        (1, "current_quantity", "long", False, "prim"),
    )


@dataclass
class SupportCompanyLevelStatus(MsgpackModel):
    level: Optional[int] = None
    current_support_point: Optional[int] = None
    last_level_upped_at: Optional[str] = None
    level_limit: Optional[int] = None
    level_limit_status: Optional["SupportCompanyLevelLimitStatus"] = None

    _FIELDS = (
        (0, "level", "int", False, "prim"),
        (1, "current_support_point", "int", False, "prim"),
        (2, "last_level_upped_at", "DateTime", False, "prim"),
        (3, "level_limit", "int", False, "prim"),
        (4, "level_limit_status", "SupportCompanyLevelLimitStatus", False, "model"),
    )


@dataclass
class TakeOverAccountPayload(MsgpackModel):
    linkage_code: Optional[str] = None
    password: Optional[str] = None

    _FIELDS = (
        (0, "linkage_code", "string", False, "prim"),
        (1, "password", "string", False, "prim"),
    )


@dataclass
class TakeOverAccountResult(MsgpackModel):
    is_success: Optional[bool] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    rank: Optional[int] = None
    login_token: Optional[str] = None

    _FIELDS = (
        (0, "is_success", "bool", False, "prim"),
        (1, "user_id", "string", False, "prim"),
        (2, "name", "string", False, "prim"),
        (3, "rank", "int", False, "prim"),
        (4, "login_token", "string", False, "prim"),
    )


@dataclass
class TakeOverCodeResult(MsgpackModel):
    is_success: Optional[bool] = None
    linkage_code: Optional[str] = None

    _FIELDS = (
        (0, "is_success", "bool", False, "prim"),
        (1, "linkage_code", "string", False, "prim"),
    )


@dataclass
class TimedConfirmationCode(MsgpackModel):
    confirmation_code: Optional[str] = None
    remaining_seconds: Optional[int] = None

    _FIELDS = (
        (0, "confirmation_code", "string", False, "prim"),
        (1, "remaining_seconds", "int", False, "prim"),
    )


@dataclass
class TimingEvent(MsgpackModel):
    total_sense_lights: Optional[List[int]] = None
    grant_sense_lights: Optional[List[int]] = None
    is_star_act: Optional[bool] = None
    lost_lights: Optional[bool] = None
    acquirable_lights: Optional[List[int]] = None
    sense_ids: Optional[List[int]] = None
    sense_voice_ids: Optional[List[int]] = None
    sense_master_id: Optional[int] = None

    _FIELDS = (
        (0, "total_sense_lights", "SenseLightTypes", True, "enum"),
        (1, "grant_sense_lights", "SenseLightTypes", True, "enum"),
        (2, "is_star_act", "bool", False, "prim"),
        (3, "lost_lights", "bool", False, "prim"),
        (4, "acquirable_lights", "SenseLightTypes", True, "enum"),
        (5, "sense_ids", "long", True, "prim"),
        (6, "sense_voice_ids", "long", True, "prim"),
        (7, "sense_master_id", "long", False, "prim"),
    )


@dataclass
class TotalPointEventInformationResult(MsgpackModel):
    current_total_point: Optional[int] = None

    _FIELDS = ((0, "current_total_point", "long", False, "prim"),)


@dataclass
class TotalPointEventRankingResult(MsgpackModel):
    raw_ranking: Optional[List["RawRankingWithLongPoint"]] = None
    user_profiles: Optional[List["UserProfile"]] = None

    _FIELDS = (
        (0, "raw_ranking", "RawRankingWithLongPoint", True, "model"),
        (1, "user_profiles", "UserProfile", True, "model"),
    )


@dataclass
class TournamentQualifyingInformationResult(MsgpackModel):
    entry_code: Optional[str] = None

    _FIELDS = ((0, "entry_code", "string", False, "prim"),)


@dataclass
class TournamentResult(MsgpackModel):
    best_ever_unique_score: Optional[int] = None
    this_time_unique_score: Optional[int] = None
    tournament_detail_master_id: Optional[int] = None

    _FIELDS = (
        (0, "best_ever_unique_score", "long", False, "prim"),
        (1, "this_time_unique_score", "long", False, "prim"),
        (2, "tournament_detail_master_id", "long", False, "prim"),
    )


@dataclass
class TransitionTokenResult(MsgpackModel):
    token: Optional[str] = None

    _FIELDS = ((0, "token", "string", False, "prim"),)


@dataclass
class TrialPartyEventResult(MsgpackModel):
    rewards: Optional[List["ReceivedThing"]] = None

    _FIELDS = ((0, "rewards", "ReceivedThing", True, "model"),)


@dataclass
class TrialPartyEventStageResult(MsgpackModel):
    principal_gauge_value: Optional[int] = None

    _FIELDS = ((0, "principal_gauge_value", "int", False, "prim"),)


@dataclass
class TripleCastPartyAndRankingResult(MsgpackModel):
    rank: Optional[int] = None
    user_id: Optional[str] = None
    best_score: Optional[int] = None
    triple_cast_master_id: Optional[int] = None
    class_type: Optional[int] = None
    difficulty: Optional[int] = None
    user_name: Optional[str] = None
    parties: Optional[List["TripleCastPartyResult"]] = None

    _FIELDS = (
        (0, "rank", "int", False, "prim"),
        (1, "user_id", "string", False, "prim"),
        (2, "best_score", "long", False, "prim"),
        (3, "triple_cast_master_id", "long", False, "prim"),
        (4, "class_type", "LeagueClassTypes", False, "enum"),
        (5, "difficulty", "MusicDifficulties", False, "enum"),
        (6, "user_name", "string", False, "prim"),
        (7, "parties", "TripleCastPartyResult", True, "model"),
    )


@dataclass
class TripleCastPartyResult(MsgpackModel):
    order: Optional[int] = None
    score: Optional[int] = None
    slots: Optional[List["LeaguePartySlotResult"]] = None

    _FIELDS = (
        (0, "order", "int", False, "prim"),
        (1, "score", "long", False, "prim"),
        (2, "slots", "LeaguePartySlotResult", True, "model"),
    )


@dataclass
class TripleCastPartyScore(MsgpackModel):
    order: Optional[int] = None
    score: Optional[int] = None

    _FIELDS = (
        (0, "order", "int", False, "prim"),
        (1, "score", "long", False, "prim"),
    )


@dataclass
class UpdateClearLampResult(MsgpackModel):
    clear_lamp: Optional[int] = None

    _FIELDS = ((0, "clear_lamp", "ClearLamps", False, "enum"),)


@dataclass
class UpdateGameHintPayload(MsgpackModel):
    categories: Optional[List[int]] = None

    _FIELDS = ((0, "categories", "PageCategories", True, "enum"),)


@dataclass
class UpdateHomeDisplayPreferencePayload(MsgpackModel):
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
    home_character_display_type: Optional[int] = None
    login_bonus_character_base_master_id: Optional[int] = None
    login_bonus_spine_costume_master_id: Optional[int] = None

    _FIELDS = (
        (0, "home_character_base_master_id", "long", False, "prim"),
        (2, "member_character_base_master_id", "long", False, "prim"),
        (3, "story_character_base_master_id", "long", False, "prim"),
        (4, "shop_character_base_master_id", "long", False, "prim"),
        (5, "home_costume_master_id", "long", False, "prim"),
        (7, "member_costume_master_id", "long", False, "prim"),
        (8, "story_costume_master_id", "long", False, "prim"),
        (9, "shop_costume_master_id", "long", False, "prim"),
        (10, "illust_character_master_id", "long", False, "prim"),
        (11, "display_awakening_status", "bool", False, "prim"),
        (12, "home_character_display_type", "HomeCharacterDisplayTypes", False, "enum"),
        (13, "login_bonus_character_base_master_id", "long", False, "prim"),
        (14, "login_bonus_spine_costume_master_id", "long", False, "prim"),
    )


@dataclass
class UpdateLastViewedAtPayload(MsgpackModel):
    viewed_shop_category_types: Optional[int] = None
    exchange_shop_master_id: Optional[int] = None

    _FIELDS = (
        (0, "viewed_shop_category_types", "ViewedShopCategoryTypes", False, "enum"),
        (1, "exchange_shop_master_id", "long", False, "prim"),
    )


@dataclass
class UpdateTutorialPayload(MsgpackModel):
    tutorial_status: Optional[int] = None

    _FIELDS = ((0, "tutorial_status", "TutorialStatus", False, "enum"),)


@dataclass
class UrlResult(MsgpackModel):
    url: Optional[str] = None

    _FIELDS = ((0, "url", "string", False, "prim"),)


@dataclass
class UseExperienceItemsPayload(MsgpackModel):
    item_master_id: Optional[int] = None
    quantity: Optional[int] = None

    _FIELDS = (
        (0, "item_master_id", "long", False, "prim"),
        (1, "quantity", "int", False, "prim"),
    )


@dataclass
class UseStaminaRecoveryItem(MsgpackModel):
    item_master_id: Optional[int] = None
    quantity: Optional[int] = None

    _FIELDS = (
        (0, "item_master_id", "long", False, "prim"),
        (1, "quantity", "int", False, "prim"),
    )


@dataclass
class UseStaminaRecoveryItemsPayload(MsgpackModel):
    items: Optional[List["UseStaminaRecoveryItem"]] = None

    _FIELDS = ((0, "items", "UseStaminaRecoveryItem", True, "model"),)


@dataclass
class User(MsgpackModel):
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
    ban_level: Optional[int] = None
    tutorial_status: Optional[int] = None
    monthly_payment: Optional[int] = None
    splash_last_displayed_at: Optional[str] = None
    is_caped_player_rank: Optional[bool] = None
    require_caped_player_rank_announce: Optional[bool] = None

    _FIELDS = (
        (0, "id_", "long", False, "prim"),
        (1, "player_rank", "int", False, "prim"),
        (2, "current_rank_point", "int", False, "prim"),
        (3, "current_stamina", "int", False, "prim"),
        (4, "max_stamina_restored_at", "DateTime", False, "prim"),
        (5, "paid_jewel", "int", False, "prim"),
        (6, "free_jewel", "int", False, "prim"),
        (7, "coin", "int", False, "prim"),
        (8, "player_rank_limit", "int", False, "prim"),
        (9, "stamina_recover_times_with_jewel", "int", False, "prim"),
        (10, "circle_usage_restrictions_end_time", "DateTime", False, "prim"),
        (11, "circle_id", "string", False, "prim"),
        (12, "game_start_at", "DateTime", False, "prim"),
        (13, "hash_user_id", "string", False, "prim"),
        (14, "ban_level", "BanLevels", False, "enum"),
        (15, "tutorial_status", "TutorialStatus", False, "enum"),
        (16, "monthly_payment", "int", False, "prim"),
        (17, "splash_last_displayed_at", "DateTime", False, "prim"),
        (18, "is_caped_player_rank", "bool", False, "prim"),
        (19, "require_caped_player_rank_announce", "bool", False, "prim"),
    )


@dataclass
class UserProfile(MsgpackModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    trophy_master_id1: Optional[int] = None
    trophy_master_id2: Optional[int] = None
    trophy_master_id3: Optional[int] = None
    main_m_character_id: Optional[int] = None
    main_character_level: Optional[int] = None
    character_display_awakening_status: Optional[bool] = None
    icon_frame_master_id: Optional[int] = None

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "user_name", "string", False, "prim"),
        (2, "trophy_master_id1", "long", False, "prim"),
        (3, "trophy_master_id2", "long", False, "prim"),
        (4, "trophy_master_id3", "long", False, "prim"),
        (5, "main_m_character_id", "long", False, "prim"),
        (6, "main_character_level", "int", False, "prim"),
        (7, "character_display_awakening_status", "bool", False, "prim"),
        (8, "icon_frame_master_id", "long", False, "prim"),
    )


@dataclass
class UserProfileDetail(MsgpackModel):
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

    _FIELDS = (
        (0, "user_id", "string", False, "prim"),
        (1, "user_name", "string", False, "prim"),
        (2, "trophy_master_id1", "long", False, "prim"),
        (3, "trophy_master_id2", "long", False, "prim"),
        (4, "trophy_master_id3", "long", False, "prim"),
        (5, "main_m_character_id", "long", False, "prim"),
        (6, "main_character_level", "int", False, "prim"),
        (7, "character_display_awakening_status", "bool", False, "prim"),
        (8, "icon_frame_master_id", "long", False, "prim"),
        (9, "name_color_master_id", "long", False, "prim"),
        (10, "name_base_color_master_id", "long", False, "prim"),
        (11, "nameplate_master_id", "long", False, "prim"),
        (12, "nameplate_detail_master_id", "long", False, "prim"),
    )


@dataclass
class UserResult(MsgpackModel):
    user: Optional["User"] = None

    _FIELDS = ((0, "user", "User", False, "model"),)


@dataclass
class ViewShopResult(MsgpackModel):
    converted_things: Optional[List["ConvertedThingResult"]] = None

    _FIELDS = ((0, "converted_things", "ConvertedThingResult", True, "model"),)


# --- registries used by MsgpackModel for nested decoding ---
for _n in (
    AbilityVarietyUpPayload,
    AccessoryAutoSellConvertThing,
    AccessoryFavoritePayload,
    AccountConnectPayload,
    AccountDeletionResult,
    AccountRegistResult,
    AcquirableThing,
    AcquirableThingsPayload,
    ActorPortalCharacterPayload,
    AlbumArrangingPayload,
    AlbumPageResult,
    AlbumPageSearchResult,
    AlbumPhotoPayload,
    AuditionClearParty,
    AuditionClearPartySlot,
    AuditionClearedInformationParties,
    AuditionClearedInformationResult,
    AuthenticatePayload,
    AuthenticateResult,
    BannerPayload,
    BaseScoreBlock,
    BlockListResult,
    BonusLiveResult,
    BooleanResult,
    BulkLevelUpPayload,
    BulkReceivePayload,
    CalculateLessonTimeEventPayload,
    CalculateTimeEventPayload,
    ChangeNamePayload,
    ChangePhotoAbilityPayload,
    CharacterBaseStarPointResult,
    CharacterFavoritePayload,
    CharacterLineupResult,
    CharacterPointEventInformationResult,
    CharacterPointEventRankingResult,
    CharacterRank,
    CharacterRarityProbability,
    ChatworkSendMessagePayload,
    CircleAuthorityChangePayload,
    CircleAuthorityResult,
    CircleBanner,
    CircleEventCircleMissionProgress,
    CircleEventInformationResult,
    CircleEventRanking,
    CircleInformationResult,
    CircleInviteResult,
    CircleMemberInfoParameters,
    CircleMemberInfoResult,
    CircleMemberParameters,
    CirclePayload,
    CircleProfile,
    CircleRawRanking,
    CircleResult,
    CircleSearchIdResult,
    CircleSearchResult,
    ConcertResult,
    ConcoursDetailInformationResult,
    ConcoursInfomationResult,
    ConvertedThingResult,
    CostumeFavoritePayload,
    CourseRankingResult,
    CourseResult,
    CreateCircleResult,
    CreateMultiRoomPayload,
    DebugAlbumSimpleArrangingPayload,
    DebugEditLeagueBasicPayload,
    DebugLinkageCodeResult,
    DebugModifyCharacterEnhanceInformationPayload,
    DebugModifyPosterEnhanceInformationPayload,
    DebugPrepareLeagueGroupUserPayload,
    DebugUserIdResult,
    Decimal,
    Dictionary,
    DonateSupportCompanyResult,
    DonateSupportLevelLimitDetail,
    DonateSupportLevelLimitPayload,
    EditBookmarkPayload,
    EditPartyPayload,
    EditPartySlotPayload,
    EditPositionPayload,
    EditPositionSlotPayload,
    EditTrialPartyEventStagePartyPayload,
    EditTrialPartyEventStagePartyPayloadSlot,
    EditUserProfilePayload,
    EexternalPaymentResult,
    Effect,
    EffectBranch,
    EffectTargetValue,
    EffectTrigger,
    EnvironmentResult,
    EpisodeResult,
    EventBoxGachaRollResult,
    EventResult,
    ExchangeShopThingPayload,
    FavoriteStampOrderPayload,
    FinishAnotherNotationLivePayload,
    FinishLessonPayload,
    FinishLivePayload,
    FinishLiveResult,
    FlashSaleReadStagePayload,
    FriendAcceptResult,
    FriendFavoritePayload,
    FriendInvitationMissionPayload,
    FriendInvitationUserInfoResult,
    FriendListResult,
    FriendRequestResult,
    FriendResult,
    FriendSearchResult,
    GachaHistoryResult,
    GachaInfoResult,
    GachaLineupItemProbability,
    GachaRollLimit,
    GachaRollResult,
    GachaSelectedThingsResult,
    GachaThingResult,
    GenerateLotteryResultPayload,
    GeneratePhotoPayload,
    GeneratePhotoResult,
    GeneratePhotosPayload,
    GhostLiveInfo,
    GhostLiveResult,
    HighScoreBuff,
    HighScoreBuffSetting,
    HighScoreParty,
    HighScorePartySlot,
    InboxReceiveResult,
    InviteMultiRoomPayload,
    JoinMultiRoomPayload,
    LeaguePartyAndRankingResult,
    LeaguePartySlotResult,
    LeagueReceiveResults,
    LeagueResult,
    LeagueTopMenuInformationResult,
    LessonResult,
    LevelUpPhotoPayload,
    LevelUpPhotoResult,
    LiveDropThing,
    LiveTimeEvent,
    LiveUnit,
    LiveUnitWithOrder,
    LoginBonusDetail,
    LoginBonusResult,
    LoginBonusSpineDetail,
    LoginBonusSpineGroup,
    LoginPayload,
    LoginResult,
    MainCharacter,
    MarketResult,
    MarketThing,
    MasterDataManifest,
    MatchingGhostLiveResult,
    MissionPassRewardsResult,
    MultiLiveAdditionalScoreBlock,
    MultiLiveInformation,
    MultiRoomCreateResult,
    MultiRoomDetailResult,
    MultiRoomInformationResult,
    MultiRoomInvitedResult,
    MultiRoomJoinnedResult,
    MultiRoomPartySlot,
    MultiRoomRanking,
    MusicCourseRandomSelectResult,
    MusicCourseRandomSelectResultDetail,
    MusicCourseRankingPayload,
    MyCircleInformationResult,
    NoteJudgePayload,
    NoteResult,
    NotificationContentResult,
    NotificationResult,
    PartyInfo,
    PartyPayload,
    PartySlotAccessoryPayload,
    PartySlotCharacterPayload,
    PartySlotDetail,
    PartySlotPayload,
    PartySlotPosterPayload,
    PhotoAppearedCharacter,
    PlayerRankPointResult,
    PosterAlternativeImagePayload,
    PosterFavoritePayload,
    PosterLineupResult,
    PosterRarityProbability,
    ProcessPaymentResult,
    PurchaseItemPayload,
    RateResult,
    RateUpdateResult,
    RawHighScoreRankingResult,
    RawRanking,
    RawRankingResult,
    RawRankingWithLongPoint,
    ReadNotificationPayload,
    ReceivedThing,
    RegisterAppStorePaymentPayload,
    RegisterBirthDayPayload,
    RegisterGooglePlayPaymentPayload,
    RegisterPayload,
    RegisterTakeOverPasswordPayload,
    RollResult,
    RouletteRollResult,
    ScoreWithDateResult,
    SelectMusicCourseRandomMusicPayload,
    SellAccessoryPayload,
    Sense,
    SenseCoolTime,
    SenseEffect,
    SenseScoreBlock,
    SenseTimingEvent,
    SetAlbumPublishingPayload,
    SetLessonPartyPayload,
    SetLessonPartySlotPayload,
    SetPhotoTagPayload,
    SetSelectedThingsPayload,
    SpRateUpdateResult,
    StarAct,
    StarActScoreBlock,
    StarPointResult,
    StartLessonPayload,
    StartLivePayload,
    StartMultiLivePayload,
    StartMultiRoomLivePayload,
    StartTournamentPayload,
    StartTripleCastLivePayload,
    StartTripleCastLiveResult,
    Status,
    StoryEventCampInfo,
    StoryEventMissionCircleProgress,
    StoryEventMissionCircleProgressResult,
    StoryEventPointExchangeResult,
    SupportCompanyInformation,
    SupportCompanyLevelLimitDetail,
    SupportCompanyLevelLimitPayload,
    SupportCompanyLevelLimitStatus,
    SupportCompanyLevelLimitStatusDetail,
    SupportCompanyLevelStatus,
    TakeOverAccountPayload,
    TakeOverAccountResult,
    TakeOverCodeResult,
    TimedConfirmationCode,
    TimingEvent,
    TotalPointEventInformationResult,
    TotalPointEventRankingResult,
    TournamentQualifyingInformationResult,
    TournamentResult,
    TransitionTokenResult,
    TrialPartyEventResult,
    TrialPartyEventStageResult,
    TripleCastPartyAndRankingResult,
    TripleCastPartyResult,
    TripleCastPartyScore,
    UpdateClearLampResult,
    UpdateGameHintPayload,
    UpdateHomeDisplayPreferencePayload,
    UpdateLastViewedAtPayload,
    UpdateTutorialPayload,
    UrlResult,
    UseExperienceItemsPayload,
    UseStaminaRecoveryItem,
    UseStaminaRecoveryItemsPayload,
    User,
    UserProfile,
    UserProfileDetail,
    UserResult,
    ViewShopResult,
):
    MODEL_REGISTRY[_n.__name__] = _n
for _e in (
    AccountDeletionErrorTypes,
    AccountRegisterErrorTypes,
    AchievementRateGrades,
    ActivityLogTypes,
    Attributes,
    AuthenticationProviders,
    BanLevels,
    BonusAbilityEnableFlags,
    BranchConditionTypes,
    BranchJudgeTypes,
    CampTypes,
    CharacterEpisodeOrder,
    CharacterRarities,
    CharacterSelectionTypes,
    CircleAuthorities,
    CircleAuthorityResultStatus,
    CircleAuthorityUpdateTypes,
    CircleDonateSupportCompanyResult,
    CircleResultStatus,
    ClearLamps,
    Companies,
    DugongRunClearTypes,
    EditTypes,
    EffectTypes,
    EntryTypes,
    FriendAcceptResultStatus,
    FriendRequestResultStatus,
    FriendSearchResultStatus,
    GachaCardTypes,
    GachaEmissionFlags,
    GameVersions,
    HomeBGMSelectionTypes,
    HomeCharacterDisplayTypes,
    InvitationCodeResultStatuses,
    LeagueClassChangeTypes,
    LeagueClassTypes,
    LiveDropTypes,
    LoginBonusLayoutTypes,
    LoginBonusSpineSelectType,
    LoginBonusTypes,
    LoginPassNotificationTypes,
    MatchingResult,
    MissionCategories,
    MissionPassRewardStatus,
    MultiRoomPlayModes,
    MusicBookmarkFlags,
    MusicCourseGaugeType,
    MusicDifficulties,
    NotificationCategory,
    NotificationTabCategory,
    PageCategories,
    PhotoRarities,
    PlayTimeTypes,
    PossessionRarities,
    PossessionRarityFlag,
    PosterEpisodeTypes,
    ProcessPaymentTransactionResult,
    SearchCircleMemberConditionTypes,
    SenseFirePriority,
    SenseLightTypes,
    SenseTypes,
    StarPassTypes,
    StoryTypes,
    ThingTypes,
    TimingTypes,
    TriggerTypes,
    TripleCastGroupOrder,
    TutorialStatus,
    ViewedShopCategoryTypes,
):
    ENUM_REGISTRY[_e.__name__] = _e
