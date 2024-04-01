from .Point import Point


class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
    
    @property
    def left(self) -> float:
        return self.x

    @property
    def top(self) -> float:
        return self.y
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def bottom(self) -> float:
        return self.y + self.height
    
    def __repr__(self):
        return f"Rectangle({self.x}, {self.y}, {self.width}, {self.height})"
    
    @property
    def center(self) -> Point:
        """The center point"""
        return Point(
            self.x + self.width / 2,
            self.y + self.height / 2
        )
    
    @property
    def top_left_corner(self) -> Point:
        """Top left corner point"""
        return Point(self.left, self.top)
    
    @property
    def top_right_corner(self) -> Point:
        """Top right corner point"""
        return Point(self.right, self.top)
    
    @property
    def bottom_left_corner(self) -> Point:
        """Bottom left corner point"""
        return Point(self.left, self.bottom)
    
    @property
    def bottom_right_corner(self) -> Point:
        """Bottom right corner point"""
        return Point(self.right, self.bottom)
