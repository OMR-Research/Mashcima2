from dataclasses import dataclass


@dataclass
class KeySignature:
    """Represents music notation key signature"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/key/
    
    fifths: int
    """Number of flats or sharps of a key signature. Negative values are flats.
    Zero is no accidentals."""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fifths/

    def __post_init__(self):
        assert self.fifths in list(range(-7, 7+1)), \
            "Key signature fifths must be between -7 and +7"
