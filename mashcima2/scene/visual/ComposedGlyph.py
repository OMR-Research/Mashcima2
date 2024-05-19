from .Glyph import Glyph
from dataclasses import dataclass
import abc


@dataclass
class ComposedGlyph(Glyph, metaclass=abc.ABCMeta):
    """
    A glyph can be composed up of multiple smaller glyphs that together
    form a ligature.
    """
    pass
