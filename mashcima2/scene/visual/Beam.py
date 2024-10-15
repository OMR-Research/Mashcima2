from .LineGlyph import LineGlyph
from ..semantic.Chord import Chord
from .BeamCoordinateSystem import BeamCoordinateSystem
from dataclasses import dataclass, field
from typing import List


@dataclass
class Beam(LineGlyph):
    """One beam (one line) in a beamed group (visually)"""

    chords: List[Chord] = field(default_factory=list)
    """List of chords that are tied together by this beam
    (in chronological order)"""

    beam_number: int = 1
    """Which beam is this beam (1 being the 8th notes beam).
    Uses the MusicXML numbering."""

    beam_coordinate_system: BeamCoordinateSystem = None
    "Defines the placement of the beam on the paper"
