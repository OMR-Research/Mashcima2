from enum import Enum


class MppGlyphClass(str, Enum):
    """
    Enum that represents glyphs from the MUSCIMA++ dataset.
    """
    noteheadFull = "muscima_pp::notehead-full"
    noteheadEmpty = "muscima_pp::notehead-empty"
    thinBarline = "muscima_pp::thin_barline"
    gClef = "muscima_pp::g-clef"
    fClef = "muscima_pp::f-clef"
    cClef = "muscima_pp::c-clef"
