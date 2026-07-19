import argparse

import yaml
from peewee import (
    SQL,
    AutoField,
    BigIntegerField,
    BooleanField,
    DoubleField,
    IntegerField,
    Model,
    PostgresqlDatabase,
    TextField,
)
from playhouse.postgres_ext import JSONField

from helpers.config import Database

_parser = argparse.ArgumentParser()
_parser.add_argument("--config", default="config.yml", help="Path to config file")
_args = _parser.parse_args()

with open(_args.config, "r", encoding="utf-8") as f:
    CONFIG = Database(**yaml.safe_load(f)["database"])

db = PostgresqlDatabase(
    CONFIG.database,
    user=CONFIG.username,
    password=CONFIG.password,
    host=CONFIG.host,
    port=CONFIG.port,
)

version = 1  # ONLY UPDATE ON CHANGED TABLE. NEW TABLES DON'T TOUCH VERSION


class BaseModel(Model):
    class Meta:
        database = db


class DatabaseInfo(BaseModel):
    version = IntegerField(unique=True, primary_key=True, null=False)


class Accounts(BaseModel):
    userId = BigIntegerField(primary_key=True)
    credential = TextField(unique=True)
    apiToken = TextField(null=True)
    platform = TextField(constraints=[SQL("DEFAULT 'Android'")])
    banLevel = IntegerField(constraints=[SQL("DEFAULT 0")])
    registeredAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastLoginAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "accounts"


