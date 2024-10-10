from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List, Optional
from .Note import Note
from .StemValue import StemValue
from mashcima2.nameof_via_dummy import nameof_via_dummy


@dataclass
class Chord(SceneObject):
    """Chord is a collection of notes that share one stem. Even a single note
    has a chord, since it needs to encode its stem information here. Musically
    a chord is a group of notes with the same onset and duration though."""
    
    notes: List[Note] = field(default_factory=list)
    "Links to all notes within this chord"

    stem_value: Optional[StemValue] = None
    "What orientation does the stem have. If none, infer when rendering."

    @staticmethod
    def of_note(
        note: Note,
        fail_if_none=False
    ) -> Optional["Chord"] | "Chord":
        return note.get_inlinked(
            Chord,
            nameof_via_dummy(Chord, lambda c: c.notes),
            at_most_one=True,
            fail_if_none=fail_if_none
        )
    
    def add_note(self, note: Note, stem_value: StemValue = None):
        """Adds a note into the chord with a stem value"""
        # store stem value if missing
        if self.stem_value is None:
            self.stem_value = stem_value

        # validate stem value if present
        if self.stem_value is not None and stem_value is not None:
            assert self.stem_value == stem_value, \
                "All notes in a chord must have the same stem value"
        
        # update the list of notes
        notes = [*self.notes, note]
        notes.sort(key=lambda n: n.pitch.get_linear_pitch()) # ascending by pitch
        self.notes = notes
