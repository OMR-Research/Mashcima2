from ..geometry.Rectangle import Rectangle
from .SceneObject import SceneObject


class ViewBox(SceneObject):
    """Viewport into the scene, always denoted in the global scene space"""

    def __init__(self, rectangle: Rectangle):
        super().__init__()

        self.rectangle = rectangle
