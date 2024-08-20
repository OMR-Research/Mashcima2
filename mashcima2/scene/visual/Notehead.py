from dataclasses import dataclass
from typing import Optional
from ..semantic.Note import Note
from .Glyph import Glyph
from nameof import nameof


@dataclass
class Notehead(Glyph):
    # TODO: there may be multiple!
    note: Optional[Note] = None

    @property
    def glyph_class(self) -> str:
        # https://www.w3.org/2019/03/smufl13/tables/noteheads.html
        # TODO: handle other notehead types (mainly full and half)
        return "smufl::noteheadBlack"

    @staticmethod
    def of_note(note: Note) -> Optional["Notehead"]:
        links = [
            l for l in note.inlinks
            if isinstance(l.source, Notehead) and l.name == nameof(l.source.note)
        ]
        if len(links) == 0:
            return None
        elif len(links) == 1:
            return links[0].source
        else:
            raise Exception("There are more than one note for a notehead")
