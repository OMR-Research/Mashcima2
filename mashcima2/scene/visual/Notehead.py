from dataclasses import dataclass, field
from typing import Optional, List
from ..semantic.Note import Note
from .Glyph import Glyph
from .Stafflines import Stafflines
from nameof import nameof


@dataclass
class Notehead(Glyph):
    """Glyph of a notehead, contains links specific to a notehead glyph"""

    assigned_glyph_class: str = None
    "Class assigned to this glyph during construction"

    notes: List[Note] = field(default_factory=list)
    "List of notes being represented by this notehead (typically just one)"

    stafflines: Optional[Stafflines] = None
    "Which stafflines does this notehead sit on"

    def __post_init__(self):
        assert self.assigned_glyph_class is not None

    @property
    def glyph_class(self) -> str:
        return str(self.assigned_glyph_class)

    @staticmethod
    def of_note(note: Note) -> Optional["Notehead"]:
        """Returns the notehead corresponding to a given note"""
        links = [
            l for l in note.inlinks
            if isinstance(l.source, Notehead) and l.name == nameof(l.source.notes)
        ]
        if len(links) == 0:
            return None
        elif len(links) == 1:
            return links[0].source
        else:
            raise Exception("There are more than one notehead for a note")
