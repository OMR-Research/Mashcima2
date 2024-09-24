from dataclasses import dataclass, field
from typing import List
from mashcima2.scene.visual.Notehead import Notehead


@dataclass
class SymbolRepository:
    """
    Extracted glyphs from MUSCIMA++ so that they can be sampled
    by the synthesizer
    """

    # TODO: this needs to be figured out and defined

    black_noteheads: List[Notehead] = field(default_factory=list)
