from dataclasses import dataclass, field
from typing import Optional
from fractions import Fraction
from ..SceneObject import SceneObject
from .Durable import Durable
from typing import List


@dataclass
class Measure(SceneObject):
    # TODO: system-staff-grandstaff measure distinction!
    
    durables: List[Durable]
    "Links to all durables within this measure"
