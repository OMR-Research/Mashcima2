import numpy as np
from mashcima.SceneObject import SceneObject


class SceneImage(SceneObject):
    """An image inside a scene"""
    def __init__(self,
        x: float, y: float, width: float, height: float,
        img: np.ndarray
    ):
        # TODO: there should be Millimeters(5.0) type that holds the distance unit

        self.x = float(x)
        "X coordinate of the top left corner of the image"
        
        self.y = float(y)
        "Y coordinate of top left corner of the image"

        self.width = float(width)
        "Physical width the image is going to be rendered at"

        self.height = float(height)
        "Physical height the image is going to be rendered at"

        self.img = img
        "The numpy array holding the image data"
    
    def debug_print(self, indent: str = "", name: str = ""):
        print(indent + f"[Image] {name} <{hex(id(self))}> " + \
            f"({self.x}, {self.y}, {self.width}, {self.height}) @ {repr(self.img.shape)}")
        for line in repr(self.img).splitlines():
            print(indent + "    " + line)
