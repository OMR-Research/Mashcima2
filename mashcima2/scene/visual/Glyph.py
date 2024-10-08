from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from ..Sprite import Sprite
from ..AffineSpace import AffineSpace
from typing import List


@dataclass
class Glyph(SceneObject):
    """
    A glyph is a visual unit of the notation. It can be detected, segmented,
    classified.

    It is: notehead, stem, flag, ledger line, staffline,
    But it's also: notehead-stem-flag ligature, ledger-notehead-stem ligature
    Since a ligature cannot be easily broken down into its parts,
    it's a glyph of its own.

    The glyph has its own local coordinate space, relative to which all spatial
    information is represented.

    Also, see the definition of a glyph:
    https://en.wikipedia.org/wiki/Glyph
    """

    glyph_class: str
    "Class name used for classification"

    space: AffineSpace = field(default_factory=AffineSpace)
    """The local space of the glyph, where the origin point is some important
    point of the glyph (depends on the glyph class, e.g. center of a notehead
    or the base of a stem)"""

    sprites: List[Sprite] = field(default_factory=list)
    "Images that should be rendered for the glyph."

    # TODO: DetectionBox
    # TODO: SegmentationMask

    def __post_init__(self):
        assert type(self.glyph_class) is str, "Glyph class must be string"
