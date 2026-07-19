"""The tutorial progression. A client may only advance through these steps, never
backtrack -- Player_UpdateTutorial rejects a target that precedes the current step.
"""

from models.enums import TutorialStatus

# expected order of tutorial steps
TUTORIAL_ORDER = (
    TutorialStatus.Start,
    TutorialStatus.TutorialDownLoad,
    TutorialStatus.MainScenario,
    TutorialStatus.TheaterMovie,
    TutorialStatus.Home,
    TutorialStatus.InGame,
    TutorialStatus.MiniTalk,
    TutorialStatus.Finish,
)


def can_advance(current: int, target: int) -> bool:
    """True if ``target`` is at or ahead of ``current`` in the tutorial order."""
    return TUTORIAL_ORDER.index(TutorialStatus(target)) >= TUTORIAL_ORDER.index(
        TutorialStatus(current)
    )
