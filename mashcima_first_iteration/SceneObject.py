from abc import ABC, abstractmethod


class SceneObject(ABC):
    """An object inside a scene"""
    def __init__(self):
        pass
    
    def debug_print(self, indent: str = "", name: str = ""):
        print(indent + f"[Object] {name} <{hex(id(self))}>")
