from ..SceneObject import SceneObject
from dataclasses import dataclass, field


@dataclass
class System(SceneObject):
    """
    A system of music is a single "line" of music with all the instruments
    side by side. It's a collection of staves and measures. It's a visual
    object and does not exist in the musical semantics.
    """
    
    first_measure_index: int
    "What is the index of the first measure on the system (relative to score)"

    measure_count: int
    "Number of measures on this system"

    @property
    def last_measure_index(self) -> int:
        """Returns index of the last measure in the system (relative to score)"""
        return self.first_measure_index + self.measure_count
