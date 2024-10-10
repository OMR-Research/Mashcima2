from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List, Optional, Dict
from .Note import Note
from .Chord import Chord
from .BeamValue import BeamValue
from mashcima2.nameof_via_dummy import nameof_via_dummy


@dataclass
class BeamedGroup(SceneObject):
    """A group of notes that share at least one beam. Rests cannot be present
    in a beamed group, because rests lack stems and beam attaches to stems.
    Although a rest can be in the middle of a beamed group optically, it is not
    present here semantically."""
    
    chords: List[Chord] = field(default_factory=list)
    """Chords in this beamed group, in chronological order
    (chord is a group of notes that share a stem)"""

    beam_values: List[Dict[int, BeamValue]] = field(default_factory=list)
    """For each chord there is a dictionary, mapping beam numers to beam values"""

    def add_chord(self, chord: Chord, beam_values: Dict[int, BeamValue]):
        """Adds a new chord into the beamed group"""
        assert chord not in self.chords, \
            "Cannot add a chord twice into a beamed group."
        
        self.chords = [*self.chords, chord]
        self.beam_values.append(beam_values)
    
    @property
    def is_complete(self) -> bool:
        """Returns true if the beamed group has been terminated on the last chord."""
        if len(self.chords) == 0:
            return False
        return self.beam_values[-1].get(1, None) == BeamValue.end
