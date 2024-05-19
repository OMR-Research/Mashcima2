from .ComposedGlyph import ComposedGlyph
from dataclasses import dataclass


@dataclass
class HalfNote(ComposedGlyph):
    """The composed glyph of a half-notehead and a stem"""
    
    @property
    def glyph_class(self) -> str:
        # TODO: handle orientation
        return "smufl::noteHalfUp"
