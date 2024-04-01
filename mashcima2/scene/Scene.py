from .Group import Group
from ..geometry.Rectangle import Rectangle


class Scene(Group):
    """
    A scene object is the result of the synthesis process. It is a hierarchical
    python-object data structure with spatial dimensions being first class
    citizen. It encapsulates as much metadata as possible.

    It can be passed to renderers to produce an annotation file,
    or the synthesized raster image.
    """
    
    def __init__(self, view_box: Rectangle):
        super().__init__()
        
        self.view_box = view_box
        "The rectangle in the scene coordinate system that is rendered"
