from .SceneObject import SceneObject
from typing import List, Optional


class Group(SceneObject):
    """A group of scene objects with a shared transform"""
    
    def __init__(self):
        self._children: List[SceneObject] = []
        "Children scene objects of this group object"
    
    def _detach_child(self, child: "SceneObject"):
        self._children.remove(child)
    
    def _attach_child(
        self,
        child: "SceneObject",
        at_index: Optional[int] = None,
        **kwargs
    ):
        if at_index is None:
            at_index = len(self._children) - 1
        self._children.insert(at_index, child)

    def insert(self, at_index: int, child: SceneObject):
        """Insert a child before the given index"""
        if child.parent is not None:
            raise ValueError(
                "You can only insert objects that are not already a " +
                    "part of some scene hierarchy"
            )
        child.attach_to_parent(self, at_index=at_index)

    def append(self, child: SceneObject):
        """Append a child object at the end"""
        if child.parent is not None:
            raise ValueError(
                "You can only append objects that are not already a " +
                    "part of some scene hierarchy"
            )
        child.attach_to_parent(self, at_index=None)
