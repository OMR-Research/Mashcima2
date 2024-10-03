from enum import Enum
from fractions import Fraction


class TypeDuration(str, Enum):
    """
    Type-duration of a note/rest (i.e. whole, quarter, 16th).
    It encodes what the musical symbol looks like, not how much time it
    actually takes up. (e.g. a triplet will be an eighth type; a grace
    note has type but no duration)

    Based on the MusicXML <type> element.
    """
    
    thousand_twenty_fourth = "1024th"
    five_hundred_twelfth = "512th"
    two_hundred_fifty_sixth = "256th"
    hundred_twenty_eighth = "128th"
    sixty_fourth = "64th"
    thirty_second = "32nd"
    sixteenth = "16th"
    eighth = "eighth"
    quarter = "quarter"
    half = "half"
    whole = "whole"
    breve = "breve"
    long = "long"
    maxima = "maxima"

    def to_quarter_multiple(self) -> Fraction:
        """Returns the number of beats (quarter notes) that this duration type
        takes up in total."""
        _LOOKUP = {
            "1024th":  Fraction(1, 256),
            "512th":   Fraction(1, 128),
            "256th":   Fraction(1, 64),
            "128th":   Fraction(1, 32),
            "64th":    Fraction(1, 16),
            "32nd":    Fraction(1, 8),
            "16th":    Fraction(1, 4),
            "eighth":  Fraction(1, 2),
            "quarter": Fraction(1, 1), # one
            "half":    Fraction(2, 1),
            "whole":   Fraction(4, 1),
            "breve":   Fraction(8, 1),
            "long":    Fraction(16, 1),
            "maxima":  Fraction(32, 1),
        }
        beats = _LOOKUP.get(self.value, None)
        if beats is None:
            raise Exception("Unknown beat count for type " + self)
        return beats
