from db.query import ExecutableQuery


def update_user_tutorial_status(user_id: int, status: int) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "user" SET "tutorialStatus" = $2 WHERE "userId" = $1',
        user_id,
        status,
    )


def upsert_user(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "playerRank",
        "currentRankPoint",
        "currentStamina",
        "maxStaminaRestoredAt",
        "paidJewel",
        "freeJewel",
        "coin",
        "playerRankLimit",
        "staminaRecoverTimesWithJewel",
        "circleUsageRestrictionsEndTime",
        "circleId",
        "gameStartAt",
        "hashUserId",
        "banLevel",
        "tutorialStatus",
        "monthlyPayment",
        "splashLastDisplayedAt",
        "isCapedPlayerRank",
        "requireCapedPlayerRankAnnounce",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "user" ("userId", "id", "playerRank", "currentRankPoint", "currentStamina", "maxStaminaRestoredAt", "paidJewel", "freeJewel", "coin", "playerRankLimit", "staminaRecoverTimesWithJewel", "circleUsageRestrictionsEndTime", "circleId", "gameStartAt", "hashUserId", "banLevel", "tutorialStatus", "monthlyPayment", "splashLastDisplayedAt", "isCapedPlayerRank", "requireCapedPlayerRankAnnounce") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21)',
        *vals,
    )


def upsert_user_profile(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "introduction",
        "mainUCharacterId",
        "mNameplateId",
        "mNameColorId",
        "mTrophyId1",
        "mTrophyId2",
        "mTrophyId3",
        "playerRate",
        "isPublicPlayerRate",
        "leagueClass",
        "totalSpCount",
        "isPublicAlbumMainPage",
        "mNameplateDetailId",
        "mainCharacterMasterId",
        "displayAwakeningStatus",
        "isPublicActivityLog",
        "nameBaseColorMasterId",
        "iconFrameMasterId",
        "homeSkinMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "user_profile" ("userId", "id", "name", "introduction", "mainUCharacterId", "mNameplateId", "mNameColorId", "mTrophyId1", "mTrophyId2", "mTrophyId3", "playerRate", "isPublicPlayerRate", "leagueClass", "totalSpCount", "isPublicAlbumMainPage", "mNameplateDetailId", "mainCharacterMasterId", "displayAwakeningStatus", "isPublicActivityLog", "nameBaseColorMasterId", "iconFrameMasterId", "homeSkinMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22)',
        *vals,
    )


def upsert_user_preference(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "multiPartyId", "birthDate"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "user_preference" ("userId", "id", "multiPartyId", "birthDate") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_home_display_preference(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "homeCharacterBaseMasterId",
        "memberCharacterBaseMasterId",
        "storyCharacterBaseMasterId",
        "shopCharacterBaseMasterId",
        "homeCostumeMasterId",
        "memberCostumeMasterId",
        "storyCostumeMasterId",
        "shopCostumeMasterId",
        "illustCharacterMasterId",
        "displayAwakeningStatus",
        "homeCharacterDisplayType",
        "loginBonusCharacterBaseMasterId",
        "loginBonusCostumeMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "home_display_preference" ("userId", "id", "homeCharacterBaseMasterId", "memberCharacterBaseMasterId", "storyCharacterBaseMasterId", "shopCharacterBaseMasterId", "homeCostumeMasterId", "memberCostumeMasterId", "storyCostumeMasterId", "shopCostumeMasterId", "illustCharacterMasterId", "displayAwakeningStatus", "homeCharacterDisplayType", "loginBonusCharacterBaseMasterId", "loginBonusCostumeMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)',
        *vals,
    )


def upsert_character(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterMasterId",
        "level",
        "currentExperience",
        "talentStage",
        "awakeningPhase",
        "characterBaseId",
        "senseLevel",
        "readEpisodeOrder",
        "releasedEpisodeOrder",
        "displayAwakeningStatus",
        "secondaryCharacterBaseId",
        "secondarySenseLevel",
        "selectionType",
        "isFavorite",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character" ("userId", "id", "characterMasterId", "level", "currentExperience", "talentStage", "awakeningPhase", "characterBaseId", "senseLevel", "readEpisodeOrder", "releasedEpisodeOrder", "displayAwakeningStatus", "secondaryCharacterBaseId", "secondarySenseLevel", "selectionType", "isFavorite") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)',
        *vals,
    )


def upsert_character_base(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterBaseMasterId",
        "starRank",
        "totalStarPoint",
        "costumeMasterId",
        "keyMissionLevel",
        "portalCharacterId",
        "portalDisplayAwakeningStatus",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_base" ("userId", "id", "characterBaseMasterId", "starRank", "totalStarPoint", "costumeMasterId", "keyMissionLevel", "portalCharacterId", "portalDisplayAwakeningStatus") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        *vals,
    )


def upsert_party(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "order", "name", "leaderPosition"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "party" ("userId", "id", "order", "name", "leaderPosition") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_party_slot(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "partyId",
        "position",
        "characterId",
        "posterId",
        "accessoryId",
        "bonusAbilityEnableFlags",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "party_slot" ("userId", "id", "partyId", "position", "characterId", "posterId", "accessoryId", "bonusAbilityEnableFlags") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_character_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterBaseMasterId",
        "name",
        "description",
        "assetId",
        "rarity",
        "attribute",
        "minLevelStatus",
        "starActMasterId",
        "awakenStarActMasterId",
        "senseMasterId",
        "forbidGenericItemBloom",
        "bloomBonusGroupMasterId",
        "senseEnhanceItemGroupMasterId",
        "firstEpisodeReleaseItemGroupId",
        "secondEpisodeReleaseItemGroupId",
        "characterAwakeningItemGroupMasterId",
        "displayStartAt",
        "displayEndAt",
        "unlockText",
        "categories",
        "leaderSenseMasterId",
        "maxTalentStage",
        "maxTalentStageReleaseDate",
        "secondaryCharacterBaseMasterId",
        "secondarySenseMasterId",
        "secondaryAttribute",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_master" ("userId", "id", "characterBaseMasterId", "name", "description", "assetId", "rarity", "attribute", "minLevelStatus", "starActMasterId", "awakenStarActMasterId", "senseMasterId", "forbidGenericItemBloom", "bloomBonusGroupMasterId", "senseEnhanceItemGroupMasterId", "firstEpisodeReleaseItemGroupId", "secondEpisodeReleaseItemGroupId", "characterAwakeningItemGroupMasterId", "displayStartAt", "displayEndAt", "unlockText", "categories", "leaderSenseMasterId", "maxTalentStage", "maxTalentStageReleaseDate", "secondaryCharacterBaseMasterId", "secondarySenseMasterId", "secondaryAttribute") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28)',
        *vals,
    )


def upsert_character_base_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "description",
        "school",
        "grade",
        "birthMonth",
        "birthDay",
        "height",
        "hobby",
        "companyMasterId",
        "nameRomanization",
        "senseName",
        "senseEffect",
        "characterVoice",
        "profileImageAssetId",
        "age",
        "familyNameRomanization",
        "firstNameRomanization",
        "pronounceFamilyName",
        "pronounceFirstName",
        "familyName",
        "firstName",
        "evoSenseName",
        "evoSenseEffect",
        "defaultCostumeMasterId",
        "characterBaseType",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_base_master" ("userId", "id", "name", "description", "school", "grade", "birthMonth", "birthDay", "height", "hobby", "companyMasterId", "nameRomanization", "senseName", "senseEffect", "characterVoice", "profileImageAssetId", "age", "familyNameRomanization", "firstNameRomanization", "pronounceFamilyName", "pronounceFirstName", "familyName", "firstName", "evoSenseName", "evoSenseEffect", "defaultCostumeMasterId", "characterBaseType") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27)',
        *vals,
    )


