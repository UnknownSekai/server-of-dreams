from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field

from models import enums as _enums

from .AccessoryEffectFilterMaster import AccessoryEffectFilterMaster
from .AccessoryEffectMaster import AccessoryEffectMaster
from .AccessoryLevelPatternGroupMaster import AccessoryLevelPatternGroupMaster
from .AccessoryLevelPatternItemMaster import AccessoryLevelPatternItemMaster
from .AccessoryLevelPatternMaster import AccessoryLevelPatternMaster
from .AccessoryMaster import AccessoryMaster
from .AchivementRateRewardMaster import AchivementRateRewardMaster
from .ActivityLogMessageTemplateMaster import ActivityLogMessageTemplateMaster
from .AdditionalRewardPackageMaster import AdditionalRewardPackageMaster
from .AdditionalRewardThingMaster import AdditionalRewardThingMaster
from .AlbumEffectMaster import AlbumEffectMaster
from .AlbumThemeMaster import AlbumThemeMaster
from .AnotherNotationMaster import AnotherNotationMaster
from .AuditionMaster import AuditionMaster
from .AuditionPhaseMaster import AuditionPhaseMaster
from .AuditionRewardPackageMaster import AuditionRewardPackageMaster
from .AuditionRewardThing import AuditionRewardThing
from .BannerMaster import BannerMaster
from .BodyMotionMaster import BodyMotionMaster
from .BombMaster import BombMaster
from .BonusLiveMaster import BonusLiveMaster
from .BonusLiveStageMaster import BonusLiveStageMaster
from .BonusLiveStageRewardThingMaster import BonusLiveStageRewardThingMaster
from .BranchMaster import BranchMaster
from .BuffItemMaster import BuffItemMaster
from .CampaignMaster import CampaignMaster
from .CategoryGroupMaster import CategoryGroupMaster
from .CategoryMaster import CategoryMaster
from .ChangeBodyMotionMaster import ChangeBodyMotionMaster
from .CharacterAwakeningItemGroupMaster import CharacterAwakeningItemGroupMaster
from .CharacterAwakeningItemMaster import CharacterAwakeningItemMaster
from .CharacterBaseBloomGenericItemMaster import CharacterBaseBloomGenericItemMaster
from .CharacterBaseMaster import CharacterBaseMaster
from .CharacterBloomBonusGroupMaster import CharacterBloomBonusGroupMaster
from .CharacterBloomBonusMaster import CharacterBloomBonusMaster
from .CharacterBloomDetailMaster import CharacterBloomDetailMaster
from .CharacterBloomItemMaster import CharacterBloomItemMaster
from .CharacterBloomRewardMaster import CharacterBloomRewardMaster
from .CharacterCategoryMaster import CharacterCategoryMaster
from .CharacterEpisodeMaster import CharacterEpisodeMaster
from .CharacterEpisodeRelationMaster import CharacterEpisodeRelationMaster
from .CharacterEpisodeReleaseItemGroupMaster import (
    CharacterEpisodeReleaseItemGroupMaster,
)
from .CharacterEpisodeReleaseItemMaster import CharacterEpisodeReleaseItemMaster
from .CharacterExperienceItemMaster import CharacterExperienceItemMaster
from .CharacterKeyMissionMaster import CharacterKeyMissionMaster
from .CharacterLessonScoreRewardMaster import CharacterLessonScoreRewardMaster
from .CharacterLevelMaster import CharacterLevelMaster
from .CharacterMaster import CharacterMaster
from .CharacterMissionCategoryLevelMaster import CharacterMissionCategoryLevelMaster
from .CharacterMissionItemMaster import CharacterMissionItemMaster
from .CharacterMissionMaster import CharacterMissionMaster
from .CharacterMissionStageMaster import CharacterMissionStageMaster
from .CharacterPieceMaster import CharacterPieceMaster
from .CharacterPointEventCharacterRankingRewardItemMaster import (
    CharacterPointEventCharacterRankingRewardItemMaster,
)
from .CharacterPointEventCharacterRankingRewardItemPackageMaster import (
    CharacterPointEventCharacterRankingRewardItemPackageMaster,
)
from .CharacterPointEventCharacterRankingRewardMaster import (
    CharacterPointEventCharacterRankingRewardMaster,
)
from .CharacterPointEventMaster import CharacterPointEventMaster
from .CharacterProfileRestrictionMaster import CharacterProfileRestrictionMaster
from .CharacterSenseEnhanceItemGroupMaster import CharacterSenseEnhanceItemGroupMaster
from .CharacterSenseEnhanceItemMaster import CharacterSenseEnhanceItemMaster
from .CharacterStarRankMaster import CharacterStarRankMaster
from .CharacterStarRankRewardGroupMaster import CharacterStarRankRewardGroupMaster
from .CharacterStarRankRewardMaster import CharacterStarRankRewardMaster
from .CircleEventCirclePointRewardMaster import CircleEventCirclePointRewardMaster
from .CircleEventCircleRankingRewardItem import CircleEventCircleRankingRewardItem
from .CircleEventCircleRankingRewardItemPackageMaster import (
    CircleEventCircleRankingRewardItemPackageMaster,
)
from .CircleEventCircleRankingRewardMaster import CircleEventCircleRankingRewardMaster
from .CircleEventMaster import CircleEventMaster
from .CircleEventMissionMaster import CircleEventMissionMaster
from .CircleEventMissionRefreshSetting import CircleEventMissionRefreshSetting
from .CircleEventMissionRefreshSettingGroupMaster import (
    CircleEventMissionRefreshSettingGroupMaster,
)
from .CircleSupportCompanyLevelDetailMaster import CircleSupportCompanyLevelDetailMaster
from .CircleSupportCompanyLevelLimitDetailMaster import (
    CircleSupportCompanyLevelLimitDetailMaster,
)
from .CircleSupportCompanyLevelLimitMaster import CircleSupportCompanyLevelLimitMaster
from .CircleTheaterLevelMaster import CircleTheaterLevelMaster
from .ComebackCampaignMaster import ComebackCampaignMaster
from .ComicEpisodeMaster import ComicEpisodeMaster
from .ComicMaster import ComicMaster
from .CompanyMaster import CompanyMaster
from .ConcertMaster import ConcertMaster
from .ConcertRewardMaster import ConcertRewardMaster
from .ConcertStageMaster import ConcertStageMaster
from .ConcoursDetailMaster import ConcoursDetailMaster
from .ConcoursMaster import ConcoursMaster
from .ConcoursPointMaster import ConcoursPointMaster
from .ConcoursPointRewardMaster import ConcoursPointRewardMaster
from .ConcoursPointRewardThingMaster import ConcoursPointRewardThingMaster
from .CostumeGroupMaster import CostumeGroupMaster
from .CostumeMaster import CostumeMaster
from .CostumeWearableCharacterGroupMaster import CostumeWearableCharacterGroupMaster
from .CourseRankingRewardMaster import CourseRankingRewardMaster
from .CourseRankingRewardThingMaster import CourseRankingRewardThingMaster
from .DecorationMaster import DecorationMaster
from .DugongRunCourseMaster import DugongRunCourseMaster
from .DugongRunRewardMaster import DugongRunRewardMaster
from .EffectConditionMaster import EffectConditionMaster
from .EffectDetailMaster import EffectDetailMaster
from .EffectDurationGroupMaster import EffectDurationGroupMaster
from .EffectDurationMaster import EffectDurationMaster
from .EffectMaster import EffectMaster
from .EffectOrderMaster import EffectOrderMaster
from .EffectTriggerCharacterBaseGroupMaster import EffectTriggerCharacterBaseGroupMaster
from .EffectTriggerMaster import EffectTriggerMaster
from .EpisodeMaster import EpisodeMaster
from .EpisodeReleaseCondition import EpisodeReleaseCondition
from .EpisodeRewardPackageMaster import EpisodeRewardPackageMaster
from .EpisodeRewardThing import EpisodeRewardThing
from .EventBonusMaster import EventBonusMaster
from .EventBoxGachaBoxMaster import EventBoxGachaBoxMaster
from .EventBoxGachaBoxThingMaster import EventBoxGachaBoxThingMaster
from .EventBoxGachaDetailMaster import EventBoxGachaDetailMaster
from .EventBoxGachaMaster import EventBoxGachaMaster
from .EventBoxGachaTextTemplateMaster import EventBoxGachaTextTemplateMaster
from .EventCampClassMaster import EventCampClassMaster
from .EventCampMaster import EventCampMaster
from .EventCampSupportPointRewardMaster import EventCampSupportPointRewardMaster
from .EventMaster import EventMaster
from .EventPointRewardMaster import EventPointRewardMaster
from .EventRankingRewardMaster import EventRankingRewardMaster
from .EventRankingRewardThingMaster import EventRankingRewardThingMaster
from .ExchangeShopMaster import ExchangeShopMaster
from .ExchangeShopThing import ExchangeShopThing
from .FacialExpressionMaster import FacialExpressionMaster
from .FilmItemMaster import FilmItemMaster
from .FriendInvitationMissionMaster import FriendInvitationMissionMaster
from .FriendInvitationMissionRewardMaster import FriendInvitationMissionRewardMaster
from .FriendInvitationMissionStageMaster import FriendInvitationMissionStageMaster
from .GachaBonusThing import GachaBonusThing
from .GachaDetailBonusThing import GachaDetailBonusThing
from .GachaDetailMaster import GachaDetailMaster
from .GachaMaster import GachaMaster
from .GachaRollBonus import GachaRollBonus
from .GachaTextTemplateMaster import GachaTextTemplateMaster
from .GachaThing import GachaThing
from .GameHintMaster import GameHintMaster
from .GhostLiveMaster import GhostLiveMaster
from .GradualMissionGroupMaster import GradualMissionGroupMaster
from .GradualMissionMaster import GradualMissionMaster
from .HeadDirectionMaster import HeadDirectionMaster
from .HeadMotionMaster import HeadMotionMaster
from .HomeBGMDetailMaster import HomeBGMDetailMaster
from .HomeBGMMaster import HomeBGMMaster
from .HomeBackgroundMaster import HomeBackgroundMaster
from .HomeCharacterMaster import HomeCharacterMaster
from .HomeCharacterVoiceMaster import HomeCharacterVoiceMaster
from .HomeCharacterVoicePeriodMaster import HomeCharacterVoicePeriodMaster
from .HomePosterMaster import HomePosterMaster
from .HomeSkinMaster import HomeSkinMaster
from .IconFrameMaster import IconFrameMaster
from .ItemMaster import ItemMaster
from .JewelShopCategoryMaster import JewelShopCategoryMaster
from .JewelShopItemMaster import JewelShopItemMaster
from .JewelShopThing import JewelShopThing
from .LeaderSenseDetailConditionMaster import LeaderSenseDetailConditionMaster
from .LeaderSenseDetailMaster import LeaderSenseDetailMaster
from .LeaderSenseMaster import LeaderSenseMaster
from .LeagueAllClassGlobalRankingRewardPackageMaster import (
    LeagueAllClassGlobalRankingRewardPackageMaster,
)
from .LeagueAllClassGlobalRankingRewardThingMaster import (
    LeagueAllClassGlobalRankingRewardThingMaster,
)
from .LeagueClassGroupMaster import LeagueClassGroupMaster
from .LeagueClassMaster import LeagueClassMaster
from .LeagueGroupRankingRewardPackageMaster import LeagueGroupRankingRewardPackageMaster
from .LeagueGroupRankingRewardThingMaster import LeagueGroupRankingRewardThingMaster
from .LeagueMaster import LeagueMaster
from .LeaguePlayRewardPackageMaster import LeaguePlayRewardPackageMaster
from .LeaguePlayRewardThingMaster import LeaguePlayRewardThingMaster
from .LeagueRewardPackageMaster import LeagueRewardPackageMaster
from .LeagueRewardThingMaster import LeagueRewardThingMaster
from .LessonScoreRewardGroupMaster import LessonScoreRewardGroupMaster
from .LessonScoreRewardMaster import LessonScoreRewardMaster
from .LightLoadSplitEffectMaster import LightLoadSplitEffectMaster
from .LipSyncMaster import LipSyncMaster
from .LiveDropFrameGroupMaster import LiveDropFrameGroupMaster
from .LiveDropFrameMaster import LiveDropFrameMaster
from .LiveDropThingMaster import LiveDropThingMaster
from .LiveMaster import LiveMaster
from .LiveSettingMaster import LiveSettingMaster
from .LoginBonusSpineCostumeMaster import LoginBonusSpineCostumeMaster
from .LoopMotionMaster import LoopMotionMaster
from .MarketFrameThingMaster import MarketFrameThingMaster
from .MissionMaster import MissionMaster
from .MissionPassDetailMaster import MissionPassDetailMaster
from .MissionPassLoopRewardMaster import MissionPassLoopRewardMaster
from .MissionPassLoopRewardThingMaster import MissionPassLoopRewardThingMaster
from .MissionPassMaster import MissionPassMaster
from .MissionPassRewardThing import MissionPassRewardThing
from .MissionRewardMaster import MissionRewardMaster
from .MissionStageMaster import MissionStageMaster
from .MultiLiveScheduleMaster import MultiLiveScheduleMaster
from .MusicCourseDetailMaster import MusicCourseDetailMaster
from .MusicCourseMaster import MusicCourseMaster
from .MusicCourseRewardGroupMaster import MusicCourseRewardGroupMaster
from .MusicCourseRewardThing import MusicCourseRewardThing
from .MusicGroupDetailMaster import MusicGroupDetailMaster
from .MusicGroupMaster import MusicGroupMaster
from .MusicMaster import MusicMaster
from .MusicVideoDefaultCostumeGroupMaster import MusicVideoDefaultCostumeGroupMaster
from .MusicVideoDefaultCostumeMaster import MusicVideoDefaultCostumeMaster
from .MusicVideoMaster import MusicVideoMaster
from .MusicVideoOriginalCharacterMaster import MusicVideoOriginalCharacterMaster
from .MusicVocalVersionMaster import MusicVocalVersionMaster
from .NameBaseColorMaster import NameBaseColorMaster
from .NameColorMaster import NameColorMaster
from .NameplateDetailMaster import NameplateDetailMaster
from .NameplateMaster import NameplateMaster
from .NgWordMaster import NgWordMaster
from .NoteMaster import NoteMaster
from .PermanentMarketThingMaster import PermanentMarketThingMaster
from .PhotoEffectChangeItemMaster import PhotoEffectChangeItemMaster
from .PhotoEffectMaster import PhotoEffectMaster
from .PhotoEffectTypeGroupMaster import PhotoEffectTypeGroupMaster
from .PhotoEffectVarietyChangeDetailMaster import PhotoEffectVarietyChangeDetailMaster
from .PhotoEffectVarietyUpDetailMaster import PhotoEffectVarietyUpDetailMaster
from .PhotoLevelUpItemGroupMaster import PhotoLevelUpItemGroupMaster
from .PhotoLevelUpItemMaster import PhotoLevelUpItemMaster
from .PhotoSpotMaster import PhotoSpotMaster
from .PickupCharacterMissionDetailGroupMaster import (
    PickupCharacterMissionDetailGroupMaster,
)
from .PickupCharacterMissionDetailMaster import PickupCharacterMissionDetailMaster
from .PickupCharacterMissionDetailRewardMaster import (
    PickupCharacterMissionDetailRewardMaster,
)
from .PickupCharacterMissionMaster import PickupCharacterMissionMaster
from .PickupSelectionGachaMaster import PickupSelectionGachaMaster
from .PlayerRankCapDetailMaster import PlayerRankCapDetailMaster
from .PlayerRankCapMaster import PlayerRankCapMaster
from .PlayerRankMaster import PlayerRankMaster
from .PosterAbilityMaster import PosterAbilityMaster
from .PosterCostumeMaster import PosterCostumeMaster
from .PosterLevelPatternGroupMaster import PosterLevelPatternGroupMaster
from .PosterLevelPatternMaster import PosterLevelPatternMaster
from .PosterMaster import PosterMaster
from .PosterReleaseItemGroupMaster import PosterReleaseItemGroupMaster
from .PosterReleaseItemMaster import PosterReleaseItemMaster
from .PosterStoryMaster import PosterStoryMaster
from .RandomEffectGroupMaster import RandomEffectGroupMaster
from .ResultVoiceMaster import ResultVoiceMaster
from .RewardRuleMaster import RewardRuleMaster
from .RouletteEventMaster import RouletteEventMaster
from .RouletteMaster import RouletteMaster
from .RoulettePrizeMaster import RoulettePrizeMaster
from .RoulettePrizeThingMaster import RoulettePrizeThingMaster
from .RouletteRollRewardMaster import RouletteRollRewardMaster
from .RouletteRollRewardThing import RouletteRollRewardThing
from .SceneCameraMaster import SceneCameraMaster
from .SenseBranchMaster import SenseBranchMaster
from .SenseEffectMaster import SenseEffectMaster
from .SenseMaster import SenseMaster
from .SenseNotationBuffMaster import SenseNotationBuffMaster
from .SenseNotationDetailMaster import SenseNotationDetailMaster
from .SenseNotationMaster import SenseNotationMaster
from .SensePerformanceCharacterMaster import SensePerformanceCharacterMaster
from .SensePerformanceMaster import SensePerformanceMaster
from .SignMaster import SignMaster
from .SpecialEpisodeMaster import SpecialEpisodeMaster
from .SpecialEventLayout import SpecialEventLayout
from .SpecialEventMaster import SpecialEventMaster
from .SpecialStoryMaster import SpecialStoryMaster
from .SplashMaster import SplashMaster
from .SpotConversationMaster import SpotConversationMaster
from .StaminaRecoveryItemMaster import StaminaRecoveryItemMaster
from .StampMaster import StampMaster
from .StarActBranchMaster import StarActBranchMaster
from .StarActConditionMaster import StarActConditionMaster
from .StarActMaster import StarActMaster
from .StarRankRewardMaster import StarRankRewardMaster
from .Status import Status
from .StepupGachaGroupMaster import StepupGachaGroupMaster
from .StepupGachaMaster import StepupGachaMaster
from .StoryEventBonusCharacterBaseMaster import StoryEventBonusCharacterBaseMaster
from .StoryEventCircleHighScoreRewardMaster import StoryEventCircleHighScoreRewardMaster
from .StoryEventCircleMaster import StoryEventCircleMaster
from .StoryEventCircleMissionMaster import StoryEventCircleMissionMaster
from .StoryEventCircleMissionRewardMaster import StoryEventCircleMissionRewardMaster
from .StoryEventEpisodeMaster import StoryEventEpisodeMaster
from .StoryEventHighScoreBuffMaster import StoryEventHighScoreBuffMaster
from .StoryEventHighScoreBuffPatternGroupMaster import (
    StoryEventHighScoreBuffPatternGroupMaster,
)
from .StoryEventHighScoreBuffPatternMaster import StoryEventHighScoreBuffPatternMaster
from .StoryEventHighScoreBuffSettingMaster import StoryEventHighScoreBuffSettingMaster
from .StoryEventHighScoreMaster import StoryEventHighScoreMaster
from .StoryEventHighScoreRewardMaster import StoryEventHighScoreRewardMaster
from .StoryEventMaster import StoryEventMaster
from .StoryEventRewardItemPackage import StoryEventRewardItemPackage
from .StoryEventRewardMaster import StoryEventRewardMaster
from .StoryEventRewardThing import StoryEventRewardThing
from .StoryEventStoryBgmGroupMaster import StoryEventStoryBgmGroupMaster
from .StoryEventStoryBgmSchedule import StoryEventStoryBgmSchedule
from .StoryEventStoryMaster import StoryEventStoryMaster
from .StoryEventTotalPointRewardMaster import StoryEventTotalPointRewardMaster
from .StoryMaster import StoryMaster
from .StoryRelationMaster import StoryRelationMaster
from .TeamChallengeMaster import TeamChallengeMaster
from .TheaterChapterMaster import TheaterChapterMaster
from .TheaterDetailMaster import TheaterDetailMaster
from .TheaterRoleMaster import TheaterRoleMaster
from .TheaterStoryMaster import TheaterStoryMaster
from .TimeLimitedControlMaster import TimeLimitedControlMaster
from .TipMaster import TipMaster
from .TitleBackgroundDetailMaster import TitleBackgroundDetailMaster
from .TitleBackgroundMaster import TitleBackgroundMaster
from .TitleCallVoiceMaster import TitleCallVoiceMaster
from .TitleDecorationMaster import TitleDecorationMaster
from .TotalPointEventMaster import TotalPointEventMaster
from .TotalPointEventRewardMaster import TotalPointEventRewardMaster
from .TournamentDetailMaster import TournamentDetailMaster
from .TournamentMaster import TournamentMaster
from .TournamentQualifyingMaster import TournamentQualifyingMaster
from .TrialPartyAccessoryMaster import TrialPartyAccessoryMaster
from .TrialPartyCharacterMaster import TrialPartyCharacterMaster
from .TrialPartyEventMaster import TrialPartyEventMaster
from .TrialPartyEventStageMaster import TrialPartyEventStageMaster
from .TrialPartyEventStageRewardMaster import TrialPartyEventStageRewardMaster
from .TrialPartyMaster import TrialPartyMaster
from .TrialPartyPosterMaster import TrialPartyPosterMaster
from .TrialPartySlotMaster import TrialPartySlotMaster
from .TripleCastAllClassGlobalRankingRewardPackageMaster import (
    TripleCastAllClassGlobalRankingRewardPackageMaster,
)
from .TripleCastAllClassGlobalRankingRewardThingMaster import (
    TripleCastAllClassGlobalRankingRewardThingMaster,
)
from .TripleCastGroupRankingRewardPackageMaster import (
    TripleCastGroupRankingRewardPackageMaster,
)
from .TripleCastGroupRankingRewardThingMaster import (
    TripleCastGroupRankingRewardThingMaster,
)
from .TripleCastMaster import TripleCastMaster
from .TrophyGroupMaster import TrophyGroupMaster
from .TrophyMaster import TrophyMaster
from .UnlockConditionMaster import UnlockConditionMaster

