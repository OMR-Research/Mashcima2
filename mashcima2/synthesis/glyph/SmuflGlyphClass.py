from enum import Enum
from mashcima2.scene.semantic.TypeDuration import TypeDuration


class SmuflGlyphClass(str, Enum):
    """
    Enum that represents glyphs from the SMuFL specification.
    https://www.w3.org/2019/03/smufl13/
    """

    # Barlines
    # https://w3c.github.io/smufl/latest/tables/barlines.html
    barlineSingle = "smufl::barlineSingle"

    # Clefs
    # https://w3c.github.io/smufl/latest/tables/clefs.html
    gClef = "smufl::gClef"
    cClef = "smufl::cClef"
    fClef = "smufl::fClef"
    gClefSmall = "smufl::gClefSmall"
    cClefSmall = "smufl::cClefSmall"
    fClefSmall = "smufl::fClefSmall"

    # Noteheads
    # https://w3c.github.io/smufl/latest/tables/noteheads.html
    noteheadDoubleWhole = "smufl::noteheadDoubleWhole"
    noteheadDoubleWholeSquare = "smufl::noteheadDoubleWholeSquare"
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

    @staticmethod
    def notehead_from_type_duration(duration: TypeDuration) -> "SmuflGlyphClass":
        # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/note-type-value/
        _LOOKUP = {
            TypeDuration.thousand_twenty_fourth: SmuflGlyphClass.noteheadBlack,
            TypeDuration.five_hundred_twelfth: SmuflGlyphClass.noteheadBlack,
            TypeDuration.two_hundred_fifty_sixth: SmuflGlyphClass.noteheadBlack,
            TypeDuration.sixty_fourth: SmuflGlyphClass.noteheadBlack,
            TypeDuration.thirty_second: SmuflGlyphClass.noteheadBlack,
            TypeDuration.sixteenth: SmuflGlyphClass.noteheadBlack,
            TypeDuration.eighth: SmuflGlyphClass.noteheadBlack,
            TypeDuration.quarter: SmuflGlyphClass.noteheadBlack,
            TypeDuration.half: SmuflGlyphClass.noteheadHalf,
            TypeDuration.whole: SmuflGlyphClass.noteheadWhole,
            TypeDuration.breve: SmuflGlyphClass.noteheadDoubleWhole,
            TypeDuration.long: SmuflGlyphClass.noteheadDoubleWholeSquare,
            TypeDuration.maxima: SmuflGlyphClass.noteheadDoubleWholeSquare,
        }
        notehead = _LOOKUP.get(duration)
        if notehead is None:
            raise Exception(f"Unsupported type duration " + duration)
        return notehead
    
    @staticmethod
    def clef_from_clef_sign(clef_sign: str, small=False) -> "SmuflGlyphClass":
        _LOOKUP = {
            ("G", False): SmuflGlyphClass.gClef,
            ("G", True): SmuflGlyphClass.gClefSmall,
            ("F", False): SmuflGlyphClass.fClef,
            ("F", True): SmuflGlyphClass.fClefSmall,
            ("C", False): SmuflGlyphClass.cClef,
            ("C", True): SmuflGlyphClass.cClefSmall,
        }
        key = (clef_sign, small)
        clef = _LOOKUP.get(key)
        if clef is None:
            raise Exception(f"Unsupported clef " + key)
        return clef