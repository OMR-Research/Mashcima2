from typing import Set, Type
from .GlyphSynthesizer import GlyphSynthesizer, T
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.assets.AssetRepository import AssetRepository
from mashcima2.assets.glyphs.muscima_pp.MuscimaPPGlyphs import MuscimaPPGlyphs
from mashcima2.assets.glyphs.muscima_pp.MppGlyphClass import MppGlyphClass
from .SmuflGlyphClass import SmuflGlyphClass
import random
import copy


class MuscimaPPGlyphSynthesizer(GlyphSynthesizer):
    """
    Synthesizes glyphs by sampling from the MUSCIMA++ dataset
    """
    def __init__(self, assets: AssetRepository, rng: random.Random):
        self.rng = rng
        bundle = assets.resolve_bundle(MuscimaPPGlyphs)
        self.symbol_repository = bundle.load_symbol_repository()
    
    @property
    def supported_glyphs(self) -> Set[str]:
        return {
            # noteheads
            SmuflGlyphClass.noteheadWhole,
            SmuflGlyphClass.noteheadHalf,
            SmuflGlyphClass.noteheadBlack,
            MppGlyphClass.noteheadEmpty,
            MppGlyphClass.noteheadFull,
            
            # barlines
            SmuflGlyphClass.barlineSingle,
        }
    
    def synthesize_glyph(
        self,
        glyph_class: str,
        expected_glyph_type: Type[T] = Glyph
    ) -> T:
        # pick a glyph from the symbol repository
        glyph = self._synthesize_glyph(glyph_class)

        # make a copy of that glyph before returning
        glyph_copy = copy.deepcopy(glyph)

        # adjust its glyph class to match what the user wants
        # (e.g. SMUFL instead of MUSCIMA++)
        glyph_copy.glyph_class = glyph_class

        # verify before returning
        self.verify_glyph_type_and_class(
            glyph_class,
            expected_glyph_type,
            glyph_copy
        )

        return glyph_copy
    
    def _synthesize_glyph(self, glyph_class: str) -> Glyph:
        # noteheads
        if glyph_class == SmuflGlyphClass.noteheadWhole \
        or glyph_class == SmuflGlyphClass.noteheadHalf \
        or glyph_class == MppGlyphClass.noteheadEmpty:
            return self.rng.choice(self.symbol_repository.empty_noteheads)
        
        if glyph_class == SmuflGlyphClass.noteheadBlack \
        or glyph_class == MppGlyphClass.noteheadFull:
            return self.rng.choice(self.symbol_repository.full_noteheads)
        
        # barlines
        if glyph_class == SmuflGlyphClass.barlineSingle:
            return self.rng.choice(self.symbol_repository.normal_barlines)
        
        raise Exception("Unsupported glyph class: " + glyph_class)
