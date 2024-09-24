from ..SceneObject import SceneObject
from dataclasses import dataclass, field


@dataclass
class System(SceneObject):
    """
    A system of music is a single "line" of music with all the instruments
    side by side. It's a collection of staves and measures. It's a visual
    object and does not exist in the musical semantics.
    """
    pass