class User(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    playerRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentRankPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentStamina = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    maxStaminaRestoredAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    # coin/freeJewel/paidJewel live only in the "currency" table; the User entity reads
    # them via a JOIN in get_users, so there is a single source of truth
    playerRankLimit = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    staminaRecoverTimesWithJewel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    circleUsageRestrictionsEndTime = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    circleId = TextField(null=True)
    gameStartAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hashUserId = TextField(null=True)
    banLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    tutorialStatus = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    monthlyPayment = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    splashLastDisplayedAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isCapedPlayerRank = BooleanField(constraints=[SQL("DEFAULT false")])
    requireCapedPlayerRankAnnounce = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "user"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class UserProfile(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    introduction = TextField(null=True)
    mainUCharacterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    mNameplateId = BigIntegerField(null=True)
    mNameColorId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    mTrophyId1 = BigIntegerField(null=True)
    mTrophyId2 = BigIntegerField(null=True)
    mTrophyId3 = BigIntegerField(null=True)
    playerRate = DoubleField(constraints=[SQL("DEFAULT 0")])
    isPublicPlayerRate = BooleanField(constraints=[SQL("DEFAULT false")])
    leagueClass = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalSpCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isPublicAlbumMainPage = BooleanField(constraints=[SQL("DEFAULT false")])
    mNameplateDetailId = BigIntegerField(null=True)
    mainCharacterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayAwakeningStatus = BooleanField(constraints=[SQL("DEFAULT false")])
    isPublicActivityLog = BooleanField(constraints=[SQL("DEFAULT false")])
    nameBaseColorMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    iconFrameMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    homeSkinMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "user_profile"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class UserPreference(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    multiPartyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    birthDate = BigIntegerField(null=True)

    class Meta:
        table_name = "user_preference"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class HomeDisplayPreference(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    homeCharacterBaseMasterId = BigIntegerField(null=True)
    memberCharacterBaseMasterId = BigIntegerField(null=True)
    storyCharacterBaseMasterId = BigIntegerField(null=True)
    shopCharacterBaseMasterId = BigIntegerField(null=True)
    homeCostumeMasterId = BigIntegerField(null=True)
    memberCostumeMasterId = BigIntegerField(null=True)
    storyCostumeMasterId = BigIntegerField(null=True)
    shopCostumeMasterId = BigIntegerField(null=True)
    illustCharacterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayAwakeningStatus = BooleanField(constraints=[SQL("DEFAULT false")])
    homeCharacterDisplayType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    loginBonusCharacterBaseMasterId = BigIntegerField(null=True)
    loginBonusCostumeMasterId = BigIntegerField(null=True)

    class Meta:
        table_name = "home_display_preference"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Character(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentExperience = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    talentStage = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    awakeningPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    senseLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    readEpisodeOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    releasedEpisodeOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayAwakeningStatus = BooleanField(constraints=[SQL("DEFAULT false")])
    secondaryCharacterBaseId = BigIntegerField(null=True)
    secondarySenseLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    selectionType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isFavorite = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "character"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterBase(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    starRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalStarPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    costumeMasterId = BigIntegerField(null=True)
    keyMissionLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    portalCharacterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    portalDisplayAwakeningStatus = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "character_base"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Party(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    leaderPosition = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "party"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PartySlot(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    partyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    position = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    posterId = BigIntegerField(null=True)
    accessoryId = BigIntegerField(null=True)
    bonusAbilityEnableFlags = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "party_slot"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    assetId = TextField(null=True)
    rarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    attribute = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    minLevelStatus = JSONField(null=True)
    starActMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    awakenStarActMasterId = BigIntegerField(null=True)
    senseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    forbidGenericItemBloom = BooleanField(constraints=[SQL("DEFAULT false")])
    bloomBonusGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    senseEnhanceItemGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    firstEpisodeReleaseItemGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    secondEpisodeReleaseItemGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterAwakeningItemGroupMasterId = BigIntegerField(null=True)
    displayStartAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayEndAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    unlockText = TextField(null=True)
    categories = JSONField(null=True)
    leaderSenseMasterId = BigIntegerField(null=True)
    maxTalentStage = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    maxTalentStageReleaseDate = BigIntegerField(null=True)
    secondaryCharacterBaseMasterId = BigIntegerField(null=True)
    secondarySenseMasterId = BigIntegerField(null=True)
    secondaryAttribute = BigIntegerField(null=True)

    class Meta:
        table_name = "character_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterBaseMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    school = TextField(null=True)
    grade = BigIntegerField(null=True)
    birthMonth = BigIntegerField(null=True)
    birthDay = BigIntegerField(null=True)
    height = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hobby = TextField(null=True)
    companyMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    nameRomanization = TextField(null=True)
    senseName = TextField(null=True)
    senseEffect = TextField(null=True)
    characterVoice = TextField(null=True)
    profileImageAssetId = TextField(null=True)
    age = BigIntegerField(null=True)
    familyNameRomanization = TextField(null=True)
    firstNameRomanization = TextField(null=True)
    pronounceFamilyName = TextField(null=True)
    pronounceFirstName = TextField(null=True)
    familyName = TextField(null=True)
    firstName = TextField(null=True)
    evoSenseName = TextField(null=True)
    evoSenseEffect = TextField(null=True)
    defaultCostumeMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseType = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_base_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterLevelMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    experienceToLevelUp = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterStatusLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    startDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_level_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Poster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    posterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    breakthroughPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    releasedEpisode = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    itemConsumeBreakThroughCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isFavorite = BooleanField(constraints=[SQL("DEFAULT false")])
    alternativeImagePattern = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "poster"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AccessoryLevelPatternGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    patterns = JSONField(null=True)

    class Meta:
        table_name = "accessory_level_pattern_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AccessoryLevelPatternMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    accessoryLevelPatternGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    requiredCoin = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    items = JSONField(null=True)

    class Meta:
        table_name = "accessory_level_pattern_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AccessoryMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    rarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    accessoryLevelPatternGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    fixedAccessoryEffects = JSONField(null=True)
    randomEffectGroups = JSONField(null=True)
    pronounceName = TextField(null=True)
    series = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    maxLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "accessory_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class EpisodeMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    title = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    episodeRewardPackageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    conditions = JSONField(null=True)
    preEpisodeMasterId = BigIntegerField(null=True)
    displayStartDate = BigIntegerField(null=True)
    displayEndDate = BigIntegerField(null=True)

    class Meta:
        table_name = "episode_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class EpisodeRewardPackageMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rewards = JSONField(null=True)

    class Meta:
        table_name = "episode_reward_package_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LiveMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    difficulty = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    noteCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    unlockCondition = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    unlockValue = BigIntegerField(null=True)
    startDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    endDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "live_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MusicMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    rewardRuleMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    pronounceName = TextField(null=True)
    lyricWriter = TextField(null=True)
    composer = TextField(null=True)
    arranger = TextField(null=True)
    unlockText = TextField(null=True)
    isLongVersion = BooleanField(constraints=[SQL("DEFAULT false")])
    releasedAt = BigIntegerField(null=True)
    staminaConsumption = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicTimeSecond = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    invisible = BooleanField(constraints=[SQL("DEFAULT false")])
    sampleStartSeconds = DoubleField(constraints=[SQL("DEFAULT 0")])
    sampleEndSeconds = DoubleField(constraints=[SQL("DEFAULT 0")])
    delaySeconds = DoubleField(constraints=[SQL("DEFAULT 0")])
    vocalVersions = JSONField(null=True)
    unlockConditionType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    unlockConditionValue = BigIntegerField(null=True)
    musicVideoType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicCoverType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventMasterId = BigIntegerField(null=True)
    storyMasterId = BigIntegerField(null=True)
    eventMasterId = BigIntegerField(null=True)

    class Meta:
        table_name = "music_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class SenseMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    type = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    preEffects = JSONField(null=True)
    branches = JSONField(null=True)
    acquirableGauge = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    acquirableScorePercent = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    scoreUpPerLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lightCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    coolTime = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    branchCondition1 = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    conditionValue1 = BigIntegerField(null=True)
    branchCondition2 = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    conditionValue2 = BigIntegerField(null=True)
    subTypes = JSONField(null=True)

    class Meta:
        table_name = "sense_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    type = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    companyMasterId = BigIntegerField(null=True)
    eventMasterId = BigIntegerField(null=True)
    chapterOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayStartAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayEndAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "story_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PosterLevelPatternGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    patterns = JSONField(null=True)

    class Meta:
        table_name = "poster_level_pattern_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PosterLevelPatternMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    levelPatternGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    itemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    quantity = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "poster_level_pattern_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PosterMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    organizeRestrictGroupId = BigIntegerField(null=True)
    rarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    levelPatternGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    subTitlePositionX1 = DoubleField(null=True)
    subTitlePositionY1 = DoubleField(null=True)
    subTitlePositionX2 = DoubleField(null=True)
    subTitlePositionY2 = DoubleField(null=True)
    subTitlePositionX3 = DoubleField(null=True)
    subTitlePositionY3 = DoubleField(null=True)
    releaseItemGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    pronounceName = TextField(null=True)
    costumes = JSONField(null=True)
    appearanceCharacterBaseMasterIds = JSONField(null=True)
    isRestrictItemBreakThrough = BooleanField(constraints=[SQL("DEFAULT false")])
    displayStartAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayEndAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    unlockText = TextField(null=True)
    orientation = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    subTitleDisplayCondition = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    subTitleDisplayConditionValue = BigIntegerField(null=True)
    posterBreakthroughMaxPhase = BigIntegerField(null=True)
    posterBreakthroughMaxPhaseReleaseDate = BigIntegerField(null=True)
    secondarySubTitleDisplayCondition = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    secondarySubTitleDisplayConditionValue = BigIntegerField(null=True)
    alternateImagePositionX1 = DoubleField(null=True)
    alternateImagePositionY1 = DoubleField(null=True)
    alternateImageReleasePhase1 = BigIntegerField(null=True)
    alternateImagePositionX2 = DoubleField(null=True)
    alternateImagePositionY2 = DoubleField(null=True)
    alternateImageReleasePhase2 = BigIntegerField(null=True)
    alternateImagePositionX3 = DoubleField(null=True)
    alternateImagePositionY3 = DoubleField(null=True)
    alternateImageReleasePhase3 = BigIntegerField(null=True)

    class Meta:
        table_name = "poster_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Live(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    liveMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    timesCompleted = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    achievementRate = DoubleField(constraints=[SQL("DEFAULT 0")])
    notationRate = DoubleField(constraints=[SQL("DEFAULT 0")])
    clearLamp = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    status = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rateGrade = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "live"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Music(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stellaReleased = BooleanField(constraints=[SQL("DEFAULT false")])
    vocalVersion = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    olivierReleaseStatus = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isPossession = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "music"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Accessory(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    accessoryMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    locked = BooleanField(constraints=[SQL("DEFAULT false")])
    accessoryEffects = JSONField(null=True)
    referenceCounting = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isFavorite = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "accessory"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Item(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    itemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stock = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "item"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AccessoryEffectMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    effectMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    variety = BigIntegerField(null=True)

    class Meta:
        table_name = "accessory_effect_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CompanyMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    companies = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField(null=True)
    isOther = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "company_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class EffectDurationGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    durations = JSONField(null=True)

    class Meta:
        table_name = "effect_duration_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class EffectMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    type = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    range = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    calculationType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    details = JSONField(null=True)
    conditions = JSONField(null=True)
    durationSecond = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    triggers = JSONField(null=True)
    fireTimingType = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "effect_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ItemMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    displayOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayEndDate = BigIntegerField(null=True)
    maxStock = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    category = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    consumable = BooleanField(constraints=[SQL("DEFAULT false")])
    jumpType = BigIntegerField(null=True)
    jumpTargetId = BigIntegerField(null=True)
    tabCategory = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "item_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class RandomEffectGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    accessoryEffects = JSONField(null=True)

    class Meta:
        table_name = "random_effect_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class RewardRuleMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    achivementRateRewards = JSONField(null=True)

    class Meta:
        table_name = "reward_rule_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class SenseEffectMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    effectMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "sense_effect_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TrophyGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    category = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "trophy_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TrophyMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    rarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trophyGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hidden = BooleanField(constraints=[SQL("DEFAULT false")])
    unlockText = TextField(null=True)

    class Meta:
        table_name = "trophy_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterLesson(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    setCharacters = JSONField(null=True)
    bestScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leaderPosition = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rewardReceivedHighScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_lesson"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class DailyLesson(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    timesLeft = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "daily_lesson"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Inbox(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    thingType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    thingId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    thingQuantity = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isTimeLimited = BooleanField(constraints=[SQL("DEFAULT false")])
    hasReceived = BooleanField(constraints=[SQL("DEFAULT false")])
    title = TextField(null=True)
    description = TextField(null=True)
    sentAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    receivedAt = BigIntegerField(null=True)
    receiveLimitAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    checked = BooleanField(
        constraints=[SQL("DEFAULT false")]
    )  # surfaced by CheckPackages

    class Meta:
        table_name = "inbox"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Bomb(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bombMasterIds = JSONField(null=True)

    class Meta:
        table_name = "bomb"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Costume(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    costumeMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "costume"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class NameColor(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    nameColorMasterIds = JSONField(null=True)

    class Meta:
        table_name = "name_color"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Nameplate(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    namePlateMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "nameplate"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Note(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    noteMasterIds = JSONField(null=True)

    class Meta:
        table_name = "note"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Stamp(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stampMasterIds = JSONField(null=True)
    favoriteStampMasterIds = JSONField(null=True)

    class Meta:
        table_name = "stamp"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Mission(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isCleared = BooleanField(constraints=[SQL("DEFAULT false")])
    isRewardReceived = BooleanField(constraints=[SQL("DEFAULT false")])
    missionCurrentCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    missionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentMissionStageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "mission"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AuditionMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    recommendedCompany = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    canSkip = BooleanField(constraints=[SQL("DEFAULT false")])
    senseNotationMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    maxPhase = TextField(null=True)
    displayStartAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayEndAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    vocalVersion = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    auditionGroupNumber = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    skipStartAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "audition_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class BombMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hidden = BooleanField(constraints=[SQL("DEFAULT false")])
    isDefault = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "bomb_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterStarRankMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    rank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    nextRankPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    requiredLessonScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    statusBonus = DoubleField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_star_rank_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterStarRankRewardGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rewards = JSONField(null=True)

    class Meta:
        table_name = "character_star_rank_reward_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CostumeMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isDefault = BooleanField(constraints=[SQL("DEFAULT false")])
    costumeGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField(null=True)

    class Meta:
        table_name = "costume_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class HomeCharacterVoiceMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    text = TextField(null=True)
    weight = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterVoicePeriodMasterId = BigIntegerField(null=True)
    isPlayerBirthDateVoice = BooleanField(constraints=[SQL("DEFAULT false")])
    voiceFileName1 = TextField(null=True)
    voiceFileName2 = TextField(null=True)
    voiceFileName3 = TextField(null=True)
    voiceFileName4 = TextField(null=True)
    voiceInterval1 = DoubleField(constraints=[SQL("DEFAULT 0")])
    voiceInterval2 = DoubleField(constraints=[SQL("DEFAULT 0")])
    voiceInterval3 = DoubleField(constraints=[SQL("DEFAULT 0")])
    mouthMotionId1 = TextField(null=True)
    mouthMotionId2 = TextField(null=True)
    mouthMotionId3 = TextField(null=True)
    mouthMotionId4 = TextField(null=True)
    bodyMotionId1 = TextField(null=True)
    bodyMotionId2 = TextField(null=True)
    bodyMotionId3 = TextField(null=True)
    bodyMotionId4 = TextField(null=True)

    class Meta:
        table_name = "home_character_voice_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class NameColorMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hidden = BooleanField(constraints=[SQL("DEFAULT false")])
    isDefault = BooleanField(constraints=[SQL("DEFAULT false")])
    unlockText = TextField(null=True)

    class Meta:
        table_name = "name_color_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class NameplateMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hidden = BooleanField(constraints=[SQL("DEFAULT false")])
    isDefault = BooleanField(constraints=[SQL("DEFAULT false")])
    details = JSONField(null=True)
    unlockText = TextField(null=True)
    changeType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    changeValue1 = BigIntegerField(null=True)
    changeValue2 = BigIntegerField(null=True)

    class Meta:
        table_name = "nameplate_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class NoteMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    description = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hidden = BooleanField(constraints=[SQL("DEFAULT false")])
    isDefault = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "note_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class SpotConversationMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    spot = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterId1 = BigIntegerField(null=True)
    characterId2 = BigIntegerField(null=True)
    characterId3 = BigIntegerField(null=True)
    characterId4 = BigIntegerField(null=True)
    characterId5 = BigIntegerField(null=True)
    episodeMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    costumeId1 = BigIntegerField(null=True)
    costumeId2 = BigIntegerField(null=True)
    costumeId3 = BigIntegerField(null=True)
    costumeId4 = BigIntegerField(null=True)
    costumeId5 = BigIntegerField(null=True)
    title = TextField(null=True)

    class Meta:
        table_name = "spot_conversation_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StampMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isDefault = BooleanField(constraints=[SQL("DEFAULT false")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    type = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    assetId = TextField(null=True)
    voiceAssetId = TextField(null=True)
    name = TextField(null=True)
    characterBaseMasterIds = JSONField(null=True)

    class Meta:
        table_name = "stamp_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterLessonSlot(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    position = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    setCharacterId = BigIntegerField(null=True)

    class Meta:
        table_name = "character_lesson_slot"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Trophy(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trophyMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trophyGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "trophy"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Market(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastRefreshedAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    refreshTimes = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "market"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ViewedShop(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    exchangeShopMasterId = BigIntegerField(null=True)
    lastViewedAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    viewedShopCategory = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "viewed_shop"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class GameHint(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    pageCategory = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hasAlreadyRead = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "game_hint"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class UserBonus(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    experienceBonus = DoubleField(constraints=[SQL("DEFAULT 0")])
    lessonStarRankBonus = DoubleField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "user_bonus"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AuditionPhaseMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    auditionasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    phase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    recommendedPlayerRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    starActCount = BigIntegerField(null=True)
    auditionRewardPackageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "audition_phase_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AuditionRewardPackageMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rewards = JSONField(null=True)

    class Meta:
        table_name = "audition_reward_package_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CampaignMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    title = TextField(null=True)
    description = TextField(null=True)
    iconImagePath = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    startDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    endDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    comebackCampaignMasterId = BigIntegerField(null=True)
    campaignEffectType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    campaignEffectValue = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "campaign_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterAwakeningItemMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    awakeningPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    itemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    requiredQuantity = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_awakening_item_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterBloomBonusGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bloomBonuses = JSONField(null=True)
    bloomRewards = JSONField(null=True)

    class Meta:
        table_name = "character_bloom_bonus_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterBloomItemMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    rarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentStage = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    requiredPieceAmount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    talentBloomItemType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    genericBloomItemMasterId = BigIntegerField(null=True)
    requiredItemMasterId = BigIntegerField(null=True)
    requiredItemAmount = BigIntegerField(null=True)

    class Meta:
        table_name = "character_bloom_item_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterExperienceItemMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    itemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    acquirableExperience = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    acquirableExperienceBonus = DoubleField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_experience_item_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterMissionMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    title = TextField(null=True)
    jumpType = BigIntegerField(null=True)
    jumpValue = BigIntegerField(null=True)
    stages = JSONField(null=True)

    class Meta:
        table_name = "character_mission_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterMissionStageMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterMissionCategoryLevelMasterId = BigIntegerField(
        constraints=[SQL("DEFAULT 0")]
    )
    characterMissionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    exclusionNoSenseCharacter = BooleanField(constraints=[SQL("DEFAULT false")])
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stageOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    goalCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_mission_stage_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterPieceMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    itemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    dugongRequiredAmount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    talentBloomItemType = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_piece_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterSenseEnhanceItemGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    items = JSONField(null=True)

    class Meta:
        table_name = "character_sense_enhance_item_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CostumeWearableCharacterGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterIds = JSONField(null=True)

    class Meta:
        table_name = "costume_wearable_character_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ExchangeShopMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isDisplayRequiredHavingItem = BooleanField(constraints=[SQL("DEFAULT false")])
    category = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    displayThingType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    displayItemMasterId = BigIntegerField(null=True)
    bannerPath = TextField(null=True)
    startDate = BigIntegerField(null=True)
    endDate = BigIntegerField(null=True)
    lastRefreshedAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lineup = JSONField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "exchange_shop_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LiveSettingMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    liveType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    liveDropFrameGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "live_setting_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MissionMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    missionCategory = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    missionViewOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    title = TextField(null=True)
    description = TextField(null=True)
    eventMasterId = BigIntegerField(null=True)
    jumpType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    jumpTargetId = BigIntegerField(null=True)
    startDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    endDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stages = JSONField(null=True)
    comebackCampaignMasterId = BigIntegerField(null=True)

    class Meta:
        table_name = "mission_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MusicVocalVersionMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    vocalVersion = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    singer = TextField(null=True)
    name = TextField(null=True)
    musicTimeSecond = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    sampleStartSeconds = DoubleField(constraints=[SQL("DEFAULT 0")])
    sampleEndSeconds = DoubleField(constraints=[SQL("DEFAULT 0")])
    musicVideoType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characters = JSONField(null=True)

    class Meta:
        table_name = "music_vocal_version_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PosterReleaseItemGroupMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    items = JSONField(null=True)
    itemConsumeApplyFlag = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "poster_release_item_group_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PosterReleaseItemMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    currentPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    itemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    requiredQuantity = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "poster_release_item_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PosterStoryMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    posterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    episodeType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(null=True)
    description = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterIconId = BigIntegerField(null=True)
    characterName = TextField(null=True)

    class Meta:
        table_name = "poster_story_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StarRankRewardMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    rank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterStarRankRewardGroupMasterId = BigIntegerField(
        constraints=[SQL("DEFAULT 0")]
    )

    class Meta:
        table_name = "star_rank_reward_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AuditionClear(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    auditionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    auditionClearPartyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    skipClearPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "audition_clear"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class SpRate(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    liveMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    point = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "sp_rate"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Notification(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    importantReadAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    updateReadAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bugReadAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "notification"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Episode(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    episodeMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hasReadAll = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "episode"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterMission(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterMissionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentStageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearedStageOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rewardReceivedStageOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    completedLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "character_mission"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MissionPass(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    missionPassMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    paid = BooleanField(constraints=[SQL("DEFAULT false")])
    freeRewardReceivedPhase = BigIntegerField(null=True)
    spRewardReceivedPhase = BigIntegerField(null=True)
    terminated = BooleanField(constraints=[SQL("DEFAULT false")])
    freeRewardLoopCount = BigIntegerField(null=True)
    freeRewardLoopReceivedPhase = BigIntegerField(null=True)
    paidRewardLoopCount = BigIntegerField(null=True)
    paidRewardLoopReceivedPhase = BigIntegerField(null=True)

    class Meta:
        table_name = "mission_pass"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MissionPassDetailMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    phase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    missionPassMasterId = BigIntegerField(null=True)
    clearPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    startDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    endDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rewards = JSONField(null=True)

    class Meta:
        table_name = "mission_pass_detail_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MissionPassMaster(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    itemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    startDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    endDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "mission_pass_master"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LeagueBasic(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    myProperty = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    starEnrollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    daiStarEnrollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentClassType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bestClassType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastJoinedLeagueSeasonMasterId = BigIntegerField(null=True)

    class Meta:
        table_name = "league_basic"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEvent(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAcquiredPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    acquiredPointUpdatedDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastRank = BigIntegerField(null=True)
    readTips = BooleanField(constraints=[SQL("DEFAULT false")])
    loginDays = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "story_event"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ExchangeLimit(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    exchangeShopThingId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    replaceType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    specifiedNumberOfDaysLimit = BigIntegerField(null=True)
    exchangedCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    until = BigIntegerField(null=True)

    class Meta:
        table_name = "exchange_limit"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LeagueGroup(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    leagueMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    classType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    classOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "league_group"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LeagueGroupMember(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    leagueGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leagueMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bestScore = BigIntegerField(null=True)

    class Meta:
        table_name = "league_group_member"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LeagueHistory(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    leagueMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    classType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    historyCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isSendedReward = BooleanField(constraints=[SQL("DEFAULT false")])
    isPlayed = BooleanField(constraints=[SQL("DEFAULT false")])
    classChangeType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    groupRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    globalRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    allClassGlobalRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "league_history"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class JewelShop(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    jewelShopItemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    purchaseCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalPurchaseCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rePurchaseDate = BigIntegerField(null=True)

    class Meta:
        table_name = "jewel_shop"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class DailyLimit(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    autoPlayTimes = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    dailyLessonTimes = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastRefreshedAt = BigIntegerField(null=True)
    musicCourseFreeChallengeTimes = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "daily_limit"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LeagueHighScoreParty(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leagueMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    highScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    classType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    difficulty = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leagueGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    slots = JSONField(null=True)
    userName = TextField(null=True)
    actingAbility = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leaderPosition = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "league_high_score_party"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LeagueHighScorePartySlot(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leagueHighScorePartyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    position = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    posterMasterId = BigIntegerField(null=True)
    posterLevel = BigIntegerField(null=True)
    posterBreakthroughPhase = BigIntegerField(null=True)
    accessoryMasterId = BigIntegerField(null=True)
    accessoryLevel = BigIntegerField(null=True)
    currentStatus = JSONField(null=True)
    characterTalentStage = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterAwakeningPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterDisplayAwakeningStatus = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "league_high_score_party_slot"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEventCircle(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    highScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    circleId = BigIntegerField(null=True)

    class Meta:
        table_name = "story_event_circle"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEventCircleMission(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventCircleMissionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "story_event_circle_mission"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEventCircleMissionReward(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventCircleMissionRewardMasterId = BigIntegerField(
        constraints=[SQL("DEFAULT 0")]
    )

    class Meta:
        table_name = "story_event_circle_mission_reward"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEventHighScoreBuffSetting(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    storyEventHighScoreBuffSettingMasterId = BigIntegerField(
        constraints=[SQL("DEFAULT 0")]
    )
    currentLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "story_event_high_score_buff_setting"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEventHighScoreParty(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    highScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rateGrade = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    difficulty = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    highScoreType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    liveSettingMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    slots = JSONField(null=True)
    leaderPosition = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "story_event_high_score_party"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEventHighScorePartySlot(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventHighScoreClearPartyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    position = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterTalentStage = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterAwakeningPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    posterMasterId = BigIntegerField(null=True)
    posterLevel = BigIntegerField(null=True)
    posterBreakthroughPhase = BigIntegerField(null=True)
    accessoryMasterId = BigIntegerField(null=True)
    accessoryLevel = BigIntegerField(null=True)
    currentStatus = JSONField(null=True)
    characterDisplayAwakeningStatus = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "story_event_high_score_party_slot"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ConnectWithAccount(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    provider = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "connect_with_account"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ConnectWithPassword(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "connect_with_password"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TournamentDetail(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    tournamentDetailMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bestUniqueScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    perfectStar = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    perfect = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    great = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    good = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bad = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    miss = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    recordedAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "tournament_detail"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class GradualMissionGroup(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    gradualMissionGroupMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    startAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "gradual_mission_group"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Photo(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    fileName = TextField(null=True)
    sasToken = TextField(null=True)
    photoEffectMasterId = BigIntegerField(null=True)
    lock = BooleanField(constraints=[SQL("DEFAULT false")])
    useAlbumPage = BigIntegerField(null=True)
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    signMasterId = BigIntegerField(null=True)
    generatedAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    thumbnailSasToken = TextField(null=True)
    appearedCharacterBaseMasterIds = JSONField(null=True)
    taggedCharacterBaseMasterIds = JSONField(null=True)
    useDecoPage = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "photo"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Album(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    level = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    publishPageNumber = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentPresetOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "album"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AlbumPage(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    page = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    editType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    publishing = BooleanField(constraints=[SQL("DEFAULT false")])
    items = JSONField(null=True)
    albumThemeMasterId = BigIntegerField(null=True)

    class Meta:
        table_name = "album_page"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StarPassStatus(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    type = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalPurchasedCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    validUntil = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "star_pass_status"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LoginPassStatus(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    validUntil = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "login_pass_status"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Currency(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    coin = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    freeJewel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    paidJewel = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "currency"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Decoration(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    decorationMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "decoration"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LiveAchievement(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    olivierReleasedCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    olivierClearedLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "live_achievement"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MusicVideo(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicVideoMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "music_video"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TheaterStory(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    theaterStoryMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "theater_story"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LiveDropCelling(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    multiLiveScheduleMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    count = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalCellingCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "live_drop_celling"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class StoryEventHighScore(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    storyEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentEnhancementPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAcquiredEnhancementPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "story_event_high_score"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Comic(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    comicEpisodeMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "comic"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ComebackCampaign(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    comebackCampaignMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    activatedAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "comeback_campaign"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class ConcertStage(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    concertStageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "concert_stage"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Limit(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    additionalAcquirablePhotoLimit = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    acquirablePhotoLimitIncreasedTimes = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    additionalAcquirableAccessoryLimit = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    acquirableAccessoryLimitIncreasedTimes = BigIntegerField(
        constraints=[SQL("DEFAULT 0")]
    )

    class Meta:
        table_name = "limit"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class GachaSelectedThing(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    gachaMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    gachaThingIds = JSONField(null=True)

    class Meta:
        table_name = "gacha_selected_thing"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TotalPointEvent(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalPointEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAcquiredPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    receivedRewardOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "total_point_event"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class EventBoxGacha(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    eventBoxGachaMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentBoxCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "event_box_gacha"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class EventBoxGachaBoxThing(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    eventBoxGachaBoxThingMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    hitCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "event_box_gacha_box_thing"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class SpecialEvent(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    specialEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    readTips = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "special_event"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CharacterPointEvent(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterPointEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(null=True)
    totalAcquiredPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    readTips = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "character_point_event"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AnotherNotation(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    anotherNotationMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearLamp = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rateGrade = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    achievementRatePercentRecord = JSONField(null=True)

    class Meta:
        table_name = "another_notation"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MusicBookmark(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    musicMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicBookmarkFlag = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "music_bookmark"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LiveDropLimit(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    multiLiveScheduleMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    countLimit = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "live_drop_limit"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Restriction(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    multiLiveRestrictionFinishedAt = BigIntegerField(null=True)
    readMultiLiveRestrictionDialog = BooleanField(null=True)

    class Meta:
        table_name = "restriction"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PermanentMarketThing(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    permanentMarketThingMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    purchaseCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "permanent_market_thing"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TimeLimitedControl(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    timeLimitedControlMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    expiredAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "time_limited_control"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class FlashSaleStage(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    flashSaleStageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    purchaseLimitedAt = BigIntegerField(null=True)
    isDefault = BooleanField(constraints=[SQL("DEFAULT false")])
    isCompleted = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "flash_sale_stage"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AlbumTheme(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    albumThemeMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "album_theme"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class CircleEventMission(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    circleEventMissionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isActive = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "circle_event_mission"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class PickupCharacterMission(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    pickupCharacterMissionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    receivedDetailMasterIds = JSONField(null=True)

    class Meta:
        table_name = "pickup_character_mission"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LeagueSeasonResult(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    leagueSeasonMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    daiStarMaxEnrollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "league_season_result"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Event(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    eventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAcquiredPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    acquiredPointUpdatedDate = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastRank = BigIntegerField(null=True)
    readTips = BooleanField(constraints=[SQL("DEFAULT false")])
    loginDays = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "event"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class BonusLive(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bonusLiveMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearedStageOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    readTips = BooleanField(constraints=[SQL("DEFAULT false")])
    dailyClearTimes = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "bonus_live"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class BonusLiveStage(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bonusLiveMasterStageId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearTimes = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "bonus_live_stage"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class RouletteEvent(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rouletteEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAcquiredPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "roulette_event"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Roulette(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rouletteMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "roulette"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class HomeBGM(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    homeBGMMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    selectionType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    homeBGMDetailMasterId = BigIntegerField(null=True)

    class Meta:
        table_name = "home_b_g_m"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class LinkCharacter(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    companyMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    linkedCharacterBaseMasterId = BigIntegerField(null=True)
    rewardReceivedMaxRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "link_character"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MusicCourse(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicCourseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearLamp = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    certificationGrade = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAchievementRatePercentRecord = JSONField(null=True)

    class Meta:
        table_name = "music_course"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TournamentQualifying(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    tournamentQualifyingMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicCourseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentChallengeCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    perfectStar = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    perfect = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    great = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    good = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bad = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    miss = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAchievementRatePercentRecord = JSONField(null=True)
    bestRecordChallengeCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bestRecordDate = BigIntegerField(null=True)

    class Meta:
        table_name = "tournament_qualifying"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Lottery(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    lotteryMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    results = JSONField(null=True)

    class Meta:
        table_name = "lottery"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastParty(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    leaderPosition = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "triple_cast_party"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastPartySlot(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    partyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    position = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    posterId = BigIntegerField(null=True)
    accessoryId = BigIntegerField(null=True)
    bonusAbilityEnableFlags = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "triple_cast_party_slot"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastBasic(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    starEnrollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    daiStarEnrollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentClassType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bestClassType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    lastJoinedTripleCastSeasonMasterId = BigIntegerField(null=True)
    partyOrder1 = BigIntegerField(null=True)
    partyOrder2 = BigIntegerField(null=True)
    partyOrder3 = BigIntegerField(null=True)

    class Meta:
        table_name = "triple_cast_basic"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastGroup(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    tripleCastMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    classType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    classOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "triple_cast_group"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastGroupMember(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    tripleCastGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    tripleCastMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bestScore = BigIntegerField(null=True)

    class Meta:
        table_name = "triple_cast_group_member"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastHighScoreParty(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    tripleCastMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    highScore = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    slots = JSONField(null=True)
    actingAbility = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leaderPosition = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    difficulty = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "triple_cast_high_score_party"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastHighScorePartySlot(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    tripleCastHighScorePartyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    position = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterLevel = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    posterMasterId = BigIntegerField(null=True)
    posterLevel = BigIntegerField(null=True)
    posterBreakthroughPhase = BigIntegerField(null=True)
    accessoryMasterId = BigIntegerField(null=True)
    accessoryLevel = BigIntegerField(null=True)
    currentStatus = JSONField(null=True)
    characterTalentStage = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterAwakeningPhase = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterDisplayAwakeningStatus = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "triple_cast_high_score_party_slot"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastSeasonResult(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    tripleCastSeasonMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    daiStarMaxEnrollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "triple_cast_season_result"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AlbumPreset(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    name = TextField(null=True)
    order = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "album_preset"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Gacha(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    gachaMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "gacha"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TripleCastHistory(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    tripleCastMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    classType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    historyCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isSendedReward = BooleanField(constraints=[SQL("DEFAULT false")])
    isPlayed = BooleanField(constraints=[SQL("DEFAULT false")])
    classChangeType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    groupRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    globalRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    allClassGlobalRank = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "triple_cast_history"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class DugongRun(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    clearedCourseIds = JSONField(null=True)
    noMistakeCourseIds = JSONField(null=True)
    dugongRunCourseGroupId = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "dugong_run"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MusicCourseRanking(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    musicCourseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentChallengeCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    perfectStar = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    perfect = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    great = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    good = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bad = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    miss = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalAchievementRatePercentRecord = JSONField(null=True)
    bestRecordChallengeCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    bestRecordDate = BigIntegerField(null=True)
    hasReceivedReward = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "music_course_ranking"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class FriendInvitation(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    invitationCode = TextField(null=True)
    hasInputOtherInvitationCode = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "friend_invitation"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class FriendInvitationMission(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    friendInvitationMissionMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    friendInvitationMissionStageMasterId = BigIntegerField(
        constraints=[SQL("DEFAULT 0")]
    )
    currentCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isCleared = BooleanField(constraints=[SQL("DEFAULT false")])
    isRewardReceived = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "friend_invitation_mission"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class NameBaseColor(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    nameBaseColorMasterIds = JSONField(null=True)

    class Meta:
        table_name = "name_base_color"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class IconFrame(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    iconFrameMasterIds = JSONField(null=True)

    class Meta:
        table_name = "icon_frame"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class GachaReRoll(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    gachaMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rollCount = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isDecided = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "gacha_re_roll"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TrialPartyEvent(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trialPartyEventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    currentStageOrder = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isCompleted = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "trial_party_event"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TrialPartyEventStage(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trialPartyEventStageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    isCleared = BooleanField(constraints=[SQL("DEFAULT false")])

    class Meta:
        table_name = "trial_party_event_stage"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TrialPartyEventStageParty(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trialPartyEventStageMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    leaderPosition = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "trial_party_event_stage_party"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class TrialPartyEventStagePartySlot(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trialPartyEventStagePartyId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    position = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trialPartyCharacterMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trialPartyPosterMasterId = BigIntegerField(null=True)
    trialPartyAccessoryMasterId = BigIntegerField(null=True)

    class Meta:
        table_name = "trial_party_event_stage_party_slot"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class UserBlock(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    blockUserId = TextField(null=True)

    class Meta:
        table_name = "user_block"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class Friend(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    friendUserId = BigIntegerField()
    isFavorite = BooleanField(constraints=[SQL("DEFAULT false")])
    createdAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "friend"
        indexes = ((("userId", "friendUserId"), True),)  # one row per direction
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class FriendRequest(BaseModel):
    rowId = AutoField()
    fromUserId = BigIntegerField(index=True)
    toUserId = BigIntegerField(index=True)
    createdAt = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "friend_request"
        indexes = ((("fromUserId", "toUserId"), True),)
        constraints = [
            SQL(
                'FOREIGN KEY ("fromUserId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


# reverse index: the client references users by their (string) hashUserId, so this maps
# it back to the sequential userId without recomputing unhash_id on every request
class HashUserId(BaseModel):
    hashUserId = TextField(primary_key=True)
    userId = BigIntegerField(unique=True, index=True)

    class Meta:
        table_name = "hash_user_id"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class HomeSkin(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    homeSkinMasterIds = JSONField(null=True)

    class Meta:
        table_name = "home_skin"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class AccessoryAutoSell(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    autoSellRarity = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "accessory_auto_sell"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class FavoriteCostume(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    characterBaseMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    favoriteCostumeMasterIds = JSONField(null=True)

    class Meta:
        table_name = "favorite_costume"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class BuffItemStatus(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    effectType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    buffItemMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    validUntil = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "buff_item_status"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class MultiRoomBasic(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    ownerMultiRoomId = TextField(null=True)

    class Meta:
        table_name = "multi_room_basic"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


class EventCamp(BaseModel):
    rowId = AutoField()
    userId = BigIntegerField(index=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    eventMasterId = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    campType = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    totalSupportPoint = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "event_camp"
        constraints = [
            SQL(
                'FOREIGN KEY ("userId") REFERENCES "accounts"("userId") ON DELETE CASCADE'
            )
        ]


db.connect()
db.execute_sql("CREATE SEQUENCE IF NOT EXISTS user_id_seq START 1")
db.create_tables([DatabaseInfo, Accounts], safe=True)
db.create_tables(
    [
        User,
        UserProfile,
        UserPreference,
        HomeDisplayPreference,
        Character,
        CharacterBase,
        Party,
        PartySlot,
        CharacterMaster,
        CharacterBaseMaster,
        CharacterLevelMaster,
        Poster,
        AccessoryLevelPatternGroupMaster,
        AccessoryLevelPatternMaster,
        AccessoryMaster,
        EpisodeMaster,
        EpisodeRewardPackageMaster,
        LiveMaster,
        MusicMaster,
        SenseMaster,
        StoryMaster,
        PosterLevelPatternGroupMaster,
        PosterLevelPatternMaster,
        PosterMaster,
        Live,
        Music,
        Accessory,
        Item,
        AccessoryEffectMaster,
        CompanyMaster,
        EffectDurationGroupMaster,
        EffectMaster,
        ItemMaster,
        RandomEffectGroupMaster,
        RewardRuleMaster,
        SenseEffectMaster,
        TrophyGroupMaster,
        TrophyMaster,
        CharacterLesson,
        DailyLesson,
        Inbox,
        Bomb,
        Costume,
        NameColor,
        Nameplate,
        Note,
        Stamp,
        Mission,
        AuditionMaster,
        BombMaster,
        CharacterStarRankMaster,
        CharacterStarRankRewardGroupMaster,
        CostumeMaster,
        HomeCharacterVoiceMaster,
        NameColorMaster,
        NameplateMaster,
        NoteMaster,
        SpotConversationMaster,
        StampMaster,
        CharacterLessonSlot,
        Trophy,
        Market,
        ViewedShop,
        GameHint,
        UserBonus,
        AuditionPhaseMaster,
        AuditionRewardPackageMaster,
        CampaignMaster,
        CharacterAwakeningItemMaster,
        CharacterBloomBonusGroupMaster,
        CharacterBloomItemMaster,
        CharacterExperienceItemMaster,
        CharacterMissionMaster,
        CharacterMissionStageMaster,
        CharacterPieceMaster,
        CharacterSenseEnhanceItemGroupMaster,
        CostumeWearableCharacterGroupMaster,
        ExchangeShopMaster,
        LiveSettingMaster,
        MissionMaster,
        MusicVocalVersionMaster,
        PosterReleaseItemGroupMaster,
        PosterReleaseItemMaster,
        PosterStoryMaster,
        StarRankRewardMaster,
        AuditionClear,
        SpRate,
        Notification,
        Episode,
        CharacterMission,
        MissionPass,
        MissionPassDetailMaster,
        MissionPassMaster,
        LeagueBasic,
        StoryEvent,
        ExchangeLimit,
        LeagueGroup,
        LeagueGroupMember,
        LeagueHistory,
        JewelShop,
        DailyLimit,
        LeagueHighScoreParty,
        LeagueHighScorePartySlot,
        StoryEventCircle,
        StoryEventCircleMission,
        StoryEventCircleMissionReward,
        StoryEventHighScoreBuffSetting,
        StoryEventHighScoreParty,
        StoryEventHighScorePartySlot,
        ConnectWithAccount,
        ConnectWithPassword,
        TournamentDetail,
        GradualMissionGroup,
        Photo,
        Album,
        AlbumPage,
        StarPassStatus,
        LoginPassStatus,
        Currency,
        Decoration,
        LiveAchievement,
        MusicVideo,
        TheaterStory,
        LiveDropCelling,
        StoryEventHighScore,
        Comic,
        ComebackCampaign,
        ConcertStage,
        Limit,
        GachaSelectedThing,
        TotalPointEvent,
        EventBoxGacha,
        EventBoxGachaBoxThing,
        SpecialEvent,
        CharacterPointEvent,
        AnotherNotation,
        MusicBookmark,
        LiveDropLimit,
        Restriction,
        PermanentMarketThing,
        TimeLimitedControl,
        FlashSaleStage,
        AlbumTheme,
        CircleEventMission,
        PickupCharacterMission,
        LeagueSeasonResult,
        Event,
        BonusLive,
        BonusLiveStage,
        RouletteEvent,
        Roulette,
        HomeBGM,
        LinkCharacter,
        MusicCourse,
        TournamentQualifying,
        Lottery,
        TripleCastParty,
        TripleCastPartySlot,
        TripleCastBasic,
        TripleCastGroup,
        TripleCastGroupMember,
        TripleCastHighScoreParty,
        TripleCastHighScorePartySlot,
        TripleCastSeasonResult,
        AlbumPreset,
        Gacha,
        TripleCastHistory,
        DugongRun,
        MusicCourseRanking,
        FriendInvitation,
        FriendInvitationMission,
        NameBaseColor,
        IconFrame,
        GachaReRoll,
        TrialPartyEvent,
        TrialPartyEventStage,
        TrialPartyEventStageParty,
        TrialPartyEventStagePartySlot,
        UserBlock,
        Friend,
        FriendRequest,
        HomeSkin,
        AccessoryAutoSell,
        FavoriteCostume,
        BuffItemStatus,
        MultiRoomBasic,
        EventCamp,
        HashUserId,
    ],
    safe=True,
)
if not DatabaseInfo.select().exists():
    DatabaseInfo.create(version=version)
db.close()
print("Complete!")
