from dataclasses import dataclass
from fractions import Fraction
from .Sprite import Sprite
from typing import List


#############
# Framework #
#############

@dataclass
class SceneObject:
    scene: "Scene"
    id: int


class Scene:
    """Container for scene objects, tracks backward references"""
    def __init__(self):
        self.objects: List[SceneObject] = []
    
    def append(self, object: SceneObject):
        self.objects.append(object)
        # TODO: extract all backward references and keep them around
    
    def find_parents_of(self, parent_type, child_object):
        # TODO
        pass


#####################
# Semantic entities #
#####################

@dataclass
class Note(SceneObject):
    pitch: str
    duration: Fraction


######################
# Graphical entities #
######################

# elementary graphical entities:
# - sprite (Sprite)
# - bbox (object annotation) (DetectionBox)
# - semantic segmentation mask (SegmentationMask)
# - 2D space (2DSpace)

# semantic graphical entities:
# - notehead
# - stafflines


@dataclass
class Notehead(SceneObject, Sprite):
    note: Note
    "Relationship to the corresponding note"

    @staticmethod
    def one_of(note: Note) -> "Notehead":
        return note.scene.find_parents_of(
            parent_type=Notehead,
            child_object=note
        )[0] # TODO: return None if missing



######################
# Sample synthesizer #
######################

def notehead_synthesizer() -> Notehead:
    # TODO: sample some sprite from symbol repo
    return Notehead()

# def staff_synthesizer() -> Staff:
#     pass


###################
# Sample renderer #
###################

def bitmap_renderer(scene: Scene):
    # go through all scene objects that are a sprite
    # transform each sprite from its local space up the 2D space hierarchy
    # to the scene's 2D space
    # composit sprite images onto a canvas
    # return the composition
    pass

def musicxml_renderer(scene: Scene):
    # go through the semantic graph of objects and extract MusicXML
    pass

def primus_agnostic_renderer(scene: Scene):
    # go through the semantic graph and extract primus agnostic annotations,
    # one for each staff
    pass
