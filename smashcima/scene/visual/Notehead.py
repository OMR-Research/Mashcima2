from dataclasses import dataclass, field
from typing import List, Optional
from ..semantic.Note import Note
from .Glyph import Glyph
from smashcima.nameof_via_dummy import nameof_via_dummy


@dataclass
class Notehead(Glyph):
    """Glyph of a notehead, contains links specific to a notehead glyph"""

    notes: List[Note] = field(default_factory=list)
    "List of notes being represented by this notehead (typically just one)"

    @staticmethod
    def of_note(
        note: Note,
        fail_if_none=False
    ) -> Optional["Notehead"] | "Notehead":
        return note.get_inlinked(
            Notehead,
            nameof_via_dummy(Notehead, lambda n: n.notes),
            at_most_one=True,
            fail_if_none=fail_if_none
        )
