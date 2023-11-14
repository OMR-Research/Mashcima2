from mashcima.SceneObject import SceneObject
from typing import List, Optional, Any, Dict
from .Geometry import Geometry


class Space:
    current: Optional["Space"] = None

    """
    Space defines a 2D space in which objects exist

    It defines the object hierarchy, object IDs,
    and facilitates final image composition from
    smaller parts.
    """
    def __init__(self, parent=None):
        self._items: Dict[str, Any] = dict()
        "List of all items within this space"

        self.parent = parent
        "Parent space"

        self.x = 0.0
        self.y = 0.0

        self._model_registrations = {}

        self._previous_space_context: Optional["Space"] = None

    def try_register(self, contract, factory):
        if contract not in self._model_registrations:
            self.register(contract, factory)

    def register(self, contract, factory):
        self._model_registrations[contract] = factory
    
    def try_resolve(self, contract):
        if contract in self._model_registrations:
            return self._model_registrations[contract]()
        if self.parent is not None:
            return self.parent.try_resolve(contract)
        return None

    def resolve(self, contract):
        model = self.try_resolve(contract)
        if issubclass(contract, type(model)):
            raise Exception(f"Resolved model {type(model)} does not implement contract {contract}")
        if model is None:
            raise Exception("Unable to resolve model " + repr(contract))
        return model

    def create_child(self, child_name: str) -> "Space":
        child = Space(parent=self)
        self[child_name] = child
        return child

    def debug_print(self, indent: str = "", name: str = "root"):
        print(indent + f"[Space] {name} <{hex(id(self))}>")
        for k, o in self._items.items():
            if isinstance(o, SceneObject) or isinstance(o, Space):
                o.debug_print(indent + "    ", name=k)
            else:
                print(indent + "    " + f"[Value] {k} {repr(o)}")
    
    def items_deep(self):
        """Iterates over key-value pairs recursively"""
        for k, v in self._items.items():
            yield (k, v)
            if isinstance(v, Space):
                for ck, cv in v.items_deep():
                    yield (ck, cv)

    def __cotains__(self, value):
        return value in self._items

    def __getitem__(self, key):
        if key not in self._items:
            raise Exception("Given key does not exist in the space")
        return self._items[key]

    def __setitem__(self, key, value):
        if type(key) is not str or str(key) == "":
            raise Exception("Spaces can only contain non-empty string keys")
        self._items[key] = value

        # set parent space for geometries
        if isinstance(value, Geometry):
            value.embed_into(self)
    
    def __enter__(self):
        self._previous_space_context = Space.current
        Space.current = self
        return self
    
    def __exit__(self, *args):
        Space.current = self._previous_space_context