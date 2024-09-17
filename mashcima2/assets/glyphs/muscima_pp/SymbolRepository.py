from dataclasses import dataclass, field
from typing import List
from .MppGlyph import MppGlyph


@dataclass
class SymbolRepository:
    """
    Extracted glyphs from MUSCIMA++ so that they can be sampled
    by the synthesizer
    """

    # TODO: this needs to be figured out and defined

    whole_notes: List[MppGlyph] = field(default_factory=list)

    black_noteheads: List[MppGlyph] = field(default_factory=list)