_TYPES = [
    AccessoryEffectFilterMaster,
    AccessoryEffectMaster,
    AccessoryLevelPatternGroupMaster,
    AccessoryLevelPatternItemMaster,
    AccessoryLevelPatternMaster,
    AccessoryMaster,
    AchivementRateRewardMaster,
    ActivityLogMessageTemplateMaster,
    AdditionalRewardPackageMaster,
    AdditionalRewardThingMaster,
    AlbumEffectMaster,
    AlbumThemeMaster,
    AnotherNotationMaster,
    AuditionMaster,
    AuditionPhaseMaster,
    AuditionRewardPackageMaster,
    AuditionRewardThing,
    BannerMaster,
    BodyMotionMaster,
    BombMaster,
    BonusLiveMaster,
    BonusLiveStageMaster,
    BonusLiveStageRewardThingMaster,
    BranchMaster,
    BuffItemMaster,
    CampaignMaster,
    CategoryGroupMaster,
    CategoryMaster,
    ChangeBodyMotionMaster,
    CharacterAwakeningItemGroupMaster,
    CharacterAwakeningItemMaster,
    CharacterBaseBloomGenericItemMaster,
    CharacterBaseMaster,
    CharacterBloomBonusGroupMaster,
    CharacterBloomBonusMaster,
    CharacterBloomDetailMaster,
    CharacterBloomItemMaster,
    CharacterBloomRewardMaster,
    CharacterCategoryMaster,
    CharacterEpisodeMaster,
    CharacterEpisodeRelationMaster,
    CharacterEpisodeReleaseItemGroupMaster,
    CharacterEpisodeReleaseItemMaster,
    CharacterExperienceItemMaster,
    CharacterKeyMissionMaster,
    CharacterLessonScoreRewardMaster,
    CharacterLevelMaster,
    CharacterMaster,
    CharacterMissionCategoryLevelMaster,
    CharacterMissionItemMaster,
    CharacterMissionMaster,
    CharacterMissionStageMaster,
    CharacterPieceMaster,
    CharacterPointEventCharacterRankingRewardItemMaster,
    CharacterPointEventCharacterRankingRewardItemPackageMaster,
    CharacterPointEventCharacterRankingRewardMaster,
    CharacterPointEventMaster,
    CharacterProfileRestrictionMaster,
    CharacterSenseEnhanceItemGroupMaster,
    CharacterSenseEnhanceItemMaster,
    CharacterStarRankMaster,
    CharacterStarRankRewardGroupMaster,
    CharacterStarRankRewardMaster,
    CircleEventCirclePointRewardMaster,
    CircleEventCircleRankingRewardItem,
    CircleEventCircleRankingRewardItemPackageMaster,
    CircleEventCircleRankingRewardMaster,
    CircleEventMaster,
    CircleEventMissionMaster,
    CircleEventMissionRefreshSetting,
    CircleEventMissionRefreshSettingGroupMaster,
    CircleSupportCompanyLevelDetailMaster,
    CircleSupportCompanyLevelLimitDetailMaster,
    CircleSupportCompanyLevelLimitMaster,
    CircleTheaterLevelMaster,
    ComebackCampaignMaster,
    ComicEpisodeMaster,
    ComicMaster,
    CompanyMaster,
    ConcertMaster,
    ConcertRewardMaster,
    ConcertStageMaster,
    ConcoursDetailMaster,
    ConcoursMaster,
    ConcoursPointMaster,
    ConcoursPointRewardMaster,
    ConcoursPointRewardThingMaster,
    CostumeGroupMaster,
    CostumeMaster,
    CostumeWearableCharacterGroupMaster,
    CourseRankingRewardMaster,
    CourseRankingRewardThingMaster,
    DecorationMaster,
    DugongRunCourseMaster,
    DugongRunRewardMaster,
    EffectConditionMaster,
    EffectDetailMaster,
    EffectDurationGroupMaster,
    EffectDurationMaster,
    EffectMaster,
    EffectOrderMaster,
    EffectTriggerCharacterBaseGroupMaster,
    EffectTriggerMaster,
    EpisodeMaster,
    EpisodeReleaseCondition,
    EpisodeRewardPackageMaster,
    EpisodeRewardThing,
    EventBonusMaster,
    EventBoxGachaBoxMaster,
    EventBoxGachaBoxThingMaster,
    EventBoxGachaDetailMaster,
    EventBoxGachaMaster,
    EventBoxGachaTextTemplateMaster,
    EventCampClassMaster,
    EventCampMaster,
    EventCampSupportPointRewardMaster,
    EventMaster,
    EventPointRewardMaster,
    EventRankingRewardMaster,
    EventRankingRewardThingMaster,
    ExchangeShopMaster,
    ExchangeShopThing,
    FacialExpressionMaster,
    FilmItemMaster,
    FriendInvitationMissionMaster,
    FriendInvitationMissionRewardMaster,
    FriendInvitationMissionStageMaster,
    GachaBonusThing,
    GachaDetailBonusThing,
    GachaDetailMaster,
    GachaMaster,
    GachaRollBonus,
    GachaTextTemplateMaster,
    GachaThing,
    GameHintMaster,
    GhostLiveMaster,
    GradualMissionGroupMaster,
    GradualMissionMaster,
    HeadDirectionMaster,
    HeadMotionMaster,
    HomeBGMDetailMaster,
    HomeBGMMaster,
    HomeBackgroundMaster,
    HomeCharacterMaster,
    HomeCharacterVoiceMaster,
    HomeCharacterVoicePeriodMaster,
    HomePosterMaster,
    HomeSkinMaster,
    IconFrameMaster,
    ItemMaster,
    JewelShopCategoryMaster,
    JewelShopItemMaster,
    JewelShopThing,
    LeaderSenseDetailConditionMaster,
    LeaderSenseDetailMaster,
    LeaderSenseMaster,
    LeagueAllClassGlobalRankingRewardPackageMaster,
    LeagueAllClassGlobalRankingRewardThingMaster,
    LeagueClassGroupMaster,
    LeagueClassMaster,
    LeagueGroupRankingRewardPackageMaster,
    LeagueGroupRankingRewardThingMaster,
    LeagueMaster,
    LeaguePlayRewardPackageMaster,
    LeaguePlayRewardThingMaster,
    LeagueRewardPackageMaster,
    LeagueRewardThingMaster,
    LessonScoreRewardGroupMaster,
    LessonScoreRewardMaster,
    LightLoadSplitEffectMaster,
    LipSyncMaster,
    LiveDropFrameGroupMaster,
    LiveDropFrameMaster,
    LiveDropThingMaster,
    LiveMaster,
    LiveSettingMaster,
    LoginBonusSpineCostumeMaster,
    LoopMotionMaster,
    MarketFrameThingMaster,
    MissionMaster,
    MissionPassDetailMaster,
    MissionPassLoopRewardMaster,
    MissionPassLoopRewardThingMaster,
    MissionPassMaster,
    MissionPassRewardThing,
    MissionRewardMaster,
    MissionStageMaster,
    MultiLiveScheduleMaster,
    MusicCourseDetailMaster,
    MusicCourseMaster,
    MusicCourseRewardGroupMaster,
    MusicCourseRewardThing,
    MusicGroupDetailMaster,
    MusicGroupMaster,
    MusicMaster,
    MusicVideoDefaultCostumeGroupMaster,
    MusicVideoDefaultCostumeMaster,
    MusicVideoMaster,
    MusicVideoOriginalCharacterMaster,
    MusicVocalVersionMaster,
    NameBaseColorMaster,
    NameColorMaster,
    NameplateDetailMaster,
    NameplateMaster,
    NgWordMaster,
    NoteMaster,
    PermanentMarketThingMaster,
    PhotoEffectChangeItemMaster,
    PhotoEffectMaster,
    PhotoEffectTypeGroupMaster,
    PhotoEffectVarietyChangeDetailMaster,
    PhotoEffectVarietyUpDetailMaster,
    PhotoLevelUpItemGroupMaster,
    PhotoLevelUpItemMaster,
    PhotoSpotMaster,
    PickupCharacterMissionDetailGroupMaster,
    PickupCharacterMissionDetailMaster,
    PickupCharacterMissionDetailRewardMaster,
    PickupCharacterMissionMaster,
    PickupSelectionGachaMaster,
    PlayerRankCapDetailMaster,
    PlayerRankCapMaster,
    PlayerRankMaster,
    PosterAbilityMaster,
    PosterCostumeMaster,
    PosterLevelPatternGroupMaster,
    PosterLevelPatternMaster,
    PosterMaster,
    PosterReleaseItemGroupMaster,
    PosterReleaseItemMaster,
    PosterStoryMaster,
    RandomEffectGroupMaster,
    ResultVoiceMaster,
    RewardRuleMaster,
    RouletteEventMaster,
    RouletteMaster,
    RoulettePrizeMaster,
    RoulettePrizeThingMaster,
    RouletteRollRewardMaster,
    RouletteRollRewardThing,
    SceneCameraMaster,
    SenseBranchMaster,
    SenseEffectMaster,
    SenseMaster,
    SenseNotationBuffMaster,
    SenseNotationDetailMaster,
    SenseNotationMaster,
    SensePerformanceCharacterMaster,
    SensePerformanceMaster,
    SignMaster,
    SpecialEpisodeMaster,
    SpecialEventLayout,
    SpecialEventMaster,
    SpecialStoryMaster,
    SplashMaster,
    SpotConversationMaster,
    StaminaRecoveryItemMaster,
    StampMaster,
    StarActBranchMaster,
    StarActConditionMaster,
    StarActMaster,
    StarRankRewardMaster,
    Status,
    StepupGachaGroupMaster,
    StepupGachaMaster,
    StoryEventBonusCharacterBaseMaster,
    StoryEventCircleHighScoreRewardMaster,
    StoryEventCircleMaster,
    StoryEventCircleMissionMaster,
    StoryEventCircleMissionRewardMaster,
    StoryEventEpisodeMaster,
    StoryEventHighScoreBuffMaster,
    StoryEventHighScoreBuffPatternGroupMaster,
    StoryEventHighScoreBuffPatternMaster,
    StoryEventHighScoreBuffSettingMaster,
    StoryEventHighScoreMaster,
    StoryEventHighScoreRewardMaster,
    StoryEventMaster,
    StoryEventRewardItemPackage,
    StoryEventRewardMaster,
    StoryEventRewardThing,
    StoryEventStoryBgmGroupMaster,
    StoryEventStoryBgmSchedule,
    StoryEventStoryMaster,
    StoryEventTotalPointRewardMaster,
    StoryMaster,
    StoryRelationMaster,
    TeamChallengeMaster,
    TheaterChapterMaster,
    TheaterDetailMaster,
    TheaterRoleMaster,
    TheaterStoryMaster,
    TimeLimitedControlMaster,
    TipMaster,
    TitleBackgroundDetailMaster,
    TitleBackgroundMaster,
    TitleCallVoiceMaster,
    TitleDecorationMaster,
    TotalPointEventMaster,
    TotalPointEventRewardMaster,
    TournamentDetailMaster,
    TournamentMaster,
    TournamentQualifyingMaster,
    TrialPartyAccessoryMaster,
    TrialPartyCharacterMaster,
    TrialPartyEventMaster,
    TrialPartyEventStageMaster,
    TrialPartyEventStageRewardMaster,
    TrialPartyMaster,
    TrialPartyPosterMaster,
    TrialPartySlotMaster,
    TripleCastAllClassGlobalRankingRewardPackageMaster,
    TripleCastAllClassGlobalRankingRewardThingMaster,
    TripleCastGroupRankingRewardPackageMaster,
    TripleCastGroupRankingRewardThingMaster,
    TripleCastMaster,
    TrophyGroupMaster,
    TrophyMaster,
    UnlockConditionMaster,
]
_ns = {_t.__name__: _t for _t in _TYPES}
_ns.update({_k: _v for _k, _v in vars(_enums).items() if isinstance(_v, type)})
for _t in _TYPES:
    _t.model_rebuild(_types_namespace=_ns)


