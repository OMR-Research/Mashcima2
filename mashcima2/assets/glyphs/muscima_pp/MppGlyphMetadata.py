from dataclasses import dataclass
from mashcima2.scene.SceneObject import SceneObject
from mashcima2.scene.visual.Glyph import Glyph
from .MppPage import MppPage
from typing import Optional
from nameof import nameof


@dataclass
class MppGlyphMetadata(SceneObject):
    """A glyph from the MUSCIMA++ dataset"""

    glyph: Glyph = None
    "The glyph that this metadata refers to"
    
    mpp_writer: int = None
    "Writer index (1 to 50) from the MUSCIMA++ dataset"

    mpp_piece: int = None
    "Music piece index (1 to 20) from the MUSCIMA++ dataset"

    def __post_init__(self):
        assert self.glyph is not None
        assert self.mpp_writer is not None
        assert self.mpp_writer >= 1 and self.mpp_writer <= 50
        assert self.mpp_piece is not None
        assert self.mpp_piece >= 1 and self.mpp_piece <= 20

    @staticmethod
    def stamp_glyph(glyph: Glyph, mpp_page: MppPage):
        # just create an instance and that's it
        # the glyph's inlinks will hold on to the instance
        MppGlyphMetadata(
            glyph=glyph,
            mpp_writer=mpp_page.mpp_writer,
            mpp_piece=mpp_page.mpp_piece
        )
    
    @staticmethod
    def of_glyph(glyph: Glyph) -> Optional["MppGlyphMetadata"]:
        return glyph.get_inlinked(
            MppGlyphMetadata,
            nameof(MppGlyphMetadata.glyph),
            at_most_one=True
        )
