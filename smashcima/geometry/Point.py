from .Vector2 import Vector2


class Point:
    """Geometric 2D point"""
    def __init__(self, x: float, y: float):
        self.vector = Vector2(float(x), float(y))
        "The vector from origin to the point position that defines this point"
    
    @staticmethod
    def from_origin_vector(vector: Vector2) -> "Point":
        return Point(vector.x, vector.y)

    @property
    def x(self) -> float:
        return self.vector.x

    @property
    def y(self) -> float:
        return self.vector.y

    @property
    def left(self) -> float:
        return self.vector.x

    @property
    def top(self) -> float:
        return self.vector.y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def __iter__(self):
        yield self.x
        yield self.y
