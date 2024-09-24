from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List, Optional
from .Durable import Durable
from nameof import nameof


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

    @staticmethod
    def of_durable(durable: Durable) -> Optional["Staff"]:
        """Returns the staff corresponding to a given durable"""
        links = [
            l for l in durable.inlinks
            if isinstance(l.source, Staff) and l.name == nameof(l.source.durables)
        ]
        if len(links) == 0:
            return None
        elif len(links) == 1:
            return links[0].source
        else:
            raise Exception("There are more than one staff for the durable")
