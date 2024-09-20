from dataclasses import dataclass
from ..SceneObject import SceneObject
from typing import List
from .Measure import Measure


@dataclass
class Staff(SceneObject):
    # TODO: get rid of this, it's only encoded via line/page breaks

    # TODO: staff vs. grandstaff vs. system
    measures: List[Measure]
