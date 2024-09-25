from typing import Set, Type
from .GlyphSynthesizer import GlyphSynthesizer, T
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.Notehead import Notehead
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
            SmuflGlyphClass.noteheadWhole,
            SmuflGlyphClass.noteheadHalf,
            SmuflGlyphClass.noteheadBlack,
        }
    
    def synthesize_glyph(self, glyph_type: Type[T], glyph_class: str) -> T:
        # pick a glyph from the symbol repository
        glyph = self._synthesize_glyph(glyph_type, glyph_class)

        # make a copy of that glyph before returning
        glyph_copy = copy.deepcopy(glyph)

        # adjust its glyph class to match what the user wants
        # (e.g. SMUFL instead of MUSCIMA++)
        glyph_copy.glyph_class = glyph_class

        # verify before returning
        self.verify_glyph_type_and_class(glyph_type, glyph_class, glyph_copy)

        return glyph_copy
    
    def _synthesize_glyph(self, glyph_type: Type[T], glyph_class: str) -> T:
        if issubclass(glyph_type, Notehead):
            return self._sythesize_notehead(glyph_class)
        
        if glyph_class == SmuflGlyphClass.barlineSingle:
            return self.rng.choice(self.symbol_repository.normal_barlines)
        
        raise Exception("Unsupported glyph class: " + glyph_class)

    def _sythesize_notehead(self, glyph_class: str) -> Notehead:
        if glyph_class == SmuflGlyphClass.noteheadWhole \
        or glyph_class == SmuflGlyphClass.noteheadHalf \
        or glyph_class == MppGlyphClass.noteheadEmpty:
            return self.rng.choice(self.symbol_repository.empty_noteheads)
        
        if glyph_class == SmuflGlyphClass.noteheadBlack \
        or glyph_class == MppGlyphClass.noteheadFull:
            return self.rng.choice(self.symbol_repository.full_noteheads)
        
        raise Exception("Unsupported notehead: " + glyph_class)
