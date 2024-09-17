from enum import Enum


class SmuflGlyphClass(str, Enum):
    """
    Enum that represents glyphs from the SMuFL specification.
    https://www.w3.org/2019/03/smufl13/
    """
    
    # Noteheads
    # https://w3c.github.io/smufl/latest/tables/noteheads.html
    noteheadWhole = "smufl::noteheadWhole"
    noteheadHalf = "smufl::noteheadHalf"
    noteheadBlack = "smufl::noteheadBlack"

    # Individual Notes
    # https://www.w3.org/2019/03/smufl13/tables/individual-notes.html
    # NOTE: This should only be used for ligatures,
    # the default usecase is synthesizing notehead-stem-flag separately.
    noteWhole = "smulf::noteWhole"
    noteHalfUp = "smulf::noteHalfUp"
    noteHalfDown = "smulf::noteHalfDown"
    noteQuarterUp = "smulf::noteQuarterUp"
    noteQuarterDown = "smulf::noteQuarterDown"
    note8thUp = "smulf::note8thUp"
    note8thDown = "smulf::note8thDown"
    note16thUp = "smulf::note16thUp"
    note16thDown = "smulf::note16thDown"
    note32ndUp = "smulf::note32ndUp"
    note32ndDown = "smulf::note32ndDown"
    # ...
    augmentationDot = "smulf::augmentationDot"

    # Rests
    # https://www.w3.org/2019/03/smufl13/tables/rests.html
    # ...
    restWhole = "smulf::restWhole"
    restHalf = "smulf::restHalf"
    restQuarter = "smulf::restQuarter"
    rest8th = "smulf::rest8th"
    rest16th = "smulf::rest16th"
    rest32nd = "smulf::rest32nd"
