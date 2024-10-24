from dataclasses import dataclass, field
from typing import List, Optional
from ..semantic.Note import Note
from .Glyph import Glyph
from .NoteheadSide import NoteheadSide
from smashcima.nameof_via_dummy import nameof_via_dummy


@dataclass
class Notehead(Glyph):
    """Glyph of a notehead, contains links specific to a notehead glyph"""

    notes: List[Note] = field(default_factory=list)
    "List of notes being represented by this notehead (typically just one)"

    up_stem_attachment_side: Optional[NoteheadSide] = NoteheadSide.right
    """On what side of the notehead should an up-pointing stem be attached.
    Notehead placing algorithm can modify this, e.g. in a dense
    chord where noteheads have to be from both sides of the stem.
    None means there should not ever be such a stem attached."""

    down_stem_attachment_side: Optional[NoteheadSide] = NoteheadSide.left
    """On what side of the notehead should a down-pointing stem be attached.
    Notehead placing algorithm can modify this, e.g. in a dense
    chord where noteheads have to be from both sides of the stem.
    None means there should not ever be such a stem attached."""

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
