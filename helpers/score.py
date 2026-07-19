"""Score-block hash verification for Lives/FinishAndValidate.

Reversed from ``*ScoreBlock.GetHash`` + ``*ScoreBlockCache.GetBlocks`` (see
scratchpad/RE_NOTES.md): each block's Hash is a running cumulative sum,
``hash[i] = hash[i-1] + sum(block[i] value fields)``, chained from 0 independently per
block-type list. A submission whose chain does not reproduce the reported hashes is a
tampered score and must be rejected.
"""

# value fields summed into each block type's hash (it's a sum, so order is irrelevant)
_BASE = ("score", "life", "note_id", "timing_type", "combo")
_SENSE = ("score", "life", "time_event_second", "sense_id", "combo")
_STAR_ACT = ("score", "life", "time_event_second", "combo")
_MULTI = ("score", "life", "time_event_second", "combo")


def _chain_ok(blocks, fields: tuple) -> bool:
    running = 0
    for block in blocks or []:
        running += sum(int(getattr(block, f)) for f in fields)
        if int(block.hash) != running:
            return False
    return True


def verify_score_blocks(payload) -> bool:
    """True if every score-block hash chain in the FinishLive payload is self-consistent."""
    return (
        _chain_ok(payload.base_score_blocks, _BASE)
        and _chain_ok(payload.sense_score_blocks, _SENSE)
        and _chain_ok(payload.star_act_score_blocks, _STAR_ACT)
        and _chain_ok(payload.multi_live_additional_score_blocks, _MULTI)
    )
