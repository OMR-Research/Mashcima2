from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List
from .Durable import Durable


@dataclass
class Staff(SceneObject):
    """
    Represents a staff within a measure (e.g. piano measures have 2 staves),
    as a collection of durables
    """

    staff_number: int
    "Number of this staff, e.g. 1, 2, 3. Numbered from 1 and from the top down"

    durables: List[Durable] = field(default_factory=list)
    "Links to all durables within this staff"