class MasterData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    accessory_effect_filter_master: List[AccessoryEffectFilterMaster] = Field(
        default_factory=list, alias="AccessoryEffectFilterMaster"
    )
    accessory_effect_master: List[AccessoryEffectMaster] = Field(
        default_factory=list, alias="AccessoryEffectMaster"
    )
    accessory_level_pattern_group_master: List[AccessoryLevelPatternGroupMaster] = (
        Field(default_factory=list, alias="AccessoryLevelPatternGroupMaster")
    )
    accessory_master: List[AccessoryMaster] = Field(
        default_factory=list, alias="AccessoryMaster"
    )
    activity_log_message_template_master: List[ActivityLogMessageTemplateMaster] = (
        Field(default_factory=list, alias="ActivityLogMessageTemplateMaster")
    )
    additional_reward_package_master: List[AdditionalRewardPackageMaster] = Field(
        default_factory=list, alias="AdditionalRewardPackageMaster"
    )
    album_effect_master: List[AlbumEffectMaster] = Field(
        default_factory=list, alias="AlbumEffectMaster"
    )
    album_theme_master: List[AlbumThemeMaster] = Field(
        default_factory=list, alias="AlbumThemeMaster"
    )
    another_notation_master: List[AnotherNotationMaster] = Field(
        default_factory=list, alias="AnotherNotationMaster"
    )
    audition_master: List[AuditionMaster] = Field(
        default_factory=list, alias="AuditionMaster"
    )
    audition_phase_master: List[AuditionPhaseMaster] = Field(
        default_factory=list, alias="AuditionPhaseMaster"
    )
    audition_reward_package_master: List[AuditionRewardPackageMaster] = Field(
        default_factory=list, alias="AuditionRewardPackageMaster"
    )
    banner_master: List[BannerMaster] = Field(
        default_factory=list, alias="BannerMaster"
    )
    body_motion_master: List[BodyMotionMaster] = Field(
        default_factory=list, alias="BodyMotionMaster"
    )
    bomb_master: List[BombMaster] = Field(default_factory=list, alias="BombMaster")
    bonus_live_master: List[BonusLiveMaster] = Field(
        default_factory=list, alias="BonusLiveMaster"
    )
    bonus_live_stage_master: List[BonusLiveStageMaster] = Field(
        default_factory=list, alias="BonusLiveStageMaster"
    )
    buff_item_master: List[BuffItemMaster] = Field(
        default_factory=list, alias="BuffItemMaster"
    )
    campaign_master: List[CampaignMaster] = Field(
        default_factory=list, alias="CampaignMaster"
    )
    category_group_master: List[CategoryGroupMaster] = Field(
        default_factory=list, alias="CategoryGroupMaster"
    )
    category_master: List[CategoryMaster] = Field(
        default_factory=list, alias="CategoryMaster"
    )
    change_body_motion_master: List[ChangeBodyMotionMaster] = Field(
        default_factory=list, alias="ChangeBodyMotionMaster"
    )
    character_awakening_item_group_master: List[CharacterAwakeningItemGroupMaster] = (
        Field(default_factory=list, alias="CharacterAwakeningItemGroupMaster")
    )
    character_awakening_item_master: List[CharacterAwakeningItemMaster] = Field(
        default_factory=list, alias="CharacterAwakeningItemMaster"
    )
    character_base_bloom_generic_item_master: List[
        CharacterBaseBloomGenericItemMaster
    ] = Field(default_factory=list, alias="CharacterBaseBloomGenericItemMaster")
    character_base_master: List[CharacterBaseMaster] = Field(
        default_factory=list, alias="CharacterBaseMaster"
    )
    character_bloom_bonus_group_master: List[CharacterBloomBonusGroupMaster] = Field(
        default_factory=list, alias="CharacterBloomBonusGroupMaster"
    )
    character_bloom_detail_master: List[CharacterBloomDetailMaster] = Field(
        default_factory=list, alias="CharacterBloomDetailMaster"
    )
    character_bloom_item_master: List[CharacterBloomItemMaster] = Field(
        default_factory=list, alias="CharacterBloomItemMaster"
    )
    character_episode_master: List[CharacterEpisodeMaster] = Field(
        default_factory=list, alias="CharacterEpisodeMaster"
    )
    character_episode_relation_master: List[CharacterEpisodeRelationMaster] = Field(
        default_factory=list, alias="CharacterEpisodeRelationMaster"
    )
    character_episode_release_item_group_master: List[
        CharacterEpisodeReleaseItemGroupMaster
    ] = Field(default_factory=list, alias="CharacterEpisodeReleaseItemGroupMaster")
    character_experience_item_master: List[CharacterExperienceItemMaster] = Field(
        default_factory=list, alias="CharacterExperienceItemMaster"
    )
    character_key_mission_master: List[CharacterKeyMissionMaster] = Field(
        default_factory=list, alias="CharacterKeyMissionMaster"
    )
    character_lesson_score_reward_master: List[CharacterLessonScoreRewardMaster] = (
        Field(default_factory=list, alias="CharacterLessonScoreRewardMaster")
    )
    character_level_master: List[CharacterLevelMaster] = Field(
        default_factory=list, alias="CharacterLevelMaster"
    )
    character_master: List[CharacterMaster] = Field(
        default_factory=list, alias="CharacterMaster"
    )
    character_mission_category_level_master: List[
        CharacterMissionCategoryLevelMaster
    ] = Field(default_factory=list, alias="CharacterMissionCategoryLevelMaster")
    character_mission_item_master: List[CharacterMissionItemMaster] = Field(
        default_factory=list, alias="CharacterMissionItemMaster"
    )
    character_mission_master: List[CharacterMissionMaster] = Field(
        default_factory=list, alias="CharacterMissionMaster"
    )
    character_mission_stage_master: List[CharacterMissionStageMaster] = Field(
        default_factory=list, alias="CharacterMissionStageMaster"
    )
    character_piece_master: List[CharacterPieceMaster] = Field(
        default_factory=list, alias="CharacterPieceMaster"
    )
    character_point_event_character_ranking_reward_item_package_master: List[
        CharacterPointEventCharacterRankingRewardItemPackageMaster
    ] = Field(
        default_factory=list,
        alias="CharacterPointEventCharacterRankingRewardItemPackageMaster",
    )
    character_point_event_character_ranking_reward_master: List[
        CharacterPointEventCharacterRankingRewardMaster
    ] = Field(
        default_factory=list, alias="CharacterPointEventCharacterRankingRewardMaster"
    )
    character_point_event_master: List[CharacterPointEventMaster] = Field(
        default_factory=list, alias="CharacterPointEventMaster"
    )
    character_profile_restriction_master: List[CharacterProfileRestrictionMaster] = (
        Field(default_factory=list, alias="CharacterProfileRestrictionMaster")
    )
    character_sense_enhance_item_group_master: List[
        CharacterSenseEnhanceItemGroupMaster
    ] = Field(default_factory=list, alias="CharacterSenseEnhanceItemGroupMaster")
    character_star_rank_master: List[CharacterStarRankMaster] = Field(
        default_factory=list, alias="CharacterStarRankMaster"
    )
    character_star_rank_reward_group_master: List[
        CharacterStarRankRewardGroupMaster
    ] = Field(default_factory=list, alias="CharacterStarRankRewardGroupMaster")
    circle_event_circle_point_reward_master: List[
        CircleEventCirclePointRewardMaster
    ] = Field(default_factory=list, alias="CircleEventCirclePointRewardMaster")
    circle_event_circle_ranking_reward_item_package_master: List[
        CircleEventCircleRankingRewardItemPackageMaster
    ] = Field(
        default_factory=list, alias="CircleEventCircleRankingRewardItemPackageMaster"
    )
    circle_event_circle_ranking_reward_master: List[
        CircleEventCircleRankingRewardMaster
    ] = Field(default_factory=list, alias="CircleEventCircleRankingRewardMaster")
    circle_event_master: List[CircleEventMaster] = Field(
        default_factory=list, alias="CircleEventMaster"
    )
    circle_event_mission_master: List[CircleEventMissionMaster] = Field(
        default_factory=list, alias="CircleEventMissionMaster"
    )
    circle_event_mission_refresh_setting_group_master: List[
        CircleEventMissionRefreshSettingGroupMaster
    ] = Field(default_factory=list, alias="CircleEventMissionRefreshSettingGroupMaster")
    circle_support_company_level_detail_master: List[
        CircleSupportCompanyLevelDetailMaster
    ] = Field(default_factory=list, alias="CircleSupportCompanyLevelDetailMaster")
    circle_support_company_level_limit_master: List[
        CircleSupportCompanyLevelLimitMaster
    ] = Field(default_factory=list, alias="CircleSupportCompanyLevelLimitMaster")
    circle_theater_level_master: List[CircleTheaterLevelMaster] = Field(
        default_factory=list, alias="CircleTheaterLevelMaster"
    )
    comeback_campaign_master: List[ComebackCampaignMaster] = Field(
        default_factory=list, alias="ComebackCampaignMaster"
    )
    comic_master: List[ComicMaster] = Field(default_factory=list, alias="ComicMaster")
    company_master: List[CompanyMaster] = Field(
        default_factory=list, alias="CompanyMaster"
    )
    concert_master: List[ConcertMaster] = Field(
        default_factory=list, alias="ConcertMaster"
    )
    concert_stage_master: List[ConcertStageMaster] = Field(
        default_factory=list, alias="ConcertStageMaster"
    )
    concours_master: List[ConcoursMaster] = Field(
        default_factory=list, alias="ConcoursMaster"
    )
    concours_point_reward_master: List[ConcoursPointRewardMaster] = Field(
        default_factory=list, alias="ConcoursPointRewardMaster"
    )
    costume_group_master: List[CostumeGroupMaster] = Field(
        default_factory=list, alias="CostumeGroupMaster"
    )
    costume_master: List[CostumeMaster] = Field(
        default_factory=list, alias="CostumeMaster"
    )
    costume_wearable_character_group_master: List[
        CostumeWearableCharacterGroupMaster
    ] = Field(default_factory=list, alias="CostumeWearableCharacterGroupMaster")
    course_ranking_reward_master: List[CourseRankingRewardMaster] = Field(
        default_factory=list, alias="CourseRankingRewardMaster"
    )
    decoration_master: List[DecorationMaster] = Field(
        default_factory=list, alias="DecorationMaster"
    )
    dugong_run_course_master: List[DugongRunCourseMaster] = Field(
        default_factory=list, alias="DugongRunCourseMaster"
    )
    dugong_run_reward_master: List[DugongRunRewardMaster] = Field(
        default_factory=list, alias="DugongRunRewardMaster"
    )
    effect_duration_group_master: List[EffectDurationGroupMaster] = Field(
        default_factory=list, alias="EffectDurationGroupMaster"
    )
    effect_master: List[EffectMaster] = Field(
        default_factory=list, alias="EffectMaster"
    )
    effect_trigger_character_base_group_master: List[
        EffectTriggerCharacterBaseGroupMaster
    ] = Field(default_factory=list, alias="EffectTriggerCharacterBaseGroupMaster")
    episode_master: List[EpisodeMaster] = Field(
        default_factory=list, alias="EpisodeMaster"
    )
    episode_reward_package_master: List[EpisodeRewardPackageMaster] = Field(
        default_factory=list, alias="EpisodeRewardPackageMaster"
    )
    event_box_gacha_box_master: List[EventBoxGachaBoxMaster] = Field(
        default_factory=list, alias="EventBoxGachaBoxMaster"
    )
    event_box_gacha_master: List[EventBoxGachaMaster] = Field(
        default_factory=list, alias="EventBoxGachaMaster"
    )
    event_box_gacha_text_template_master: List[EventBoxGachaTextTemplateMaster] = Field(
        default_factory=list, alias="EventBoxGachaTextTemplateMaster"
    )
    event_camp_class_master: List[EventCampClassMaster] = Field(
        default_factory=list, alias="EventCampClassMaster"
    )
    event_camp_master: List[EventCampMaster] = Field(
        default_factory=list, alias="EventCampMaster"
    )
    event_camp_support_point_reward_master: List[EventCampSupportPointRewardMaster] = (
        Field(default_factory=list, alias="EventCampSupportPointRewardMaster")
    )
    event_master: List[EventMaster] = Field(default_factory=list, alias="EventMaster")
    exchange_shop_master: List[ExchangeShopMaster] = Field(
        default_factory=list, alias="ExchangeShopMaster"
    )
    facial_expression_master: List[FacialExpressionMaster] = Field(
        default_factory=list, alias="FacialExpressionMaster"
    )
    film_item_master: List[FilmItemMaster] = Field(
        default_factory=list, alias="FilmItemMaster"
    )
    friend_invitation_mission_master: List[FriendInvitationMissionMaster] = Field(
        default_factory=list, alias="FriendInvitationMissionMaster"
    )
    gacha_master: List[GachaMaster] = Field(default_factory=list, alias="GachaMaster")
    gacha_text_template_master: List[GachaTextTemplateMaster] = Field(
        default_factory=list, alias="GachaTextTemplateMaster"
    )
    game_hint_master: List[GameHintMaster] = Field(
        default_factory=list, alias="GameHintMaster"
    )
    ghost_live_master: List[GhostLiveMaster] = Field(
        default_factory=list, alias="GhostLiveMaster"
    )
    gradual_mission_group_master: List[GradualMissionGroupMaster] = Field(
        default_factory=list, alias="GradualMissionGroupMaster"
    )
    head_direction_master: List[HeadDirectionMaster] = Field(
        default_factory=list, alias="HeadDirectionMaster"
    )
    head_motion_master: List[HeadMotionMaster] = Field(
        default_factory=list, alias="HeadMotionMaster"
    )
    home_b_g_m_detail_master: List[HomeBGMDetailMaster] = Field(
        default_factory=list, alias="HomeBGMDetailMaster"
    )
    home_b_g_m_master: List[HomeBGMMaster] = Field(
        default_factory=list, alias="HomeBGMMaster"
    )
    home_background_master: List[HomeBackgroundMaster] = Field(
        default_factory=list, alias="HomeBackgroundMaster"
    )
    home_character_master: List[HomeCharacterMaster] = Field(
        default_factory=list, alias="HomeCharacterMaster"
    )
    home_character_voice_master: List[HomeCharacterVoiceMaster] = Field(
        default_factory=list, alias="HomeCharacterVoiceMaster"
    )
    home_character_voice_period_master: List[HomeCharacterVoicePeriodMaster] = Field(
        default_factory=list, alias="HomeCharacterVoicePeriodMaster"
    )
    home_poster_master: List[HomePosterMaster] = Field(
        default_factory=list, alias="HomePosterMaster"
    )
    home_skin_master: List[HomeSkinMaster] = Field(
        default_factory=list, alias="HomeSkinMaster"
    )
    icon_frame_master: List[IconFrameMaster] = Field(
        default_factory=list, alias="IconFrameMaster"
    )
    item_master: List[ItemMaster] = Field(default_factory=list, alias="ItemMaster")
    jewel_shop_category_master: List[JewelShopCategoryMaster] = Field(
        default_factory=list, alias="JewelShopCategoryMaster"
    )
    jewel_shop_item_master: List[JewelShopItemMaster] = Field(
        default_factory=list, alias="JewelShopItemMaster"
    )
    leader_sense_master: List[LeaderSenseMaster] = Field(
        default_factory=list, alias="LeaderSenseMaster"
    )
    league_all_class_global_ranking_reward_thing_master: List[
        LeagueAllClassGlobalRankingRewardPackageMaster
    ] = Field(
        default_factory=list, alias="LeagueAllClassGlobalRankingRewardThingMaster"
    )
    league_class_group_master: List[LeagueClassGroupMaster] = Field(
        default_factory=list, alias="LeagueClassGroupMaster"
    )
    league_group_ranking_reward_package_master: List[
        LeagueGroupRankingRewardPackageMaster
    ] = Field(default_factory=list, alias="LeagueGroupRankingRewardPackageMaster")
    league_master: List[LeagueMaster] = Field(
        default_factory=list, alias="LeagueMaster"
    )
    league_play_reward_package_master: List[LeaguePlayRewardPackageMaster] = Field(
        default_factory=list, alias="LeaguePlayRewardPackageMaster"
    )
    league_reward_package_master: List[LeagueRewardPackageMaster] = Field(
        default_factory=list, alias="LeagueRewardPackageMaster"
    )
    lesson_score_reward_group_master: List[LessonScoreRewardGroupMaster] = Field(
        default_factory=list, alias="LessonScoreRewardGroupMaster"
    )
    lesson_score_reward_master: List[LessonScoreRewardMaster] = Field(
        default_factory=list, alias="LessonScoreRewardMaster"
    )
    light_load_split_effect_master: List[LightLoadSplitEffectMaster] = Field(
        default_factory=list, alias="LightLoadSplitEffectMaster"
    )
    lip_sync_master: List[LipSyncMaster] = Field(
        default_factory=list, alias="LipSyncMaster"
    )
    live_drop_frame_group_master: List[LiveDropFrameGroupMaster] = Field(
        default_factory=list, alias="LiveDropFrameGroupMaster"
    )
    live_master: List[LiveMaster] = Field(default_factory=list, alias="LiveMaster")
    live_setting_master: List[LiveSettingMaster] = Field(
        default_factory=list, alias="LiveSettingMaster"
    )
    login_bonus_spine_costume_master: List[LoginBonusSpineCostumeMaster] = Field(
        default_factory=list, alias="LoginBonusSpineCostumeMaster"
    )
    loop_motion_master: List[LoopMotionMaster] = Field(
        default_factory=list, alias="LoopMotionMaster"
    )
    market_frame_thing_master: List[MarketFrameThingMaster] = Field(
        default_factory=list, alias="MarketFrameThingMaster"
    )
    mission_master: List[MissionMaster] = Field(
        default_factory=list, alias="MissionMaster"
    )
    mission_pass_detail_master: List[MissionPassDetailMaster] = Field(
        default_factory=list, alias="MissionPassDetailMaster"
    )
    mission_pass_loop_reward_master: List[MissionPassLoopRewardMaster] = Field(
        default_factory=list, alias="MissionPassLoopRewardMaster"
    )
    mission_pass_loop_reward_thing_master: List[MissionPassLoopRewardThingMaster] = (
        Field(default_factory=list, alias="MissionPassLoopRewardThingMaster")
    )
    mission_pass_master: List[MissionPassMaster] = Field(
        default_factory=list, alias="MissionPassMaster"
    )
    multi_live_schedule_master: List[MultiLiveScheduleMaster] = Field(
        default_factory=list, alias="MultiLiveScheduleMaster"
    )
    music_course_master: List[MusicCourseMaster] = Field(
        default_factory=list, alias="MusicCourseMaster"
    )
    music_course_reward_group_master: List[MusicCourseRewardGroupMaster] = Field(
        default_factory=list, alias="MusicCourseRewardGroupMaster"
    )
    music_group_detail_master: List[MusicGroupDetailMaster] = Field(
        default_factory=list, alias="MusicGroupDetailMaster"
    )
    music_group_master: List[MusicGroupMaster] = Field(
        default_factory=list, alias="MusicGroupMaster"
    )
    music_master: List[MusicMaster] = Field(default_factory=list, alias="MusicMaster")
    music_video_default_costume_group_master: List[
        MusicVideoDefaultCostumeGroupMaster
    ] = Field(default_factory=list, alias="MusicVideoDefaultCostumeGroupMaster")
    music_video_master: List[MusicVideoMaster] = Field(
        default_factory=list, alias="MusicVideoMaster"
    )
    music_vocal_version_master: List[MusicVocalVersionMaster] = Field(
        default_factory=list, alias="MusicVocalVersionMaster"
    )
    name_base_color_master: List[NameBaseColorMaster] = Field(
        default_factory=list, alias="NameBaseColorMaster"
    )
    name_color_master: List[NameColorMaster] = Field(
        default_factory=list, alias="NameColorMaster"
    )
    nameplate_master: List[NameplateMaster] = Field(
        default_factory=list, alias="NameplateMaster"
    )
    ng_word_master: List[NgWordMaster] = Field(
        default_factory=list, alias="NgWordMaster"
    )
    note_master: List[NoteMaster] = Field(default_factory=list, alias="NoteMaster")
    permanent_market_thing_master: List[PermanentMarketThingMaster] = Field(
        default_factory=list, alias="PermanentMarketThingMaster"
    )
    photo_effect_change_item_master: List[PhotoEffectChangeItemMaster] = Field(
        default_factory=list, alias="PhotoEffectChangeItemMaster"
    )
    photo_effect_master: List[PhotoEffectMaster] = Field(
        default_factory=list, alias="PhotoEffectMaster"
    )
    photo_effect_type_group_master: List[PhotoEffectTypeGroupMaster] = Field(
        default_factory=list, alias="PhotoEffectTypeGroupMaster"
    )
    photo_effect_variety_change_detail_master: List[
        PhotoEffectVarietyChangeDetailMaster
    ] = Field(default_factory=list, alias="PhotoEffectVarietyChangeDetailMaster")
    photo_effect_variety_up_detail_master: List[PhotoEffectVarietyUpDetailMaster] = (
        Field(default_factory=list, alias="PhotoEffectVarietyUpDetailMaster")
    )
    photo_level_up_item_group_master: List[PhotoLevelUpItemGroupMaster] = Field(
        default_factory=list, alias="PhotoLevelUpItemGroupMaster"
    )
    photo_spot_master: List[PhotoSpotMaster] = Field(
        default_factory=list, alias="PhotoSpotMaster"
    )
    pickup_character_mission_detail_group_master: List[
        PickupCharacterMissionDetailGroupMaster
    ] = Field(default_factory=list, alias="PickupCharacterMissionDetailGroupMaster")
    pickup_character_mission_detail_master: List[PickupCharacterMissionDetailMaster] = (
        Field(default_factory=list, alias="PickupCharacterMissionDetailMaster")
    )
    pickup_character_mission_master: List[PickupCharacterMissionMaster] = Field(
        default_factory=list, alias="PickupCharacterMissionMaster"
    )
    pickup_selection_gacha_master: List[PickupSelectionGachaMaster] = Field(
        default_factory=list, alias="PickupSelectionGachaMaster"
    )
    player_rank_cap_master: List[PlayerRankCapMaster] = Field(
        default_factory=list, alias="PlayerRankCapMaster"
    )
    player_rank_master: List[PlayerRankMaster] = Field(
        default_factory=list, alias="PlayerRankMaster"
    )
    poster_ability_master: List[PosterAbilityMaster] = Field(
        default_factory=list, alias="PosterAbilityMaster"
    )
    poster_level_pattern_group_master: List[PosterLevelPatternGroupMaster] = Field(
        default_factory=list, alias="PosterLevelPatternGroupMaster"
    )
    poster_master: List[PosterMaster] = Field(
        default_factory=list, alias="PosterMaster"
    )
    poster_release_item_group_master: List[PosterReleaseItemGroupMaster] = Field(
        default_factory=list, alias="PosterReleaseItemGroupMaster"
    )
    poster_story_master: List[PosterStoryMaster] = Field(
        default_factory=list, alias="PosterStoryMaster"
    )
    random_effect_group_master: List[RandomEffectGroupMaster] = Field(
        default_factory=list, alias="RandomEffectGroupMaster"
    )
    result_voice_master: List[ResultVoiceMaster] = Field(
        default_factory=list, alias="ResultVoiceMaster"
    )
    reward_rule_master: List[RewardRuleMaster] = Field(
        default_factory=list, alias="RewardRuleMaster"
    )
    roulette_event_master: List[RouletteEventMaster] = Field(
        default_factory=list, alias="RouletteEventMaster"
    )
    roulette_master: List[RouletteMaster] = Field(
        default_factory=list, alias="RouletteMaster"
    )
    roulette_prize_master: List[RoulettePrizeMaster] = Field(
        default_factory=list, alias="RoulettePrizeMaster"
    )
    scene_camera_master: List[SceneCameraMaster] = Field(
        default_factory=list, alias="SceneCameraMaster"
    )
    sense_branch_master: List[SenseBranchMaster] = Field(
        default_factory=list, alias="SenseBranchMaster"
    )
    sense_master: List[SenseMaster] = Field(default_factory=list, alias="SenseMaster")
    sense_notation_master: List[SenseNotationMaster] = Field(
        default_factory=list, alias="SenseNotationMaster"
    )
    sense_performance_master: List[SensePerformanceMaster] = Field(
        default_factory=list, alias="SensePerformanceMaster"
    )
    sign_master: List[SignMaster] = Field(default_factory=list, alias="SignMaster")
    special_episode_master: List[SpecialEpisodeMaster] = Field(
        default_factory=list, alias="SpecialEpisodeMaster"
    )
    special_event_master: List[SpecialEventMaster] = Field(
        default_factory=list, alias="SpecialEventMaster"
    )
    special_story_master: List[SpecialStoryMaster] = Field(
        default_factory=list, alias="SpecialStoryMaster"
    )
    splash_master: List[SplashMaster] = Field(
        default_factory=list, alias="SplashMaster"
    )
    spot_conversation_master: List[SpotConversationMaster] = Field(
        default_factory=list, alias="SpotConversationMaster"
    )
    stamina_recovery_item_master: List[StaminaRecoveryItemMaster] = Field(
        default_factory=list, alias="StaminaRecoveryItemMaster"
    )
    stamp_master: List[StampMaster] = Field(default_factory=list, alias="StampMaster")
    star_act_branch_master: List[StarActBranchMaster] = Field(
        default_factory=list, alias="StarActBranchMaster"
    )
    star_act_condition_master: List[StarActConditionMaster] = Field(
        default_factory=list, alias="StarActConditionMaster"
    )
    star_act_master: List[StarActMaster] = Field(
        default_factory=list, alias="StarActMaster"
    )
    star_rank_reward_master: List[StarRankRewardMaster] = Field(
        default_factory=list, alias="StarRankRewardMaster"
    )
    stepup_gacha_group_master: List[StepupGachaGroupMaster] = Field(
        default_factory=list, alias="StepupGachaGroupMaster"
    )
    story_event_bonus_character_base_master: List[
        StoryEventBonusCharacterBaseMaster
    ] = Field(default_factory=list, alias="StoryEventBonusCharacterBaseMaster")
    story_event_circle_high_score_reward_master: List[
        StoryEventCircleHighScoreRewardMaster
    ] = Field(default_factory=list, alias="StoryEventCircleHighScoreRewardMaster")
    story_event_circle_master: List[StoryEventCircleMaster] = Field(
        default_factory=list, alias="StoryEventCircleMaster"
    )
    story_event_circle_mission_master: List[StoryEventCircleMissionMaster] = Field(
        default_factory=list, alias="StoryEventCircleMissionMaster"
    )
    story_event_circle_mission_reward_master: List[
        StoryEventCircleMissionRewardMaster
    ] = Field(default_factory=list, alias="StoryEventCircleMissionRewardMaster")
    story_event_episode_master: List[StoryEventEpisodeMaster] = Field(
        default_factory=list, alias="StoryEventEpisodeMaster"
    )
    story_event_high_score_buff_master: List[StoryEventHighScoreBuffMaster] = Field(
        default_factory=list, alias="StoryEventHighScoreBuffMaster"
    )
    story_event_high_score_buff_pattern_group_master: List[
        StoryEventHighScoreBuffPatternGroupMaster
    ] = Field(default_factory=list, alias="StoryEventHighScoreBuffPatternGroupMaster")
    story_event_high_score_buff_setting_master: List[
        StoryEventHighScoreBuffSettingMaster
    ] = Field(default_factory=list, alias="StoryEventHighScoreBuffSettingMaster")
    story_event_high_score_master: List[StoryEventHighScoreMaster] = Field(
        default_factory=list, alias="StoryEventHighScoreMaster"
    )
    story_event_high_score_reward_master: List[StoryEventHighScoreRewardMaster] = Field(
        default_factory=list, alias="StoryEventHighScoreRewardMaster"
    )
    story_event_master: List[StoryEventMaster] = Field(
        default_factory=list, alias="StoryEventMaster"
    )
    story_event_reward_item_package: List[StoryEventRewardItemPackage] = Field(
        default_factory=list, alias="StoryEventRewardItemPackage"
    )
    story_event_reward_master: List[StoryEventRewardMaster] = Field(
        default_factory=list, alias="StoryEventRewardMaster"
    )
    story_event_story_bgm_group_master: List[StoryEventStoryBgmGroupMaster] = Field(
        default_factory=list, alias="StoryEventStoryBgmGroupMaster"
    )
    story_event_story_master: List[StoryEventStoryMaster] = Field(
        default_factory=list, alias="StoryEventStoryMaster"
    )
    story_event_total_point_reward_master: List[StoryEventTotalPointRewardMaster] = (
        Field(default_factory=list, alias="StoryEventTotalPointRewardMaster")
    )
    story_master: List[StoryMaster] = Field(default_factory=list, alias="StoryMaster")
    story_relation_master: List[StoryRelationMaster] = Field(
        default_factory=list, alias="StoryRelationMaster"
    )
    team_challenge_master: List[TeamChallengeMaster] = Field(
        default_factory=list, alias="TeamChallengeMaster"
    )
    theater_chapter_master: List[TheaterChapterMaster] = Field(
        default_factory=list, alias="TheaterChapterMaster"
    )
    theater_story_master: List[TheaterStoryMaster] = Field(
        default_factory=list, alias="TheaterStoryMaster"
    )
    time_limited_control_master: List[TimeLimitedControlMaster] = Field(
        default_factory=list, alias="TimeLimitedControlMaster"
    )
    tip_master: List[TipMaster] = Field(default_factory=list, alias="TipMaster")
    title_background_master: List[TitleBackgroundMaster] = Field(
        default_factory=list, alias="TitleBackgroundMaster"
    )
    title_call_voice_master: List[TitleCallVoiceMaster] = Field(
        default_factory=list, alias="TitleCallVoiceMaster"
    )
    title_decoration_master: List[TitleDecorationMaster] = Field(
        default_factory=list, alias="TitleDecorationMaster"
    )
    total_point_event_master: List[TotalPointEventMaster] = Field(
        default_factory=list, alias="TotalPointEventMaster"
    )
    total_point_event_reward_master: List[TotalPointEventRewardMaster] = Field(
        default_factory=list, alias="TotalPointEventRewardMaster"
    )
    tournament_master: List[TournamentMaster] = Field(
        default_factory=list, alias="TournamentMaster"
    )
    tournament_qualifying_master: List[TournamentQualifyingMaster] = Field(
        default_factory=list, alias="TournamentQualifyingMaster"
    )
    trial_party_accessory_master: List[TrialPartyAccessoryMaster] = Field(
        default_factory=list, alias="TrialPartyAccessoryMaster"
    )
    trial_party_character_master: List[TrialPartyCharacterMaster] = Field(
        default_factory=list, alias="TrialPartyCharacterMaster"
    )
    trial_party_event_master: List[TrialPartyEventMaster] = Field(
        default_factory=list, alias="TrialPartyEventMaster"
    )
    trial_party_event_stage_master: List[TrialPartyEventStageMaster] = Field(
        default_factory=list, alias="TrialPartyEventStageMaster"
    )
    trial_party_master: List[TrialPartyMaster] = Field(
        default_factory=list, alias="TrialPartyMaster"
    )
    trial_party_poster_master: List[TrialPartyPosterMaster] = Field(
        default_factory=list, alias="TrialPartyPosterMaster"
    )
    triple_cast_all_class_global_ranking_reward_thing_master: List[
        TripleCastAllClassGlobalRankingRewardPackageMaster
    ] = Field(
        default_factory=list, alias="TripleCastAllClassGlobalRankingRewardThingMaster"
    )
    triple_cast_group_ranking_reward_package_master: List[
        TripleCastGroupRankingRewardPackageMaster
    ] = Field(default_factory=list, alias="TripleCastGroupRankingRewardPackageMaster")
    triple_cast_master: List[TripleCastMaster] = Field(
        default_factory=list, alias="TripleCastMaster"
    )
    trophy_group_master: List[TrophyGroupMaster] = Field(
        default_factory=list, alias="TrophyGroupMaster"
    )
    trophy_master: List[TrophyMaster] = Field(
        default_factory=list, alias="TrophyMaster"
    )
    unlock_condition_master: List[UnlockConditionMaster] = Field(
        default_factory=list, alias="UnlockConditionMaster"
    )


