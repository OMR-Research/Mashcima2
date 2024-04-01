class Vector2:
    """Mathematical 2D vector"""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
    
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
        return f"Vector2({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Vectors can only be added with other vectors")
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            raise ValueError("Vectors can only be subtracted from other vectors")
    
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x * other, self.y * other)
        else:
            raise ValueError("Vectors can only be multiplied by scalars")
    
    def __div__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x / other, self.y / other)
        else:
            raise ValueError("Vectors can only be divided by scalars")
