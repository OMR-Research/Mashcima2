from dataclasses import dataclass
from .ClefSign import ClefSign


@dataclass
class Clef:
    """Represents a music notation clef"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/clef/

    sign: ClefSign
    "What type of clef is this"

    line: int
    "Position of the clef, 1 is bottom staffline, numbering goes up"

    after_barline: bool = False
    """Should the clef be rendered after the barline? If not (default),
    the clef is rendered at the end of previous measure (if its onset is 0).
    Ignored for mid-measure clefs."""
