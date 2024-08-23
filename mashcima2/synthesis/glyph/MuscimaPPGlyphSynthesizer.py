from typing import Set
from .GlyphSynthesizer import GlyphSynthesizer
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.scene.Sprite import Sprite
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.assets.datasets.MuscimaPP import MuscimaPP
from .SmuflGlyphClass import SmuflGlyphClass


class MuscimaPPGlyphSynthesizer(GlyphSynthesizer):
    """
    Synthesizes glyphs by sampling from the MUSCIMA++ dataset
    """
    def __init__(self, muscima_pp: MuscimaPP):
        self.muscima_pp = muscima_pp
    
    def synthesize(self, glyph_class: str) -> Glyph:
        local_space = AffineSpace()
        notehead = Notehead(
            space=local_space,
            sprites=[
                # dummy notehead
                Sprite.debug_box(local_space, Rectangle(-1, -1, 2, 2))
            ]
        )
        return notehead
    
    @property
    def supported_glyphs(self) -> Set[str]:
        return {
            SmuflGlyphClass.noteWhole
        }
