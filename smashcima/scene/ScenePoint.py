from .SceneObject import SceneObject
from .AffineSpace import AffineSpace
from .Sprite import Sprite
from ..geometry.Point import Point
from ..geometry.Rectangle import Rectangle
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

    def detach(self):
        """Detaches the scene point from the scene hierarchy"""
        self.space = None
    
    def place_debug_overlay(self, radius=0.25, color=(0, 0, 255, 128)) -> Sprite:
        """Places a sprite that acts as debugging overlay for the point"""
        return Sprite.debug_box(
            space=self.space,
            rectangle=Rectangle(
                x=self.point.x - radius,
                y=self.point.y - radius,
                width=radius * 2,
                height=radius * 2
            ),
            fill_color=color,
            border_width=0
        )
