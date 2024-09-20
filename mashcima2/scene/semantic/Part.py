from dataclasses import dataclass
from ..SceneObject import SceneObject
from typing import List
from .Measure import Measure


@dataclass
class Part(SceneObject):
    """Represents a single part (an instrument) of a score"""
    
    measures: List[Measure]
    "A part consists of a list of measures"
