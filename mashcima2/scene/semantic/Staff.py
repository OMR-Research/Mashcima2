from dataclasses import dataclass
from ..SceneObject import SceneObject
from typing import List
from .Measure import Measure


@dataclass
class Staff(SceneObject):
    # TODO: staff vs. grandstaff vs. system
    measures: List[Measure]
