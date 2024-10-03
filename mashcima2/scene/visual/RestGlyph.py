from dataclasses import dataclass
from ..semantic.Rest import Rest
from ..semantic.MeasureRest import MeasureRest
from .Glyph import Glyph


@dataclass
class RestGlyph(Glyph):
    """Glyph of a rest symbol"""

    rest: Rest | MeasureRest | None = None
    "The semantic rest that this glyph represents"
