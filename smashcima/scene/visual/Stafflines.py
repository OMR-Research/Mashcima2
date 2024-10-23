from ..SceneObject import SceneObject
from dataclasses import dataclass, field
from ..AffineSpace import AffineSpace
from ..Sprite import Sprite
from typing import List
import abc
from ...geometry.Transform import Transform


class StaffCoordinateSystem(abc.ABC):
    @abc.abstractmethod
    def get_transform(
        self,
        pitch_position: float,
        time_position: float
    ) -> Transform:
        """Converts stafflines coordinates (pitch position in staffspace/2 units,
        where zero is the middle staffline, 4 is the topmost staffline;
        time position in milimeters from the begining of the staff)
        to a transform to a specific place (and possibly rotation)
        on the staff."""
        # TODO: maybe time position should be in different units than
        # millimeters, this needs to be inspected. How does staffline
        # spacing affect temporal spacing of notes. Are they related? How?
        raise NotImplementedError


@dataclass
class Stafflines(SceneObject):
    """Represents the visual stafflines for a staff on the page"""

    width: float
    "Width (in millimeters) of these stafflines"

    staff_coordinate_system: StaffCoordinateSystem
    "Coordinate system that maps from pitch-time space to 2D position"

    space: AffineSpace = field(default_factory=AffineSpace)
    "The affine space that contains all glyphs on these stafflines"

    sprites: List[Sprite] = field(default_factory=list)
    "Sprites that together make up the stafflines visually"