def upsert_character_level_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["level", "experienceToLevelUp", "characterStatusLevel", "startDate"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_level_master" ("userId", "level", "experienceToLevelUp", "characterStatusLevel", "startDate") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_poster(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "posterMasterId",
        "level",
        "breakthroughPhase",
        "releasedEpisode",
        "itemConsumeBreakThroughCount",
        "isFavorite",
        "alternativeImagePattern",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "poster" ("userId", "id", "posterMasterId", "level", "breakthroughPhase", "releasedEpisode", "itemConsumeBreakThroughCount", "isFavorite", "alternativeImagePattern") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        *vals,
    )


def upsert_accessory_level_pattern_group_master(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["id", "patterns"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "accessory_level_pattern_group_master" ("userId", "id", "patterns") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_accessory_level_pattern_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "accessoryLevelPatternGroupMasterId",
        "level",
        "requiredCoin",
        "items",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "accessory_level_pattern_master" ("userId", "id", "accessoryLevelPatternGroupMasterId", "level", "requiredCoin", "items") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_accessory_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "description",
        "rarity",
        "accessoryLevelPatternGroupId",
        "fixedAccessoryEffects",
        "randomEffectGroups",
        "pronounceName",
        "series",
        "maxLevel",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "accessory_master" ("userId", "id", "name", "description", "rarity", "accessoryLevelPatternGroupId", "fixedAccessoryEffects", "randomEffectGroups", "pronounceName", "series", "maxLevel") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)',
        *vals,
    )


def upsert_episode_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "storyMasterId",
        "title",
        "order",
        "episodeRewardPackageMasterId",
        "conditions",
        "preEpisodeMasterId",
        "displayStartDate",
        "displayEndDate",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "episode_master" ("userId", "id", "storyMasterId", "title", "order", "episodeRewardPackageMasterId", "conditions", "preEpisodeMasterId", "displayStartDate", "displayEndDate") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_episode_reward_package_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "rewards"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "episode_reward_package_master" ("userId", "id", "rewards") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_live_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "difficulty",
        "musicMasterId",
        "level",
        "noteCount",
        "unlockCondition",
        "unlockValue",
        "startDate",
        "endDate",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "live_master" ("userId", "id", "difficulty", "musicMasterId", "level", "noteCount", "unlockCondition", "unlockValue", "startDate", "endDate") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_music_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "description",
        "rewardRuleMasterId",
        "pronounceName",
        "lyricWriter",
        "composer",
        "arranger",
        "unlockText",
        "isLongVersion",
        "releasedAt",
        "staminaConsumption",
        "musicTimeSecond",
        "invisible",
        "sampleStartSeconds",
        "sampleEndSeconds",
        "delaySeconds",
        "vocalVersions",
        "unlockConditionType",
        "unlockConditionValue",
        "musicVideoType",
        "musicCoverType",
        "storyEventMasterId",
        "storyMasterId",
        "eventMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "music_master" ("userId", "id", "name", "description", "rewardRuleMasterId", "pronounceName", "lyricWriter", "composer", "arranger", "unlockText", "isLongVersion", "releasedAt", "staminaConsumption", "musicTimeSecond", "invisible", "sampleStartSeconds", "sampleEndSeconds", "delaySeconds", "vocalVersions", "unlockConditionType", "unlockConditionValue", "musicVideoType", "musicCoverType", "storyEventMasterId", "storyMasterId", "eventMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26)',
        *vals,
    )


def upsert_sense_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "description",
        "type",
        "preEffects",
        "branches",
        "acquirableGauge",
        "acquirableScorePercent",
        "scoreUpPerLevel",
        "lightCount",
        "coolTime",
        "branchCondition1",
        "conditionValue1",
        "branchCondition2",
        "conditionValue2",
        "subTypes",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "sense_master" ("userId", "id", "name", "description", "type", "preEffects", "branches", "acquirableGauge", "acquirableScorePercent", "scoreUpPerLevel", "lightCount", "coolTime", "branchCondition1", "conditionValue1", "branchCondition2", "conditionValue2", "subTypes") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)',
        *vals,
    )


def upsert_story_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "type",
        "companyMasterId",
        "eventMasterId",
        "chapterOrder",
        "displayStartAt",
        "displayEndAt",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_master" ("userId", "id", "type", "companyMasterId", "eventMasterId", "chapterOrder", "displayStartAt", "displayEndAt") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_poster_level_pattern_group_master(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["id", "patterns"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "poster_level_pattern_group_master" ("userId", "id", "patterns") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_poster_level_pattern_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "levelPatternGroupId", "level", "itemMasterId", "quantity"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "poster_level_pattern_master" ("userId", "id", "levelPatternGroupId", "level", "itemMasterId", "quantity") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_poster_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "organizeRestrictGroupId",
        "rarity",
        "levelPatternGroupMasterId",
        "subTitlePositionX1",
        "subTitlePositionY1",
        "subTitlePositionX2",
        "subTitlePositionY2",
        "subTitlePositionX3",
        "subTitlePositionY3",
        "releaseItemGroupId",
        "pronounceName",
        "costumes",
        "appearanceCharacterBaseMasterIds",
        "isRestrictItemBreakThrough",
        "displayStartAt",
        "displayEndAt",
        "unlockText",
        "orientation",
        "subTitleDisplayCondition",
        "subTitleDisplayConditionValue",
        "posterBreakthroughMaxPhase",
        "posterBreakthroughMaxPhaseReleaseDate",
        "secondarySubTitleDisplayCondition",
        "secondarySubTitleDisplayConditionValue",
        "alternateImagePositionX1",
        "alternateImagePositionY1",
        "alternateImageReleasePhase1",
        "alternateImagePositionX2",
        "alternateImagePositionY2",
        "alternateImageReleasePhase2",
        "alternateImagePositionX3",
        "alternateImagePositionY3",
        "alternateImageReleasePhase3",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "poster_master" ("userId", "id", "name", "organizeRestrictGroupId", "rarity", "levelPatternGroupMasterId", "subTitlePositionX1", "subTitlePositionY1", "subTitlePositionX2", "subTitlePositionY2", "subTitlePositionX3", "subTitlePositionY3", "releaseItemGroupId", "pronounceName", "costumes", "appearanceCharacterBaseMasterIds", "isRestrictItemBreakThrough", "displayStartAt", "displayEndAt", "unlockText", "orientation", "subTitleDisplayCondition", "subTitleDisplayConditionValue", "posterBreakthroughMaxPhase", "posterBreakthroughMaxPhaseReleaseDate", "secondarySubTitleDisplayCondition", "secondarySubTitleDisplayConditionValue", "alternateImagePositionX1", "alternateImagePositionY1", "alternateImageReleasePhase1", "alternateImagePositionX2", "alternateImagePositionY2", "alternateImageReleasePhase2", "alternateImagePositionX3", "alternateImagePositionY3", "alternateImageReleasePhase3") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36)',
        *vals,
    )


