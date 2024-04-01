import abc
from typing import Optional
from ..geometry.Transform import Transform


class SceneObject(abc.ABC):
    """Base class for all objects in a scene"""
    
    # TODO: tags

    def __init__(self):
        self._parent: Optional["SceneObject"] = None
        "Parent scene object, may be None"

        self.transform = Transform.identity()
        """Transform that maps from this object's coordinate system
        to the parent's coordinate system"""
    
    @property
    def parent(self) -> Optional["SceneObject"]:
        """
        Provides property-like access and control over the parent scene object
        """
        return self._parent
    
    @parent.setter
    def parent(self, value: Optional["SceneObject"]):
        if value is None:
            self.detach_from_parent()
        elif isinstance(value, SceneObject):
            if self._parent is not None:
                self.detach_from_parent()
            self.attach_to_parent(value)
        else:
            raise ValueError(
                "Parent of a scene object has to be another scene object"
            )
    
    def detach_from_parent(self):
        """Detaches this scene object from parent, does nothing if no parent"""
        if self._parent is None:
            return
        self._parent._detach_child(self)
        self._parent = None
    
    def attach_to_parent(self, parent: "SceneObject", **kwargs):
        """Attaches this scene object to a parent scene object"""
        if self._parent is not None:
            raise Exception(
                "This scene object has to detached before it can be " +
                "attached to another parent object"
            )
        self._parent = parent
        parent._attach_child(self, **kwargs)
    
    def _detach_child(self, child: "SceneObject"):
        """Detach a child from this game object; override this in containers"""
        # do nothing, as no child can even be attached to begin with
        pass
    
    def _attach_child(self, child: "SceneObject", **kwargs):
        """Attach a child to this game object; override this in containers"""
        # if you are a container object, override this method
        raise Exception(
            "Cannot attach a child to a scene object that is not a " +
            "collection (e.g. a Group)"
        )
