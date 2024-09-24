from typing import Set
from .GlyphSynthesizer import GlyphSynthesizer
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.assets.AssetRepository import AssetRepository
from mashcima2.assets.glyphs.muscima_pp.MuscimaPPGlyphs import MuscimaPPGlyphs
from .SmuflGlyphClass import SmuflGlyphClass
import random
import copy


class MuscimaPPGlyphSynthesizer(GlyphSynthesizer):
    """
    Synthesizes glyphs by sampling from the MUSCIMA++ dataset
    """
    def __init__(self, assets: AssetRepository):
        bundle = assets.resolve_bundle(MuscimaPPGlyphs)
        self.symbol_repository = bundle.load_symbol_repository()
    
    def synthesize(self, glyph_class: str) -> Glyph:
        assert glyph_class == SmuflGlyphClass.noteheadBlack

        notehead = random.choice(
            self.symbol_repository.black_noteheads
        )
        return copy.deepcopy(notehead)
    
    @property
    def supported_glyphs(self) -> Set[str]:
        return {
            SmuflGlyphClass.noteheadBlack
        }