def upsert_live(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "liveMasterId",
        "timesCompleted",
        "achievementRate",
        "notationRate",
        "clearLamp",
        "status",
        "rateGrade",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "live" ("userId", "id", "liveMasterId", "timesCompleted", "achievementRate", "notationRate", "clearLamp", "status", "rateGrade") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        *vals,
    )


def upsert_music(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "musicMasterId",
        "stellaReleased",
        "vocalVersion",
        "olivierReleaseStatus",
        "isPossession",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "music" ("userId", "id", "musicMasterId", "stellaReleased", "vocalVersion", "olivierReleaseStatus", "isPossession") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_accessory(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "accessoryMasterId",
        "level",
        "locked",
        "accessoryEffects",
        "referenceCounting",
        "isFavorite",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "accessory" ("userId", "id", "accessoryMasterId", "level", "locked", "accessoryEffects", "referenceCounting", "isFavorite") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_item(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "itemMasterId", "stock"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "item" ("userId", "id", "itemMasterId", "stock") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def increment_item_stock(
    user_id: int, item_master_id: int, delta: int
) -> ExecutableQuery:
    """Add ``delta`` to the caller's stock of an item, creating the row if new (id = master id)."""
    return ExecutableQuery(
        "WITH upd AS ("
        '  UPDATE "item" SET "stock" = "stock" + $3 '
        '  WHERE "userId" = $1 AND "itemMasterId" = $2 RETURNING 1'
        ") "
        'INSERT INTO "item" ("userId", "id", "itemMasterId", "stock") '
        "SELECT $1, $2, $2, $3 WHERE NOT EXISTS (SELECT 1 FROM upd)",
        user_id,
        item_master_id,
        delta,
    )


def add_currency(user_id: int, coin: int = 0, free_jewel: int = 0) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "currency" SET "coin" = "coin" + $2, "freeJewel" = "freeJewel" + $3 '
        'WHERE "userId" = $1',
        user_id,
        coin,
        free_jewel,
    )


def mark_inboxs_checked(user_id: int) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "inbox" SET "checked" = true WHERE "userId" = $1 AND "checked" = false',
        user_id,
    )


def create_inbox(
    user_id: int,
    inbox_id: int,
    thing_type: int,
    thing_id: int,
    quantity: int,
    description,
    sent_at: int,
    receive_limit_at: int,
) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "inbox" ("userId", "id", "thingType", "thingId", "thingQuantity", '
        '"isTimeLimited", "hasReceived", "description", "sentAt", "receiveLimitAt") '
        "VALUES ($1, $2, $3, $4, $5, true, false, $6, $7, $8)",
        user_id,
        inbox_id,
        thing_type,
        thing_id,
        quantity,
        description,
        sent_at,
        receive_limit_at,
    )


def upsert_accessory_effect_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "effectMasterId", "name", "description", "variety"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "accessory_effect_master" ("userId", "id", "effectMasterId", "name", "description", "variety") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_company_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "name", "companies", "description", "isOther"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "company_master" ("userId", "id", "name", "companies", "description", "isOther") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_effect_duration_group_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "durations"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "effect_duration_group_master" ("userId", "id", "durations") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_effect_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "type",
        "range",
        "calculationType",
        "details",
        "conditions",
        "durationSecond",
        "triggers",
        "fireTimingType",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "effect_master" ("userId", "id", "type", "range", "calculationType", "details", "conditions", "durationSecond", "triggers", "fireTimingType") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_item_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "description",
        "displayOrder",
        "displayEndDate",
        "maxStock",
        "category",
        "consumable",
        "jumpType",
        "jumpTargetId",
        "tabCategory",
        "rarity",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "item_master" ("userId", "id", "name", "description", "displayOrder", "displayEndDate", "maxStock", "category", "consumable", "jumpType", "jumpTargetId", "tabCategory", "rarity") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)',
        *vals,
    )


def upsert_random_effect_group_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "accessoryEffects"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "random_effect_group_master" ("userId", "id", "accessoryEffects") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_reward_rule_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "achivementRateRewards"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "reward_rule_master" ("userId", "id", "achivementRateRewards") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_sense_effect_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["order", "effectMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "sense_effect_master" ("userId", "order", "effectMasterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_trophy_group_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "category"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "trophy_group_master" ("userId", "id", "category") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_trophy_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "description",
        "rarity",
        "order",
        "trophyGroupMasterId",
        "hidden",
        "unlockText",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "trophy_master" ("userId", "id", "name", "description", "rarity", "order", "trophyGroupMasterId", "hidden", "unlockText") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        *vals,
    )


def upsert_character_lesson(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "characterBaseMasterId",
        "setCharacters",
        "bestScore",
        "leaderPosition",
        "rewardReceivedHighScore",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_lesson" ("userId", "characterBaseMasterId", "setCharacters", "bestScore", "leaderPosition", "rewardReceivedHighScore") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_daily_lesson(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["timesLeft"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "daily_lesson" ("userId", "timesLeft") VALUES ($1, $2)',
        *vals,
    )


def upsert_inbox(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "thingType",
        "thingId",
        "thingQuantity",
        "isTimeLimited",
        "hasReceived",
        "title",
        "description",
        "sentAt",
        "receivedAt",
        "receiveLimitAt",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "inbox" ("userId", "id", "thingType", "thingId", "thingQuantity", "isTimeLimited", "hasReceived", "title", "description", "sentAt", "receivedAt", "receiveLimitAt") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)',
        *vals,
    )


