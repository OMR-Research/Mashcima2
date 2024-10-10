from .Glyph import Glyph
from mashcima2.geometry.Point import Point
from dataclasses import dataclass


@dataclass
class LineGlyph(Glyph):
    """Line glyph is a glyph that represents a line segment and as such is
    defined by two point (start and end) placed in the glyph space."""
    
    start_point: Point = None
    """Start point of the line, must be set during construction of the glyph.
    Coordinates are relative to the glyph space."""

    end_point: Point = None
    """End point of the line, must be set during construction of the glyph.
    Coordinates are relative to the glyph space."""
