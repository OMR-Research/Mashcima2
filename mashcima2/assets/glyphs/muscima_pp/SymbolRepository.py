from dataclasses import dataclass, field
from typing import List
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.Notehead import Notehead


@dataclass
class SymbolRepository:
    """
    Extracted glyphs from MUSCIMA++ so that they can be sampled
    by the synthesizer
    """
    empty_noteheads: List[Notehead] = field(default_factory=list)
    full_noteheads: List[Notehead] = field(default_factory=list)
    normal_barlines: List[Glyph] = field(default_factory=list)
