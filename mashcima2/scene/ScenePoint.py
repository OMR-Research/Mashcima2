from .SceneObject import SceneObject
from .AffineSpace import AffineSpace
from ..geometry.Point import Point
from dataclasses import dataclass


@dataclass
class ScenePoint(SceneObject):
    """Like the geometric point, but is placed within the scene visual hierarchy,
    therefore belonging under an affine space."""
    
    point: Point
    "The point, in the coordinate space of the attached affine space"

    space: AffineSpace
    "The affine space the point is situated in"

    def transform_to(self, other_space: AffineSpace) -> Point:
        """Returns the point, as if it was placed in a higher affine space"""
        return other_space.transform_from(self.space).apply_to(self.point)
