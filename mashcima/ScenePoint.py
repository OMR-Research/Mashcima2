from mashcima.SceneObject import SceneObject


class ScenePoint(SceneObject):
    """A 2D point inside a scene"""
    def __init__(self, x: float, y: float):
        self.x = float(x)
        "X coordinate of the point in scene units (millimeters)"
        
        self.y = float(y)
        "Y coordinate of the point in scene units (millimeters)"
    
    def debug_print(self, indent: str = "", name: str = ""):
        print(indent + f"[Point] {name} <{hex(id(self))}> ({self.x}, {self.y})")
