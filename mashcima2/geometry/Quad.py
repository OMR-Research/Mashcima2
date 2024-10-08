from .Point import Point
from .Rectangle import Rectangle
from typing import List


class Quad:
    """
    Quad is a set of four points enclosing a quadrangle area.
    This is what you get from a rectangle after doing an affine transform.
    You can turn it back to a rectangle by getting the bounding box (bbox).
    It's created from a rectangle by going over its corners from the left top
    corner in the clockwise direction.
    """

    def __init__(self, a: Point, b: Point, c: Point, d: Point):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def from_rectangle(rectangle: Rectangle) -> "Quad":
        """Constructs a quad from a rectangle by going over its corners
        from top left, in the clocwise direction."""
        return Quad(
            a=rectangle.top_left_corner,
            b=rectangle.top_right_corner,
            c=rectangle.bottom_right_corner,
            d=rectangle.bottom_left_corner
        )

    @property
    def points(self) -> List[Point]:
        """Returns the quad points as a list"""
        return [self.a, self.b, self.c, self.d]
    
    def __repr__(self):
        return f"Quad({self.a}, {self.b}, {self.c}, {self.d})"
    
    def bbox(self) -> Rectangle:
        """Returns the bounding box of the quad"""
        pts = self.points
        top = min(p.y for p in pts)
        bottom = max(p.y for p in pts)
        left = min(p.x for p in pts)
        right = max(p.x for p in pts)
        return Rectangle(
            x=left,
            y=top,
            width=right-left,
            height=bottom-top
        )
