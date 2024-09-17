from dataclasses import dataclass, field
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from typing import Dict


# TODO: this should be a "MppGlyphMetadata" linked to a specific glyph instance
# (because outside the core of mashcima, composition should be used over inheritance)

@dataclass
class MppGlyph(Glyph):
    """A glyph from the MUSCIMA++ dataset"""
    
    mpp_writer: int = None
    "Writer index (1 to 50) from the MUSCIMA++ dataset"

    mpp_piece: int = None
    "Document index (1 to 20) from the MUSCIMA++ dataset"

    assigned_smufl_glyph_class: SmuflGlyphClass = None
    "Class assigned to this glyph during construction"

    def __post_init__(self):
        assert self.mpp_writer is not None
        assert self.mpp_writer >= 1 and self.mpp_writer <= 50
        assert self.mpp_piece is not None
        assert self.mpp_piece >= 1 and self.mpp_piece <= 20
        assert self.assigned_smufl_glyph_class is not None
    
    @property
    def glyph_class(self) -> str:
        return str(self.assigned_smufl_glyph_class)
