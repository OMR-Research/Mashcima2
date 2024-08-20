from typing import Set
from .GlyphSynthesizer import GlyphSynthesizer
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.scene.Sprite import Sprite
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.assets.datasets.MuscimaPP import MuscimaPP


class MuscimaPPGlyphSynthesizer(GlyphSynthesizer):
    """
    Synthesizes glyphs by sampling from the MUSCIMA++ dataset
    """
    def __init__(self, muscima_pp: MuscimaPP):
        self.muscima_pp = muscima_pp
    
    def synthesize(
        self,
        glyph_class: str,
        parent_space: AffineSpace,
        transform: Transform
    ) -> Glyph:
        """Synthesizes a new glyph
        
        :glyph_class What glyph to synthesize.
        :parent_space The affine space that will become the parent
            of the new glyph
        :transform Where to place the new glyph in the parent space.
            The origin point of the glyph depends on the glyph class.
        """
        local_space = AffineSpace(
            parent_space=parent_space,
            transform=transform
        )
        sprites = [
            Sprite.debug_box(local_space, Rectangle(-1, -1, 2, 2)) # notehead
        ]
        notehead = Notehead(
            space=local_space,
            sprites=sprites
        )
        return notehead
    
    @property
    def supported_glyphs(self) -> Set[str]:
        return {
            "smufl::noteheadBlack"
        }
