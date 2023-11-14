from abc import ABC, abstractmethod


class Geometry(ABC):
    """Represents some geometric object that can be embedded within a Space"""
    def __init__(self):
        self.parent_space = None
        "The space that this geometry is embedded in"
    
    def is_embedded(self) -> bool:
        """Returns true if this geometry is embedded in some space"""
        return self.parent_space is not None
    
    def embed_into(self, space):
        """Embeds this geometry into a given space"""
        self.parent_space = space

    @abstractmethod
    def elevate(self):
        """
        Returns a copy of this geometry, that is located one
        step up in the space hierarchy with the coordinates updated properly
        """
        if self.parent_space is None:
            raise Exception("Only embedded geometries can be elevated")

    def elevate_into(self, target_space):
        """Elevate this geometry all the way to a given target space"""
        me = self
        space = self.parent_space
        while True:
            if space is target_space:
                return me
            if space is None:
                raise Exception("Target space is not an ancestor of this geometry")
            
            me = me.elevate()
            space = space.parent # because elevation looses the parent space
