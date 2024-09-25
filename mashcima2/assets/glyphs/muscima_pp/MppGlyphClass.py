from enum import Enum


class MppGlyphClass(str, Enum):
    """
    Enum that represents glyphs from the MUSCIMA++ dataset.
    """
    noteheadFull = "muscima_pp::notehead-full"
    noteheadEmpty = "muscima_pp::notehead-empty"
    thinBarline = "muscima_pp:thin_barline"
