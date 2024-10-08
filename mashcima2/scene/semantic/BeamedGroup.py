from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List, Optional
from .Note import Note
from .Chord import Chord
from .StemValue import StemValue
from mashcima2.nameof_via_dummy import nameof_via_dummy


@dataclass
class BeamedGroup(SceneObject):
    """A group of notes that share at least one beam."""
    
    # TODO: rests can also be part of a beamed group...
    # notes: List[Note] = field(default_factory=list)
    # "Links to all notes within this beam group"