def upsert_bomb(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "bombMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "bomb" ("userId", "id", "bombMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_costume(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "costumeMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "costume" ("userId", "id", "costumeMasterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_name_color(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "nameColorMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "name_color" ("userId", "id", "nameColorMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_nameplate(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "namePlateMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "nameplate" ("userId", "id", "namePlateMasterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_note(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "noteMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "note" ("userId", "id", "noteMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_stamp(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "stampMasterIds", "favoriteStampMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "stamp" ("userId", "id", "stampMasterIds", "favoriteStampMasterIds") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_mission(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "isCleared",
        "isRewardReceived",
        "missionCurrentCount",
        "missionMasterId",
        "currentMissionStageMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "mission" ("userId", "id", "isCleared", "isRewardReceived", "missionCurrentCount", "missionMasterId", "currentMissionStageMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_audition_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "musicMasterId",
        "recommendedCompany",
        "canSkip",
        "senseNotationMasterId",
        "maxPhase",
        "displayStartAt",
        "displayEndAt",
        "vocalVersion",
        "auditionGroupNumber",
        "skipStartAt",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "audition_master" ("userId", "id", "musicMasterId", "recommendedCompany", "canSkip", "senseNotationMasterId", "maxPhase", "displayStartAt", "displayEndAt", "vocalVersion", "auditionGroupNumber", "skipStartAt") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)',
        *vals,
    )


def upsert_bomb_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "name", "description", "order", "hidden", "isDefault"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "bomb_master" ("userId", "id", "name", "description", "order", "hidden", "isDefault") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_character_star_rank_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["rank", "nextRankPoint", "requiredLessonScore", "statusBonus"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_star_rank_master" ("userId", "rank", "nextRankPoint", "requiredLessonScore", "statusBonus") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_character_star_rank_reward_group_master(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["id", "rewards"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_star_rank_reward_group_master" ("userId", "id", "rewards") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_costume_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "name", "order", "isDefault", "costumeGroupMasterId", "description"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "costume_master" ("userId", "id", "name", "order", "isDefault", "costumeGroupMasterId", "description") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_home_character_voice_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterBaseMasterId",
        "text",
        "weight",
        "characterVoicePeriodMasterId",
        "isPlayerBirthDateVoice",
        "voiceFileName1",
        "voiceFileName2",
        "voiceFileName3",
        "voiceFileName4",
        "voiceInterval1",
        "voiceInterval2",
        "voiceInterval3",
        "mouthMotionId1",
        "mouthMotionId2",
        "mouthMotionId3",
        "mouthMotionId4",
        "bodyMotionId1",
        "bodyMotionId2",
        "bodyMotionId3",
        "bodyMotionId4",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "home_character_voice_master" ("userId", "id", "characterBaseMasterId", "text", "weight", "characterVoicePeriodMasterId", "isPlayerBirthDateVoice", "voiceFileName1", "voiceFileName2", "voiceFileName3", "voiceFileName4", "voiceInterval1", "voiceInterval2", "voiceInterval3", "mouthMotionId1", "mouthMotionId2", "mouthMotionId3", "mouthMotionId4", "bodyMotionId1", "bodyMotionId2", "bodyMotionId3", "bodyMotionId4") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22)',
        *vals,
    )


def upsert_name_color_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "name", "description", "order", "hidden", "isDefault", "unlockText"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "name_color_master" ("userId", "id", "name", "description", "order", "hidden", "isDefault", "unlockText") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_nameplate_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "name",
        "description",
        "order",
        "hidden",
        "isDefault",
        "details",
        "unlockText",
        "changeType",
        "changeValue1",
        "changeValue2",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "nameplate_master" ("userId", "id", "name", "description", "order", "hidden", "isDefault", "details", "unlockText", "changeType", "changeValue1", "changeValue2") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)',
        *vals,
    )


def upsert_note_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "name", "description", "order", "hidden", "isDefault"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "note_master" ("userId", "id", "name", "description", "order", "hidden", "isDefault") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_spot_conversation_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "spot",
        "characterId1",
        "characterId2",
        "characterId3",
        "characterId4",
        "characterId5",
        "episodeMasterId",
        "costumeId1",
        "costumeId2",
        "costumeId3",
        "costumeId4",
        "costumeId5",
        "title",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "spot_conversation_master" ("userId", "id", "spot", "characterId1", "characterId2", "characterId3", "characterId4", "characterId5", "episodeMasterId", "costumeId1", "costumeId2", "costumeId3", "costumeId4", "costumeId5", "title") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)',
        *vals,
    )


def upsert_stamp_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "order",
        "isDefault",
        "characterBaseMasterId",
        "type",
        "assetId",
        "voiceAssetId",
        "name",
        "characterBaseMasterIds",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "stamp_master" ("userId", "id", "order", "isDefault", "characterBaseMasterId", "type", "assetId", "voiceAssetId", "name", "characterBaseMasterIds") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_character_lesson_slot(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["position", "setCharacterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_lesson_slot" ("userId", "position", "setCharacterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_trophy(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "trophyMasterId", "trophyGroupMasterId", "currentOrder"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "trophy" ("userId", "id", "trophyMasterId", "trophyGroupMasterId", "currentOrder") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_market(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "lastRefreshedAt", "refreshTimes"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "market" ("userId", "id", "lastRefreshedAt", "refreshTimes") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_viewed_shop(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "exchangeShopMasterId", "lastViewedAt", "viewedShopCategory"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "viewed_shop" ("userId", "id", "exchangeShopMasterId", "lastViewedAt", "viewedShopCategory") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_game_hint(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "pageCategory", "hasAlreadyRead"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "game_hint" ("userId", "id", "pageCategory", "hasAlreadyRead") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def mark_game_hint_read(user_id: int, page_category: int) -> ExecutableQuery:
    """Idempotently mark a page category's hint read (id = the category)."""
    return ExecutableQuery(
        "WITH upd AS ("
        '  UPDATE "game_hint" SET "hasAlreadyRead" = true '
        '  WHERE "userId" = $1 AND "pageCategory" = $2 RETURNING 1'
        ") "
        'INSERT INTO "game_hint" ("userId", "id", "pageCategory", "hasAlreadyRead") '
        "SELECT $1, $2, $2, true WHERE NOT EXISTS (SELECT 1 FROM upd)",
        user_id,
        page_category,
    )


def upsert_user_bonus(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "experienceBonus", "lessonStarRankBonus"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "user_bonus" ("userId", "id", "experienceBonus", "lessonStarRankBonus") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_audition_phase_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "auditionasterId",
        "phase",
        "recommendedPlayerRank",
        "clearScore",
        "starActCount",
        "auditionRewardPackageMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "audition_phase_master" ("userId", "id", "auditionasterId", "phase", "recommendedPlayerRank", "clearScore", "starActCount", "auditionRewardPackageMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_audition_reward_package_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "rewards"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "audition_reward_package_master" ("userId", "id", "rewards") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_campaign_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "title",
        "description",
        "iconImagePath",
        "order",
        "startDate",
        "endDate",
        "comebackCampaignMasterId",
        "campaignEffectType",
        "campaignEffectValue",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "campaign_master" ("userId", "id", "title", "description", "iconImagePath", "order", "startDate", "endDate", "comebackCampaignMasterId", "campaignEffectType", "campaignEffectValue") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)',
        *vals,
    )


def upsert_character_awakening_item_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "awakeningPhase", "itemMasterId", "requiredQuantity"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_awakening_item_master" ("userId", "id", "awakeningPhase", "itemMasterId", "requiredQuantity") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_character_bloom_bonus_group_master(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["id", "bloomBonuses", "bloomRewards"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_bloom_bonus_group_master" ("userId", "id", "bloomBonuses", "bloomRewards") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_character_bloom_item_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "rarity",
        "currentStage",
        "requiredPieceAmount",
        "talentBloomItemType",
        "genericBloomItemMasterId",
        "requiredItemMasterId",
        "requiredItemAmount",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_bloom_item_master" ("userId", "rarity", "currentStage", "requiredPieceAmount", "talentBloomItemType", "genericBloomItemMasterId", "requiredItemMasterId", "requiredItemAmount") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_character_experience_item_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "itemMasterId", "acquirableExperience", "acquirableExperienceBonus"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_experience_item_master" ("userId", "id", "itemMasterId", "acquirableExperience", "acquirableExperienceBonus") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_character_mission_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "title", "jumpType", "jumpValue", "stages"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_mission_master" ("userId", "id", "title", "jumpType", "jumpValue", "stages") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_character_mission_stage_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterMissionCategoryLevelMasterId",
        "characterMissionMasterId",
        "exclusionNoSenseCharacter",
        "order",
        "stageOrder",
        "goalCount",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_mission_stage_master" ("userId", "id", "characterMissionCategoryLevelMasterId", "characterMissionMasterId", "exclusionNoSenseCharacter", "order", "stageOrder", "goalCount") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_character_piece_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "itemMasterId",
        "characterMasterId",
        "dugongRequiredAmount",
        "talentBloomItemType",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_piece_master" ("userId", "itemMasterId", "characterMasterId", "dugongRequiredAmount", "talentBloomItemType") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_character_sense_enhance_item_group_master(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["id", "items"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_sense_enhance_item_group_master" ("userId", "id", "items") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_costume_wearable_character_group_master(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["id", "characterBaseMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "costume_wearable_character_group_master" ("userId", "id", "characterBaseMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_exchange_shop_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "isDisplayRequiredHavingItem",
        "category",
        "name",
        "displayThingType",
        "displayItemMasterId",
        "bannerPath",
        "startDate",
        "endDate",
        "lastRefreshedAt",
        "lineup",
        "order",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "exchange_shop_master" ("userId", "id", "isDisplayRequiredHavingItem", "category", "name", "displayThingType", "displayItemMasterId", "bannerPath", "startDate", "endDate", "lastRefreshedAt", "lineup", "order") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)',
        *vals,
    )


def upsert_live_setting_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "name", "liveType", "liveDropFrameGroupMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "live_setting_master" ("userId", "id", "name", "liveType", "liveDropFrameGroupMasterId") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_mission_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "missionCategory",
        "missionViewOrder",
        "title",
        "description",
        "eventMasterId",
        "jumpType",
        "jumpTargetId",
        "startDate",
        "endDate",
        "stages",
        "comebackCampaignMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "mission_master" ("userId", "id", "missionCategory", "missionViewOrder", "title", "description", "eventMasterId", "jumpType", "jumpTargetId", "startDate", "endDate", "stages", "comebackCampaignMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)',
        *vals,
    )


