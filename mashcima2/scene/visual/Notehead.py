from dataclasses import dataclass, field
from typing import List
from ..semantic.Note import Note
from .Glyph import Glyph


@dataclass
class Notehead(Glyph):
    """Glyph of a notehead, contains links specific to a notehead glyph"""

    notes: List[Note] = field(default_factory=list)
    "List of notes being represented by this notehead (typically just one)"
