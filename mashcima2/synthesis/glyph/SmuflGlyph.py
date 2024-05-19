from enum import Enum


class SmuflGlyphClass(str, Enum):
    """
    Enum that represents glyphs from the SMuFL specification.
    https://www.w3.org/2019/03/smufl13/
    """
    
    # Individual Notes
    # https://www.w3.org/2019/03/smufl13/tables/individual-notes.html
    # ...
    noteWhole = "noteWhole"
    noteHalfUp = "noteHalfUp"
    noteHalfDown = "noteHalfDown"
    noteQuarterUp = "noteQuarterUp"
    noteQuarterDown = "noteQuarterDown"
    note8thUp = "note8thUp"
    note8thDown = "note8thDown"
    note16thUp = "note16thUp"
    note16thDown = "note16thDown"
    note32ndUp = "note32ndUp"
    note32ndDown = "note32ndDown"
    # ...
    augmentationDot = "augmentationDot"

    # Rests
    # https://www.w3.org/2019/03/smufl13/tables/rests.html
    # ...
    restWhole = "restWhole"
    restHalf = "restHalf"
    restQuarter = "restQuarter"
    rest8th = "rest8th"
    rest16th = "rest16th"
    rest32nd = "rest32nd"
