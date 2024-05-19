from ..geometry.Rectangle import Rectangle
from .SceneObject import SceneObject


class ViewBox(SceneObject):
    def __init__(self, rectangle: Rectangle):
        super().__init__()

        self.rectangle = rectangle
