from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from fractions import Fraction
from .Durable import Durable
from typing import List


@dataclass
class Event(SceneObject):
    """A collection of notes (and other symbols) with the same musical onset"""
    
    fractional_measure_onset: Fraction
    """How many quarter notes from the beginning of the measure this event occus"""

    durables: List[Durable] = field(default_factory=list)
    "Links to all durables with this onset time"