MasterData.model_rebuild(_types_namespace=_ns)

TABLES = {
    "AccessoryEffectFilterMaster": AccessoryEffectFilterMaster,
    "AccessoryEffectMaster": AccessoryEffectMaster,
    "AccessoryLevelPatternGroupMaster": AccessoryLevelPatternGroupMaster,
    "AccessoryMaster": AccessoryMaster,
    "ActivityLogMessageTemplateMaster": ActivityLogMessageTemplateMaster,
    "AdditionalRewardPackageMaster": AdditionalRewardPackageMaster,
    "AlbumEffectMaster": AlbumEffectMaster,
    "AlbumThemeMaster": AlbumThemeMaster,
    "AnotherNotationMaster": AnotherNotationMaster,
    "AuditionMaster": AuditionMaster,
    "AuditionPhaseMaster": AuditionPhaseMaster,
    "AuditionRewardPackageMaster": AuditionRewardPackageMaster,
    "BannerMaster": BannerMaster,
    "BodyMotionMaster": BodyMotionMaster,
    "BombMaster": BombMaster,
    "BonusLiveMaster": BonusLiveMaster,
    "BonusLiveStageMaster": BonusLiveStageMaster,
    "BuffItemMaster": BuffItemMaster,
    "CampaignMaster": CampaignMaster,
    "CategoryGroupMaster": CategoryGroupMaster,
    "CategoryMaster": CategoryMaster,
    "ChangeBodyMotionMaster": ChangeBodyMotionMaster,
    "CharacterAwakeningItemGroupMaster": CharacterAwakeningItemGroupMaster,
    "CharacterAwakeningItemMaster": CharacterAwakeningItemMaster,
    "CharacterBaseBloomGenericItemMaster": CharacterBaseBloomGenericItemMaster,
    "CharacterBaseMaster": CharacterBaseMaster,
    "CharacterBloomBonusGroupMaster": CharacterBloomBonusGroupMaster,
    "CharacterBloomDetailMaster": CharacterBloomDetailMaster,
    "CharacterBloomItemMaster": CharacterBloomItemMaster,
    "CharacterEpisodeMaster": CharacterEpisodeMaster,
    "CharacterEpisodeRelationMaster": CharacterEpisodeRelationMaster,
    "CharacterEpisodeReleaseItemGroupMaster": CharacterEpisodeReleaseItemGroupMaster,
    "CharacterExperienceItemMaster": CharacterExperienceItemMaster,
    "CharacterKeyMissionMaster": CharacterKeyMissionMaster,
    "CharacterLessonScoreRewardMaster": CharacterLessonScoreRewardMaster,
    "CharacterLevelMaster": CharacterLevelMaster,
    "CharacterMaster": CharacterMaster,
    "CharacterMissionCategoryLevelMaster": CharacterMissionCategoryLevelMaster,
    "CharacterMissionItemMaster": CharacterMissionItemMaster,
    "CharacterMissionMaster": CharacterMissionMaster,
    "CharacterMissionStageMaster": CharacterMissionStageMaster,
    "CharacterPieceMaster": CharacterPieceMaster,
    "CharacterPointEventCharacterRankingRewardItemPackageMaster": CharacterPointEventCharacterRankingRewardItemPackageMaster,
    "CharacterPointEventCharacterRankingRewardMaster": CharacterPointEventCharacterRankingRewardMaster,
    "CharacterPointEventMaster": CharacterPointEventMaster,
    "CharacterProfileRestrictionMaster": CharacterProfileRestrictionMaster,
    "CharacterSenseEnhanceItemGroupMaster": CharacterSenseEnhanceItemGroupMaster,
    "CharacterStarRankMaster": CharacterStarRankMaster,
    "CharacterStarRankRewardGroupMaster": CharacterStarRankRewardGroupMaster,
    "CircleEventCirclePointRewardMaster": CircleEventCirclePointRewardMaster,
    "CircleEventCircleRankingRewardItemPackageMaster": CircleEventCircleRankingRewardItemPackageMaster,
    "CircleEventCircleRankingRewardMaster": CircleEventCircleRankingRewardMaster,
    "CircleEventMaster": CircleEventMaster,
    "CircleEventMissionMaster": CircleEventMissionMaster,
    "CircleEventMissionRefreshSettingGroupMaster": CircleEventMissionRefreshSettingGroupMaster,
    "CircleSupportCompanyLevelDetailMaster": CircleSupportCompanyLevelDetailMaster,
    "CircleSupportCompanyLevelLimitMaster": CircleSupportCompanyLevelLimitMaster,
    "CircleTheaterLevelMaster": CircleTheaterLevelMaster,
    "ComebackCampaignMaster": ComebackCampaignMaster,
    "ComicMaster": ComicMaster,
    "CompanyMaster": CompanyMaster,
    "ConcertMaster": ConcertMaster,
    "ConcertStageMaster": ConcertStageMaster,
    "ConcoursMaster": ConcoursMaster,
    "ConcoursPointRewardMaster": ConcoursPointRewardMaster,
    "CostumeGroupMaster": CostumeGroupMaster,
    "CostumeMaster": CostumeMaster,
    "CostumeWearableCharacterGroupMaster": CostumeWearableCharacterGroupMaster,
    "CourseRankingRewardMaster": CourseRankingRewardMaster,
    "DecorationMaster": DecorationMaster,
    "DugongRunCourseMaster": DugongRunCourseMaster,
    "DugongRunRewardMaster": DugongRunRewardMaster,
    "EffectDurationGroupMaster": EffectDurationGroupMaster,
    "EffectMaster": EffectMaster,
    "EffectTriggerCharacterBaseGroupMaster": EffectTriggerCharacterBaseGroupMaster,
    "EpisodeMaster": EpisodeMaster,
    "EpisodeRewardPackageMaster": EpisodeRewardPackageMaster,
    "EventBoxGachaBoxMaster": EventBoxGachaBoxMaster,
    "EventBoxGachaMaster": EventBoxGachaMaster,
    "EventBoxGachaTextTemplateMaster": EventBoxGachaTextTemplateMaster,
    "EventCampClassMaster": EventCampClassMaster,
    "EventCampMaster": EventCampMaster,
    "EventCampSupportPointRewardMaster": EventCampSupportPointRewardMaster,
    "EventMaster": EventMaster,
    "ExchangeShopMaster": ExchangeShopMaster,
    "FacialExpressionMaster": FacialExpressionMaster,
    "FilmItemMaster": FilmItemMaster,
    "FriendInvitationMissionMaster": FriendInvitationMissionMaster,
    "GachaMaster": GachaMaster,
    "GachaTextTemplateMaster": GachaTextTemplateMaster,
    "GameHintMaster": GameHintMaster,
    "GhostLiveMaster": GhostLiveMaster,
    "GradualMissionGroupMaster": GradualMissionGroupMaster,
    "HeadDirectionMaster": HeadDirectionMaster,
    "HeadMotionMaster": HeadMotionMaster,
    "HomeBGMDetailMaster": HomeBGMDetailMaster,
    "HomeBGMMaster": HomeBGMMaster,
    "HomeBackgroundMaster": HomeBackgroundMaster,
    "HomeCharacterMaster": HomeCharacterMaster,
    "HomeCharacterVoiceMaster": HomeCharacterVoiceMaster,
    "HomeCharacterVoicePeriodMaster": HomeCharacterVoicePeriodMaster,
    "HomePosterMaster": HomePosterMaster,
    "HomeSkinMaster": HomeSkinMaster,
    "IconFrameMaster": IconFrameMaster,
    "ItemMaster": ItemMaster,
    "JewelShopCategoryMaster": JewelShopCategoryMaster,
    "JewelShopItemMaster": JewelShopItemMaster,
    "LeaderSenseMaster": LeaderSenseMaster,
    "LeagueAllClassGlobalRankingRewardThingMaster": LeagueAllClassGlobalRankingRewardPackageMaster,
    "LeagueClassGroupMaster": LeagueClassGroupMaster,
    "LeagueGroupRankingRewardPackageMaster": LeagueGroupRankingRewardPackageMaster,
    "LeagueMaster": LeagueMaster,
    "LeaguePlayRewardPackageMaster": LeaguePlayRewardPackageMaster,
    "LeagueRewardPackageMaster": LeagueRewardPackageMaster,
    "LessonScoreRewardGroupMaster": LessonScoreRewardGroupMaster,
    "LessonScoreRewardMaster": LessonScoreRewardMaster,
    "LightLoadSplitEffectMaster": LightLoadSplitEffectMaster,
    "LipSyncMaster": LipSyncMaster,
    "LiveDropFrameGroupMaster": LiveDropFrameGroupMaster,
    "LiveMaster": LiveMaster,
    "LiveSettingMaster": LiveSettingMaster,
    "LoginBonusSpineCostumeMaster": LoginBonusSpineCostumeMaster,
    "LoopMotionMaster": LoopMotionMaster,
    "MarketFrameThingMaster": MarketFrameThingMaster,
    "MissionMaster": MissionMaster,
    "MissionPassDetailMaster": MissionPassDetailMaster,
    "MissionPassLoopRewardMaster": MissionPassLoopRewardMaster,
    "MissionPassLoopRewardThingMaster": MissionPassLoopRewardThingMaster,
    "MissionPassMaster": MissionPassMaster,
    "MultiLiveScheduleMaster": MultiLiveScheduleMaster,
    "MusicCourseMaster": MusicCourseMaster,
    "MusicCourseRewardGroupMaster": MusicCourseRewardGroupMaster,
    "MusicGroupDetailMaster": MusicGroupDetailMaster,
    "MusicGroupMaster": MusicGroupMaster,
    "MusicMaster": MusicMaster,
    "MusicVideoDefaultCostumeGroupMaster": MusicVideoDefaultCostumeGroupMaster,
    "MusicVideoMaster": MusicVideoMaster,
    "MusicVocalVersionMaster": MusicVocalVersionMaster,
    "NameBaseColorMaster": NameBaseColorMaster,
    "NameColorMaster": NameColorMaster,
    "NameplateMaster": NameplateMaster,
    "NgWordMaster": NgWordMaster,
    "NoteMaster": NoteMaster,
    "PermanentMarketThingMaster": PermanentMarketThingMaster,
    "PhotoEffectChangeItemMaster": PhotoEffectChangeItemMaster,
    "PhotoEffectMaster": PhotoEffectMaster,
    "PhotoEffectTypeGroupMaster": PhotoEffectTypeGroupMaster,
    "PhotoEffectVarietyChangeDetailMaster": PhotoEffectVarietyChangeDetailMaster,
    "PhotoEffectVarietyUpDetailMaster": PhotoEffectVarietyUpDetailMaster,
    "PhotoLevelUpItemGroupMaster": PhotoLevelUpItemGroupMaster,
    "PhotoSpotMaster": PhotoSpotMaster,
    "PickupCharacterMissionDetailGroupMaster": PickupCharacterMissionDetailGroupMaster,
    "PickupCharacterMissionDetailMaster": PickupCharacterMissionDetailMaster,
    "PickupCharacterMissionMaster": PickupCharacterMissionMaster,
    "PickupSelectionGachaMaster": PickupSelectionGachaMaster,
    "PlayerRankCapMaster": PlayerRankCapMaster,
    "PlayerRankMaster": PlayerRankMaster,
    "PosterAbilityMaster": PosterAbilityMaster,
    "PosterLevelPatternGroupMaster": PosterLevelPatternGroupMaster,
    "PosterMaster": PosterMaster,
    "PosterReleaseItemGroupMaster": PosterReleaseItemGroupMaster,
    "PosterStoryMaster": PosterStoryMaster,
    "RandomEffectGroupMaster": RandomEffectGroupMaster,
    "ResultVoiceMaster": ResultVoiceMaster,
    "RewardRuleMaster": RewardRuleMaster,
    "RouletteEventMaster": RouletteEventMaster,
    "RouletteMaster": RouletteMaster,
    "RoulettePrizeMaster": RoulettePrizeMaster,
    "SceneCameraMaster": SceneCameraMaster,
    "SenseBranchMaster": SenseBranchMaster,
    "SenseMaster": SenseMaster,
    "SenseNotationMaster": SenseNotationMaster,
    "SensePerformanceMaster": SensePerformanceMaster,
    "SignMaster": SignMaster,
    "SpecialEpisodeMaster": SpecialEpisodeMaster,
    "SpecialEventMaster": SpecialEventMaster,
    "SpecialStoryMaster": SpecialStoryMaster,
    "SplashMaster": SplashMaster,
    "SpotConversationMaster": SpotConversationMaster,
    "StaminaRecoveryItemMaster": StaminaRecoveryItemMaster,
    "StampMaster": StampMaster,
    "StarActBranchMaster": StarActBranchMaster,
    "StarActConditionMaster": StarActConditionMaster,
    "StarActMaster": StarActMaster,
    "StarRankRewardMaster": StarRankRewardMaster,
    "StepupGachaGroupMaster": StepupGachaGroupMaster,
    "StoryEventBonusCharacterBaseMaster": StoryEventBonusCharacterBaseMaster,
    "StoryEventCircleHighScoreRewardMaster": StoryEventCircleHighScoreRewardMaster,
    "StoryEventCircleMaster": StoryEventCircleMaster,
    "StoryEventCircleMissionMaster": StoryEventCircleMissionMaster,
    "StoryEventCircleMissionRewardMaster": StoryEventCircleMissionRewardMaster,
    "StoryEventEpisodeMaster": StoryEventEpisodeMaster,
    "StoryEventHighScoreBuffMaster": StoryEventHighScoreBuffMaster,
    "StoryEventHighScoreBuffPatternGroupMaster": StoryEventHighScoreBuffPatternGroupMaster,
    "StoryEventHighScoreBuffSettingMaster": StoryEventHighScoreBuffSettingMaster,
    "StoryEventHighScoreMaster": StoryEventHighScoreMaster,
    "StoryEventHighScoreRewardMaster": StoryEventHighScoreRewardMaster,
    "StoryEventMaster": StoryEventMaster,
    "StoryEventRewardItemPackage": StoryEventRewardItemPackage,
    "StoryEventRewardMaster": StoryEventRewardMaster,
    "StoryEventStoryBgmGroupMaster": StoryEventStoryBgmGroupMaster,
    "StoryEventStoryMaster": StoryEventStoryMaster,
    "StoryEventTotalPointRewardMaster": StoryEventTotalPointRewardMaster,
    "StoryMaster": StoryMaster,
    "StoryRelationMaster": StoryRelationMaster,
    "TeamChallengeMaster": TeamChallengeMaster,
    "TheaterChapterMaster": TheaterChapterMaster,
    "TheaterStoryMaster": TheaterStoryMaster,
    "TimeLimitedControlMaster": TimeLimitedControlMaster,
    "TipMaster": TipMaster,
    "TitleBackgroundMaster": TitleBackgroundMaster,
    "TitleCallVoiceMaster": TitleCallVoiceMaster,
    "TitleDecorationMaster": TitleDecorationMaster,
    "TotalPointEventMaster": TotalPointEventMaster,
    "TotalPointEventRewardMaster": TotalPointEventRewardMaster,
    "TournamentMaster": TournamentMaster,
    "TournamentQualifyingMaster": TournamentQualifyingMaster,
    "TrialPartyAccessoryMaster": TrialPartyAccessoryMaster,
    "TrialPartyCharacterMaster": TrialPartyCharacterMaster,
    "TrialPartyEventMaster": TrialPartyEventMaster,
    "TrialPartyEventStageMaster": TrialPartyEventStageMaster,
    "TrialPartyMaster": TrialPartyMaster,
    "TrialPartyPosterMaster": TrialPartyPosterMaster,
    "TripleCastAllClassGlobalRankingRewardThingMaster": TripleCastAllClassGlobalRankingRewardPackageMaster,
    "TripleCastGroupRankingRewardPackageMaster": TripleCastGroupRankingRewardPackageMaster,
    "TripleCastMaster": TripleCastMaster,
    "TrophyGroupMaster": TrophyGroupMaster,
    "TrophyMaster": TrophyMaster,
    "UnlockConditionMaster": UnlockConditionMaster,
}

__all__ = [_t.__name__ for _t in _TYPES] + ["MasterData", "TABLES"]
