from .SceneObject import SceneObject
from dataclasses import dataclass
from typing import Optional
from ..geometry.Transform import Transform


@dataclass
class AffineSpace(SceneObject):
    """
    Affine spaces define the visual hierarchy of the scene. Only visual elements
    require their presence. Their hierarchy allows for defining local spatial
    relationships in local coordinate systems. 2D affine transforms are used
    to traverse the affine space hierarchy.
    """

    parent_space: Optional["AffineSpace"] = None
    "What other space does this space belong under"

    transform: Transform = Transform.identity()
    """Transform that translates from this space's local coordinates
    to the parent's space coordinates, effectively defining the placement of
    this space within the parent space."""

    def transform_from(self, sub_space: "AffineSpace") -> Transform:
        """Returns the transform from the given space to the current space"""
        t = Transform.identity()
        
        while sub_space is not None:
            if sub_space is self:
                return t
            
            t = t.then(sub_space.transform)
            sub_space = sub_space.parent_space

        raise Exception("The given sub space is not attached under this space")
