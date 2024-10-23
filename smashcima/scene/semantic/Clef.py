from dataclasses import dataclass
from .ClefSign import ClefSign
from .Pitch import Pitch


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

    @staticmethod
    def clef_line_to_pitch_position(line: int) -> int:
        """Given the staff line number, return the pitch position of that
        staff line. Pitch position is 0 on the center line, increases up and
        1 step is one half-space, i.e. the top line is 4 and the bottom line
        is -4."""
        # NOTE: we assume 5 line staff
        return (line - 3) * 2
    
    @staticmethod
    def origin_pitch(sign: ClefSign) -> Pitch:
        """Which pitch sits at the origin of the clef (e.g. G4 for G clef)"""
        if sign == ClefSign.G:
            return Pitch.parse("4", "G")
        if sign == ClefSign.F:
            return Pitch.parse("3", "F")
        if sign == ClefSign.C:
            return Pitch.parse("4", "C")
        raise Exception(f"Unknown clef sign {sign}")
    
    def pitch_to_pitch_position(self, pitch: Pitch) -> int:
        """Returns the stafflines-pitch-position for the given note pitch
        if this clef is currently active for the staff"""
        origin_pitch_position = Clef.clef_line_to_pitch_position(self.line)
        origin_linear_pitch = Clef.origin_pitch(self.sign) \
            .get_linear_pitch(with_alters=False)
        given_linear_pitch = pitch.get_linear_pitch(with_alters=False)
        return origin_pitch_position \
            + (given_linear_pitch - origin_linear_pitch)

    def pitch_position_to_pitch(self, pitch_position: int) -> Pitch:
        """Returns the note pitch on a given stafflines-pitch-position
        if this clef is currently active for the staff"""
        origin_pitch_position = Clef.clef_line_to_pitch_position(self.line)
        origin_linear_pitch = Clef.origin_pitch(self.sign) \
            .get_linear_pitch(with_alters=False)
        linear_pitch = (pitch_position - origin_pitch_position) \
            + origin_linear_pitch
        return Pitch.from_linear_pitch(linear_pitch)
