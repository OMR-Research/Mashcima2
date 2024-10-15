from .LineGlyph import LineGlyph
from .BeamCoordinateSystem import BeamCoordinateSystem
from ..semantic.Chord import Chord
from dataclasses import dataclass
from ..semantic.BeamValue import BeamValue


@dataclass
class BeamHook(LineGlyph):
    """One hook glyph in a beamed group (visually)"""

    chord: Chord = None
    """The chord in whose stem the hook is placed"""

    beam_number: int = 1
    """Which beam is this beam (1 being the 8th notes beam).
    Uses the MusicXML numbering."""

    hook_type: BeamValue = None
    """Either forward hook or backward hook. Any other value is invalid."""

    beam_coordinate_system: BeamCoordinateSystem = None
    "Defines the placement of the beam on the paper"
