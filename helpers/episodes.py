"""Episode scene scripts.

The vendored ``_data/episodes/<id>.json`` files (from wds-sirius/Adv-Resource) each hold an
episode's metadata plus its ``EpisodeDetail`` -- the full script, one entry per scene line.
The client fetches that script as a msgpack ``.bin`` (an ``EpisodeDetailResult[]``); this packs
it on demand and caches the result. ``bin_hashes.json`` (the repo's manifest/BinHash.json) maps
each episode id to its ``"<id>_<hash>"`` blob name, used to build the download URL.
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from helpers.cache import cache
from helpers.config import config
from helpers.msgpack import pack
from models import EpisodeDetailResult, EpisodeResult
from models.enums import StoryTypes

_DIR = Path(__file__).resolve().parent.parent / "_data" / "episodes"

_HASHES_PATH = _DIR / "bin_hashes.json"
_BIN_HASHES: dict = (
    json.loads(_HASHES_PATH.read_text(encoding="utf-8"))
    if _HASHES_PATH.exists()
    else {}
)


def scene_bin_name(episode_id: int) -> Optional[str]:
    """The episode's ``"<id>_<hash>"`` scene-blob name, or None if we don't have it."""
    return _BIN_HASHES.get(str(episode_id))


def _asset_base() -> str:
    # scene bins are served under /master-data/production/scenes/ (see routes/episodes.py),
    # so build the client-facing URL off the same master-data base.
    return str(config["master_data_url"]).rstrip("/")


# episode-master tables that carry title/order and link to a StoryMaster (its .type is the
# story type: Main/Event/Special). CharacterEpisodeMaster has no story link and no title --
# its episodes are Side stories.
_STORY_EPISODE_TABLES = (
    "episode_master",
    "story_event_episode_master",
    "special_episode_master",
)

_EPISODE_META: dict = {}  # episode_master_id -> (title, order, StoryTypes)


def _build_meta() -> None:
    if _EPISODE_META:
        return
    story_type = {sm.id_: sm.type for sm in cache.story_master}
    for attr in _STORY_EPISODE_TABLES:
        for e in getattr(cache, attr):
            _EPISODE_META[e.id_] = (
                getattr(e, "title", None),
                getattr(e, "order", 0) or 0,
                story_type.get(e.story_master_id, StoryTypes.None_),
            )
    for e in cache.character_episode_master:
        _EPISODE_META[e.id_] = (None, e.episode_order, StoryTypes.Side)


@lru_cache(maxsize=1024)
def _local_meta(episode_id: int) -> Optional[tuple]:
    """(title, order, StoryTypes) from the vendored ``<id>.json`` top-level, or None."""
    path = _DIR / f"{episode_id}.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    return raw.get("Title"), raw.get("Order", 0), StoryTypes(raw.get("StoryType", 0))


def episode_result(episode_id: int) -> Optional[EpisodeResult]:
    """The EpisodeResult (title/type/order + scene-bin download URL) for GetEpisodeDetail, or
    None if we can't describe the episode / have no scene blob.

    Character episodes (StoryType 4) come from the vendored local files -- they have no
    master-data entry at all. Every other type (Main/Event/Side/Special) comes from master data.
    """
    name = scene_bin_name(episode_id)
    if name is None:
        return None
    _build_meta()
    meta = _EPISODE_META.get(episode_id)
    if (
        meta is None
    ):  # absent from master data == a Character (StoryType 4) episode -> local
        meta = _local_meta(episode_id)
        if meta is None:
            return None
    title, order, story_type = meta
    return EpisodeResult(
        episode_title=title,
        story_type=story_type,
        episode_order=order,
        episode_detail_asset_source=f"scenes/{name}.bin",
    )


# The 歌劇目録 (opera catalogue) items -- their item category. It's the extra reward for reading
# ALL of an episode's text, but only for MAIN-story episodes (EpisodeMaster). Event packages
# also carry the item as a normal read reward, but their full-read grants no extra copy.
_CATALOGUE_ITEM_CATEGORY = 13

_READ_REWARDS: dict = (
    {}
)  # episode id -> read reward (the full package, chapter-all excluded)
_READALL_REWARDS: dict = (
    {}
)  # main episode id -> read-all reward (the catalogue item[s])


def _build_rewards() -> None:
    if _READ_REWARDS:
        return
    catalogue = {
        it.id_ for it in cache.item_master if it.category == _CATALOGUE_ITEM_CATEGORY
    }
    main_episodes = {e.id_ for e in cache.episode_master}
    for pkg in cache.episode_reward_package_master:
        read = [
            (int(r.thing_type), r.thing_id, r.thing_quantity)
            for r in (pkg.rewards or [])
            if not r.is_chapter_all_read_reward
        ]
        _READ_REWARDS[pkg.id_] = read
        if pkg.id_ in main_episodes:
            _READALL_REWARDS[pkg.id_] = [
                t for t in read if t[0] == 1 and t[1] in catalogue
            ]


def episode_read_reward_things(episode_id: int) -> list[tuple[int, int, int]]:
    """The reward for reading an episode -- its full reward package (minus the chapter-all-read
    bonus; package id == episode id). Granted once, on the first Read or ReadAll."""
    _build_rewards()
    return _READ_REWARDS.get(episode_id, [])


def episode_readall_reward_things(episode_id: int) -> list[tuple[int, int, int]]:
    """The extra reward for reading ALL an episode's text -- the 歌劇目録 catalogue item(s) from
    its package. Granted once by ReadAll, on top of the read reward."""
    _build_rewards()
    return _READALL_REWARDS.get(episode_id, [])


@lru_cache(maxsize=1024)
def episode_scene_bin(episode_id: int) -> Optional[bytes]:
    """msgpack of the episode's ``EpisodeDetailResult[]`` (its whole script), or None if the
    episode isn't vendored."""
    path = _DIR / f"{episode_id}.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    scenes = [
        EpisodeDetailResult.model_validate(s) for s in (raw.get("EpisodeDetail") or [])
    ]
    return pack(scenes)