def upsert_music_vocal_version_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "musicMasterId",
        "vocalVersion",
        "singer",
        "name",
        "musicTimeSecond",
        "sampleStartSeconds",
        "sampleEndSeconds",
        "musicVideoType",
        "characters",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "music_vocal_version_master" ("userId", "id", "musicMasterId", "vocalVersion", "singer", "name", "musicTimeSecond", "sampleStartSeconds", "sampleEndSeconds", "musicVideoType", "characters") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)',
        *vals,
    )


def upsert_poster_release_item_group_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "items", "itemConsumeApplyFlag"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "poster_release_item_group_master" ("userId", "id", "items", "itemConsumeApplyFlag") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_poster_release_item_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["currentPhase", "itemMasterId", "requiredQuantity"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "poster_release_item_master" ("userId", "currentPhase", "itemMasterId", "requiredQuantity") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_poster_story_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "posterMasterId",
        "episodeType",
        "characterBaseMasterId",
        "description",
        "order",
        "characterIconId",
        "characterName",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "poster_story_master" ("userId", "id", "posterMasterId", "episodeType", "characterBaseMasterId", "description", "order", "characterIconId", "characterName") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        *vals,
    )


def upsert_star_rank_reward_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["rank", "characterBaseMasterId", "characterStarRankRewardGroupMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "star_rank_reward_master" ("userId", "rank", "characterBaseMasterId", "characterStarRankRewardGroupMasterId") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_audition_clear(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "auditionMasterId",
        "clearPhase",
        "auditionClearPartyId",
        "skipClearPhase",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "audition_clear" ("userId", "id", "auditionMasterId", "clearPhase", "auditionClearPartyId", "skipClearPhase") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_sp_rate(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "liveMasterId", "point"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "sp_rate" ("userId", "id", "liveMasterId", "point") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_notification(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "importantReadAt", "updateReadAt", "bugReadAt"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "notification" ("userId", "id", "importantReadAt", "updateReadAt", "bugReadAt") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_episode(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["episodeMasterId", "hasReadAll"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "episode" ("userId", "episodeMasterId", "hasReadAll") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_character_mission(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterBaseMasterId",
        "characterMissionMasterId",
        "currentStageMasterId",
        "currentCount",
        "clearedStageOrder",
        "rewardReceivedStageOrder",
        "completedLevel",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_mission" ("userId", "id", "characterBaseMasterId", "characterMissionMasterId", "currentStageMasterId", "currentCount", "clearedStageOrder", "rewardReceivedStageOrder", "completedLevel") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        *vals,
    )


def upsert_mission_pass(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "missionPassMasterId",
        "paid",
        "freeRewardReceivedPhase",
        "spRewardReceivedPhase",
        "terminated",
        "freeRewardLoopCount",
        "freeRewardLoopReceivedPhase",
        "paidRewardLoopCount",
        "paidRewardLoopReceivedPhase",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "mission_pass" ("userId", "id", "missionPassMasterId", "paid", "freeRewardReceivedPhase", "spRewardReceivedPhase", "terminated", "freeRewardLoopCount", "freeRewardLoopReceivedPhase", "paidRewardLoopCount", "paidRewardLoopReceivedPhase") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)',
        *vals,
    )


def upsert_mission_pass_detail_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "phase",
        "missionPassMasterId",
        "clearPoint",
        "startDate",
        "endDate",
        "rewards",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "mission_pass_detail_master" ("userId", "id", "phase", "missionPassMasterId", "clearPoint", "startDate", "endDate", "rewards") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_mission_pass_master(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "itemMasterId", "startDate", "endDate"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "mission_pass_master" ("userId", "id", "itemMasterId", "startDate", "endDate") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_league_basic(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "myProperty",
        "starEnrollCount",
        "daiStarEnrollCount",
        "currentClassType",
        "bestClassType",
        "lastJoinedLeagueSeasonMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "league_basic" ("userId", "myProperty", "starEnrollCount", "daiStarEnrollCount", "currentClassType", "bestClassType", "lastJoinedLeagueSeasonMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_story_event(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "storyEventMasterId",
        "totalAcquiredPoint",
        "acquiredPointUpdatedDate",
        "lastRank",
        "readTips",
        "loginDays",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event" ("userId", "id", "storyEventMasterId", "totalAcquiredPoint", "acquiredPointUpdatedDate", "lastRank", "readTips", "loginDays") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_exchange_limit(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "exchangeShopThingId",
        "replaceType",
        "specifiedNumberOfDaysLimit",
        "exchangedCount",
        "until",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "exchange_limit" ("userId", "id", "exchangeShopThingId", "replaceType", "specifiedNumberOfDaysLimit", "exchangedCount", "until") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_league_group(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["leagueMasterId", "classType", "classOrder"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "league_group" ("userId", "leagueMasterId", "classType", "classOrder") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_league_group_member(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["leagueGroupId", "leagueMasterId", "bestScore"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "league_group_member" ("userId", "leagueGroupId", "leagueMasterId", "bestScore") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_league_history(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "leagueMasterId",
        "classType",
        "historyCount",
        "isSendedReward",
        "isPlayed",
        "classChangeType",
        "groupRank",
        "globalRank",
        "allClassGlobalRank",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "league_history" ("userId", "leagueMasterId", "classType", "historyCount", "isSendedReward", "isPlayed", "classChangeType", "groupRank", "globalRank", "allClassGlobalRank") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_jewel_shop(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "jewelShopItemMasterId",
        "purchaseCount",
        "totalPurchaseCount",
        "rePurchaseDate",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "jewel_shop" ("userId", "id", "jewelShopItemMasterId", "purchaseCount", "totalPurchaseCount", "rePurchaseDate") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_daily_limit(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "autoPlayTimes",
        "dailyLessonTimes",
        "lastRefreshedAt",
        "musicCourseFreeChallengeTimes",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "daily_limit" ("userId", "id", "autoPlayTimes", "dailyLessonTimes", "lastRefreshedAt", "musicCourseFreeChallengeTimes") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def update_daily_limit(user_id: int, row: dict) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "daily_limit" SET "autoPlayTimes" = $2, "dailyLessonTimes" = $3, '
        '"lastRefreshedAt" = $4, "musicCourseFreeChallengeTimes" = $5 WHERE "userId" = $1',
        user_id,
        row.get("autoPlayTimes"),
        row.get("dailyLessonTimes"),
        row.get("lastRefreshedAt"),
        row.get("musicCourseFreeChallengeTimes"),
    )


def upsert_league_high_score_party(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "leagueMasterId",
        "highScore",
        "classType",
        "difficulty",
        "musicMasterId",
        "leagueGroupId",
        "slots",
        "userName",
        "actingAbility",
        "leaderPosition",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "league_high_score_party" ("userId", "id", "leagueMasterId", "highScore", "classType", "difficulty", "musicMasterId", "leagueGroupId", "slots", "userName", "actingAbility", "leaderPosition") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)',
        *vals,
    )


def upsert_league_high_score_party_slot(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "leagueHighScorePartyId",
        "position",
        "characterMasterId",
        "characterLevel",
        "posterMasterId",
        "posterLevel",
        "posterBreakthroughPhase",
        "accessoryMasterId",
        "accessoryLevel",
        "currentStatus",
        "characterTalentStage",
        "characterAwakeningPhase",
        "characterDisplayAwakeningStatus",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "league_high_score_party_slot" ("userId", "id", "leagueHighScorePartyId", "position", "characterMasterId", "characterLevel", "posterMasterId", "posterLevel", "posterBreakthroughPhase", "accessoryMasterId", "accessoryLevel", "currentStatus", "characterTalentStage", "characterAwakeningPhase", "characterDisplayAwakeningStatus") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)',
        *vals,
    )


def upsert_story_event_circle(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "storyEventMasterId", "currentPoint", "highScore", "circleId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event_circle" ("userId", "id", "storyEventMasterId", "currentPoint", "highScore", "circleId") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_story_event_circle_mission(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "storyEventCircleMissionMasterId", "currentCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event_circle_mission" ("userId", "id", "storyEventCircleMissionMasterId", "currentCount") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_story_event_circle_mission_reward(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["id", "storyEventMasterId", "storyEventCircleMissionRewardMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event_circle_mission_reward" ("userId", "id", "storyEventMasterId", "storyEventCircleMissionRewardMasterId") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_story_event_high_score_buff_setting(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = ["storyEventHighScoreBuffSettingMasterId", "currentLevel"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event_high_score_buff_setting" ("userId", "storyEventHighScoreBuffSettingMasterId", "currentLevel") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_story_event_high_score_party(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "storyEventMasterId",
        "highScore",
        "rateGrade",
        "difficulty",
        "highScoreType",
        "liveSettingMasterId",
        "slots",
        "leaderPosition",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event_high_score_party" ("userId", "id", "storyEventMasterId", "highScore", "rateGrade", "difficulty", "highScoreType", "liveSettingMasterId", "slots", "leaderPosition") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_story_event_high_score_party_slot(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = [
        "id",
        "storyEventHighScoreClearPartyId",
        "position",
        "characterMasterId",
        "characterLevel",
        "characterTalentStage",
        "characterAwakeningPhase",
        "posterMasterId",
        "posterLevel",
        "posterBreakthroughPhase",
        "accessoryMasterId",
        "accessoryLevel",
        "currentStatus",
        "characterDisplayAwakeningStatus",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event_high_score_party_slot" ("userId", "id", "storyEventHighScoreClearPartyId", "position", "characterMasterId", "characterLevel", "characterTalentStage", "characterAwakeningPhase", "posterMasterId", "posterLevel", "posterBreakthroughPhase", "accessoryMasterId", "accessoryLevel", "currentStatus", "characterDisplayAwakeningStatus") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)',
        *vals,
    )


def upsert_connect_with_account(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "provider"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "connect_with_account" ("userId", "id", "provider") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_connect_with_password(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "connect_with_password" ("userId", "id") VALUES ($1, $2)',
        *vals,
    )


def upsert_tournament_detail(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "tournamentDetailMasterId",
        "bestUniqueScore",
        "perfectStar",
        "perfect",
        "great",
        "good",
        "bad",
        "miss",
        "recordedAt",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "tournament_detail" ("userId", "id", "tournamentDetailMasterId", "bestUniqueScore", "perfectStar", "perfect", "great", "good", "bad", "miss", "recordedAt") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)',
        *vals,
    )


def upsert_gradual_mission_group(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "gradualMissionGroupMasterId", "startAt"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "gradual_mission_group" ("userId", "id", "gradualMissionGroupMasterId", "startAt") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_photo(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "fileName",
        "sasToken",
        "photoEffectMasterId",
        "lock",
        "useAlbumPage",
        "level",
        "rarity",
        "signMasterId",
        "generatedAt",
        "thumbnailSasToken",
        "appearedCharacterBaseMasterIds",
        "taggedCharacterBaseMasterIds",
        "useDecoPage",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "photo" ("userId", "id", "fileName", "sasToken", "photoEffectMasterId", "lock", "useAlbumPage", "level", "rarity", "signMasterId", "generatedAt", "thumbnailSasToken", "appearedCharacterBaseMasterIds", "taggedCharacterBaseMasterIds", "useDecoPage") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)',
        *vals,
    )


def upsert_album(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "level", "publishPageNumber", "currentPresetOrder"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "album" ("userId", "id", "level", "publishPageNumber", "currentPresetOrder") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_album_page(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "page", "editType", "publishing", "items", "albumThemeMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "album_page" ("userId", "id", "page", "editType", "publishing", "items", "albumThemeMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_star_pass_status(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "type", "totalPurchasedCount", "validUntil"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "star_pass_status" ("userId", "id", "type", "totalPurchasedCount", "validUntil") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_login_pass_status(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "validUntil"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "login_pass_status" ("userId", "id", "validUntil") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_currency(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "coin", "freeJewel", "paidJewel"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "currency" ("userId", "id", "coin", "freeJewel", "paidJewel") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_decoration(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "decorationMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "decoration" ("userId", "id", "decorationMasterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_live_achievement(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "olivierReleasedCount", "olivierClearedLevel"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "live_achievement" ("userId", "id", "olivierReleasedCount", "olivierClearedLevel") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_music_video(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "musicVideoMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "music_video" ("userId", "id", "musicVideoMasterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_theater_story(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "theaterStoryMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "theater_story" ("userId", "id", "theaterStoryMasterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_live_drop_celling(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "multiLiveScheduleMasterId", "count", "totalCellingCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "live_drop_celling" ("userId", "id", "multiLiveScheduleMasterId", "count", "totalCellingCount") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_story_event_high_score(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "storyEventMasterId",
        "currentEnhancementPoint",
        "totalAcquiredEnhancementPoint",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "story_event_high_score" ("userId", "id", "storyEventMasterId", "currentEnhancementPoint", "totalAcquiredEnhancementPoint") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_comic(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["comicEpisodeMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "comic" ("userId", "comicEpisodeMasterId") VALUES ($1, $2)',
        *vals,
    )


def upsert_comeback_campaign(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["comebackCampaignMasterId", "activatedAt"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "comeback_campaign" ("userId", "comebackCampaignMasterId", "activatedAt") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_concert_stage(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["concertStageMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "concert_stage" ("userId", "concertStageMasterId") VALUES ($1, $2)',
        *vals,
    )


def upsert_limit(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "additionalAcquirablePhotoLimit",
        "acquirablePhotoLimitIncreasedTimes",
        "additionalAcquirableAccessoryLimit",
        "acquirableAccessoryLimitIncreasedTimes",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "limit" ("userId", "id", "additionalAcquirablePhotoLimit", "acquirablePhotoLimitIncreasedTimes", "additionalAcquirableAccessoryLimit", "acquirableAccessoryLimitIncreasedTimes") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_gacha_selected_thing(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["gachaMasterId", "gachaThingIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "gacha_selected_thing" ("userId", "gachaMasterId", "gachaThingIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_total_point_event(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "totalPointEventMasterId",
        "totalAcquiredPoint",
        "receivedRewardOrder",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "total_point_event" ("userId", "id", "totalPointEventMasterId", "totalAcquiredPoint", "receivedRewardOrder") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_event_box_gacha(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "eventBoxGachaMasterId", "currentBoxCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "event_box_gacha" ("userId", "id", "eventBoxGachaMasterId", "currentBoxCount") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_event_box_gacha_box_thing(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "eventBoxGachaBoxThingMasterId", "hitCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "event_box_gacha_box_thing" ("userId", "id", "eventBoxGachaBoxThingMasterId", "hitCount") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_special_event(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "specialEventMasterId", "readTips"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "special_event" ("userId", "id", "specialEventMasterId", "readTips") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_character_point_event(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterPointEventMasterId",
        "characterBaseMasterId",
        "totalAcquiredPoint",
        "lastRank",
        "readTips",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "character_point_event" ("userId", "id", "characterPointEventMasterId", "characterBaseMasterId", "totalAcquiredPoint", "lastRank", "readTips") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_another_notation(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "anotherNotationMasterId",
        "clearLamp",
        "rateGrade",
        "achievementRatePercentRecord",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "another_notation" ("userId", "id", "anotherNotationMasterId", "clearLamp", "rateGrade", "achievementRatePercentRecord") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_music_bookmark(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["musicMasterId", "musicBookmarkFlag"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "music_bookmark" ("userId", "musicMasterId", "musicBookmarkFlag") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_live_drop_limit(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["multiLiveScheduleMasterId", "currentCount", "countLimit"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "live_drop_limit" ("userId", "multiLiveScheduleMasterId", "currentCount", "countLimit") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_restriction(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "multiLiveRestrictionFinishedAt", "readMultiLiveRestrictionDialog"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "restriction" ("userId", "id", "multiLiveRestrictionFinishedAt", "readMultiLiveRestrictionDialog") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_permanent_market_thing(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["permanentMarketThingMasterId", "purchaseCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "permanent_market_thing" ("userId", "permanentMarketThingMasterId", "purchaseCount") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_time_limited_control(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "timeLimitedControlMasterId", "expiredAt"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "time_limited_control" ("userId", "id", "timeLimitedControlMasterId", "expiredAt") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_flash_sale_stage(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "flashSaleStageMasterId",
        "purchaseLimitedAt",
        "isDefault",
        "isCompleted",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "flash_sale_stage" ("userId", "id", "flashSaleStageMasterId", "purchaseLimitedAt", "isDefault", "isCompleted") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_album_theme(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "albumThemeMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "album_theme" ("userId", "id", "albumThemeMasterId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_circle_event_mission(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["circleEventMissionMasterId", "currentCount", "isActive"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "circle_event_mission" ("userId", "circleEventMissionMasterId", "currentCount", "isActive") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_pickup_character_mission(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["pickupCharacterMissionMasterId", "receivedDetailMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "pickup_character_mission" ("userId", "pickupCharacterMissionMasterId", "receivedDetailMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_league_season_result(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["leagueSeasonMasterId", "daiStarMaxEnrollCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "league_season_result" ("userId", "leagueSeasonMasterId", "daiStarMaxEnrollCount") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_event(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "eventMasterId",
        "totalAcquiredPoint",
        "acquiredPointUpdatedDate",
        "lastRank",
        "readTips",
        "loginDays",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "event" ("userId", "id", "eventMasterId", "totalAcquiredPoint", "acquiredPointUpdatedDate", "lastRank", "readTips", "loginDays") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_bonus_live(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "bonusLiveMasterId",
        "clearedStageOrder",
        "readTips",
        "dailyClearTimes",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "bonus_live" ("userId", "id", "bonusLiveMasterId", "clearedStageOrder", "readTips", "dailyClearTimes") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_bonus_live_stage(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "bonusLiveMasterStageId", "clearTimes"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "bonus_live_stage" ("userId", "id", "bonusLiveMasterStageId", "clearTimes") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_roulette_event(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "rouletteEventMasterId", "totalAcquiredPoint"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "roulette_event" ("userId", "id", "rouletteEventMasterId", "totalAcquiredPoint") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_roulette(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "rouletteMasterId", "rollCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "roulette" ("userId", "id", "rouletteMasterId", "rollCount") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_home_b_g_m(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["homeBGMMasterId", "selectionType", "homeBGMDetailMasterId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "home_b_g_m" ("userId", "homeBGMMasterId", "selectionType", "homeBGMDetailMasterId") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_link_character(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "characterBaseMasterId",
        "companyMasterId",
        "linkedCharacterBaseMasterId",
        "rewardReceivedMaxRank",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "link_character" ("userId", "id", "characterBaseMasterId", "companyMasterId", "linkedCharacterBaseMasterId", "rewardReceivedMaxRank") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_music_course(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "musicCourseMasterId",
        "clearLamp",
        "certificationGrade",
        "totalAchievementRatePercentRecord",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "music_course" ("userId", "id", "musicCourseMasterId", "clearLamp", "certificationGrade", "totalAchievementRatePercentRecord") VALUES ($1, $2, $3, $4, $5, $6)',
        *vals,
    )


def upsert_tournament_qualifying(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "tournamentQualifyingMasterId",
        "musicCourseMasterId",
        "currentChallengeCount",
        "perfectStar",
        "perfect",
        "great",
        "good",
        "bad",
        "miss",
        "totalAchievementRatePercentRecord",
        "bestRecordChallengeCount",
        "bestRecordDate",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "tournament_qualifying" ("userId", "id", "tournamentQualifyingMasterId", "musicCourseMasterId", "currentChallengeCount", "perfectStar", "perfect", "great", "good", "bad", "miss", "totalAchievementRatePercentRecord", "bestRecordChallengeCount", "bestRecordDate") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)',
        *vals,
    )


def upsert_lottery(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["lotteryMasterId", "results"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "lottery" ("userId", "lotteryMasterId", "results") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_triple_cast_party(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "order", "name", "leaderPosition"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_party" ("userId", "id", "order", "name", "leaderPosition") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_triple_cast_party_slot(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "partyId",
        "position",
        "characterId",
        "posterId",
        "accessoryId",
        "bonusAbilityEnableFlags",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_party_slot" ("userId", "id", "partyId", "position", "characterId", "posterId", "accessoryId", "bonusAbilityEnableFlags") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        *vals,
    )


def upsert_triple_cast_basic(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "starEnrollCount",
        "daiStarEnrollCount",
        "currentClassType",
        "bestClassType",
        "lastJoinedTripleCastSeasonMasterId",
        "partyOrder1",
        "partyOrder2",
        "partyOrder3",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_basic" ("userId", "id", "starEnrollCount", "daiStarEnrollCount", "currentClassType", "bestClassType", "lastJoinedTripleCastSeasonMasterId", "partyOrder1", "partyOrder2", "partyOrder3") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_triple_cast_group(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["tripleCastMasterId", "classType", "classOrder"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_group" ("userId", "tripleCastMasterId", "classType", "classOrder") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_triple_cast_group_member(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["tripleCastGroupId", "tripleCastMasterId", "bestScore"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_group_member" ("userId", "tripleCastGroupId", "tripleCastMasterId", "bestScore") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_triple_cast_high_score_party(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "tripleCastMasterId",
        "order",
        "highScore",
        "slots",
        "actingAbility",
        "leaderPosition",
        "difficulty",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_high_score_party" ("userId", "id", "tripleCastMasterId", "order", "highScore", "slots", "actingAbility", "leaderPosition", "difficulty") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        *vals,
    )


def upsert_triple_cast_high_score_party_slot(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = [
        "id",
        "tripleCastHighScorePartyId",
        "position",
        "characterMasterId",
        "characterLevel",
        "posterMasterId",
        "posterLevel",
        "posterBreakthroughPhase",
        "accessoryMasterId",
        "accessoryLevel",
        "currentStatus",
        "characterTalentStage",
        "characterAwakeningPhase",
        "characterDisplayAwakeningStatus",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_high_score_party_slot" ("userId", "id", "tripleCastHighScorePartyId", "position", "characterMasterId", "characterLevel", "posterMasterId", "posterLevel", "posterBreakthroughPhase", "accessoryMasterId", "accessoryLevel", "currentStatus", "characterTalentStage", "characterAwakeningPhase", "characterDisplayAwakeningStatus") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)',
        *vals,
    )


def upsert_triple_cast_season_result(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["tripleCastSeasonMasterId", "daiStarMaxEnrollCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_season_result" ("userId", "tripleCastSeasonMasterId", "daiStarMaxEnrollCount") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_album_preset(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "name", "order"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "album_preset" ("userId", "id", "name", "order") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_gacha(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "gachaMasterId", "rollCount"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "gacha" ("userId", "id", "gachaMasterId", "rollCount") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_triple_cast_history(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "tripleCastMasterId",
        "classType",
        "historyCount",
        "isSendedReward",
        "isPlayed",
        "classChangeType",
        "groupRank",
        "globalRank",
        "allClassGlobalRank",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "triple_cast_history" ("userId", "tripleCastMasterId", "classType", "historyCount", "isSendedReward", "isPlayed", "classChangeType", "groupRank", "globalRank", "allClassGlobalRank") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        *vals,
    )


def upsert_dugong_run(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "clearedCourseIds", "noMistakeCourseIds", "dugongRunCourseGroupId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "dugong_run" ("userId", "id", "clearedCourseIds", "noMistakeCourseIds", "dugongRunCourseGroupId") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_music_course_ranking(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "musicCourseMasterId",
        "currentChallengeCount",
        "perfectStar",
        "perfect",
        "great",
        "good",
        "bad",
        "miss",
        "totalAchievementRatePercentRecord",
        "bestRecordChallengeCount",
        "bestRecordDate",
        "hasReceivedReward",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "music_course_ranking" ("userId", "id", "musicCourseMasterId", "currentChallengeCount", "perfectStar", "perfect", "great", "good", "bad", "miss", "totalAchievementRatePercentRecord", "bestRecordChallengeCount", "bestRecordDate", "hasReceivedReward") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)',
        *vals,
    )


def upsert_friend_invitation(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "invitationCode", "hasInputOtherInvitationCode"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "friend_invitation" ("userId", "id", "invitationCode", "hasInputOtherInvitationCode") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_friend_invitation_mission(user_id: int, row: dict) -> ExecutableQuery:
    cols = [
        "id",
        "friendInvitationMissionMasterId",
        "friendInvitationMissionStageMasterId",
        "currentCount",
        "isCleared",
        "isRewardReceived",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "friend_invitation_mission" ("userId", "id", "friendInvitationMissionMasterId", "friendInvitationMissionStageMasterId", "currentCount", "isCleared", "isRewardReceived") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_name_base_color(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "nameBaseColorMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "name_base_color" ("userId", "id", "nameBaseColorMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_icon_frame(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "iconFrameMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "icon_frame" ("userId", "id", "iconFrameMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_gacha_re_roll(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["gachaMasterId", "rollCount", "isDecided"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "gacha_re_roll" ("userId", "gachaMasterId", "rollCount", "isDecided") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_trial_party_event(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "trialPartyEventMasterId", "currentStageOrder", "isCompleted"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "trial_party_event" ("userId", "id", "trialPartyEventMasterId", "currentStageOrder", "isCompleted") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_trial_party_event_stage(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "trialPartyEventStageMasterId", "isCleared"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "trial_party_event_stage" ("userId", "id", "trialPartyEventStageMasterId", "isCleared") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_trial_party_event_stage_party(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "trialPartyEventStageMasterId", "leaderPosition"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "trial_party_event_stage_party" ("userId", "id", "trialPartyEventStageMasterId", "leaderPosition") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_trial_party_event_stage_party_slot(
    user_id: int, row: dict
) -> ExecutableQuery:
    cols = [
        "id",
        "trialPartyEventStagePartyId",
        "position",
        "trialPartyCharacterMasterId",
        "trialPartyPosterMasterId",
        "trialPartyAccessoryMasterId",
    ]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "trial_party_event_stage_party_slot" ("userId", "id", "trialPartyEventStagePartyId", "position", "trialPartyCharacterMasterId", "trialPartyPosterMasterId", "trialPartyAccessoryMasterId") VALUES ($1, $2, $3, $4, $5, $6, $7)',
        *vals,
    )


def upsert_user_block(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "blockUserId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "user_block" ("userId", "id", "blockUserId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_home_skin(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "homeSkinMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "home_skin" ("userId", "id", "homeSkinMasterIds") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_accessory_auto_sell(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "autoSellRarity"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "accessory_auto_sell" ("userId", "id", "autoSellRarity") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_favorite_costume(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "characterBaseMasterId", "favoriteCostumeMasterIds"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "favorite_costume" ("userId", "id", "characterBaseMasterId", "favoriteCostumeMasterIds") VALUES ($1, $2, $3, $4)',
        *vals,
    )


def upsert_buff_item_status(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "effectType", "buffItemMasterId", "validUntil"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "buff_item_status" ("userId", "id", "effectType", "buffItemMasterId", "validUntil") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )


def upsert_multi_room_basic(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "ownerMultiRoomId"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "multi_room_basic" ("userId", "id", "ownerMultiRoomId") VALUES ($1, $2, $3)',
        *vals,
    )


def upsert_event_camp(user_id: int, row: dict) -> ExecutableQuery:
    cols = ["id", "eventMasterId", "campType", "totalSupportPoint"]
    vals = [user_id] + [row.get(k) for k in cols]
    return ExecutableQuery(
        'INSERT INTO "event_camp" ("userId", "id", "eventMasterId", "campType", "totalSupportPoint") VALUES ($1, $2, $3, $4, $5)',
        *vals,
    )
