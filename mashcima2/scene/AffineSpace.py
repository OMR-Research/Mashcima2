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
