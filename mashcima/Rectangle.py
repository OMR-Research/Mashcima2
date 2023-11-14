from .Geometry import Geometry


class Rectangle(Geometry):
    def __init__(self, x: float, y: float, width: float, height: float):
        super().__init__()

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
    
    def elevate(self):
        super().elevate()
        return Rectangle(
            self.x + self.parent_space.x,
            self.y + self.parent_space.y,
            self.width,
            self.height
        )
    
    def __repr__(self):
        return f"Rectangle({self.x}, {self.y}, {self.width}, {self.height})"
