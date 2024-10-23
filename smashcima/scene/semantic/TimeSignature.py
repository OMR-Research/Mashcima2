from dataclasses import dataclass
from enum import Enum


class TimeSymbol(str, Enum):
    """How to render a time signature"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/time-symbol/
    common = "common" # the "C" symbol
    cut = "cut" # the "slashed C" symbol
    normal = "normal" # two numbers atop each other


@dataclass
class TimeSignature:
    """Represents music notation time signature"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/time/
    
    beats: int
    "How many beats are there in one measure. It's the top number."

    beat_type: int
    "What note type is one beat. It's the bottom number, 4 = quarter."

    symbol: TimeSymbol
    "How to render the time signature"

    def __post_init__(self):
        assert self.beats in list(range(1, 16+1)), \
            "Unexpected beat number per measure (expected 1-16)"
        assert self.beat_type in [2, 4, 8, 16], "Unexpected beat type."
