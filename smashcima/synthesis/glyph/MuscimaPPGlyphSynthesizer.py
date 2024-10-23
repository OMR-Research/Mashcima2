from typing import Set, Type, Dict
from .GlyphSynthesizer import GlyphSynthesizer, T
from smashcima.scene.visual.Glyph import Glyph
from smashcima.assets.AssetRepository import AssetRepository
from smashcima.assets.glyphs.muscima_pp.MuscimaPPGlyphs import MuscimaPPGlyphs
from smashcima.assets.glyphs.muscima_pp.MppGlyphClass import MppGlyphClass
from .SmuflGlyphClass import SmuflGlyphClass
from smashcima.synthesis.style.MuscimaPPStyleDomain import MuscimaPPStyleDomain
import random
import copy


_QUERY_TO_MPP_LOOKUP: Dict[str, str] = {
    # barlines
    SmuflGlyphClass.barlineSingle.value: MppGlyphClass.thinBarline.value,
    MppGlyphClass.thinBarline.value: MppGlyphClass.thinBarline.value,

    # clefs    (clefs ignore the normal/small distinction)
    SmuflGlyphClass.gClef: MppGlyphClass.gClef,
    SmuflGlyphClass.gClefSmall: MppGlyphClass.gClef,
    MppGlyphClass.gClef: MppGlyphClass.gClef,
    SmuflGlyphClass.fClef: MppGlyphClass.fClef,
    SmuflGlyphClass.fClefSmall: MppGlyphClass.fClef,
    MppGlyphClass.fClef: MppGlyphClass.fClef,
    SmuflGlyphClass.cClef: MppGlyphClass.cClef,
    SmuflGlyphClass.cClefSmall: MppGlyphClass.cClef,
    MppGlyphClass.cClef: MppGlyphClass.cClef,

    # noteheads
    SmuflGlyphClass.noteheadWhole.value: MppGlyphClass.noteheadEmpty.value,
    SmuflGlyphClass.noteheadHalf.value: MppGlyphClass.noteheadEmpty.value,
    SmuflGlyphClass.noteheadBlack.value: MppGlyphClass.noteheadFull.value,
    MppGlyphClass.noteheadEmpty.value: MppGlyphClass.noteheadEmpty.value,
    MppGlyphClass.noteheadFull.value: MppGlyphClass.noteheadFull.value,

    # rests
    SmuflGlyphClass.restWhole.value: MppGlyphClass.wholeRest.value,
    SmuflGlyphClass.restHalf.value: MppGlyphClass.halfRest.value,
    SmuflGlyphClass.restQuarter.value: MppGlyphClass.quarterRest.value,
    SmuflGlyphClass.rest8th.value: MppGlyphClass.eighthRest.value,
    SmuflGlyphClass.rest16th.value: MppGlyphClass.sixteenthRest.value,
    MppGlyphClass.wholeRest.value: MppGlyphClass.wholeRest.value,
    MppGlyphClass.halfRest.value: MppGlyphClass.halfRest.value,
    MppGlyphClass.quarterRest.value: MppGlyphClass.quarterRest.value,
    MppGlyphClass.eighthRest.value: MppGlyphClass.eighthRest.value,
    MppGlyphClass.sixteenthRest.value: MppGlyphClass.sixteenthRest.value,
}


class MuscimaPPGlyphSynthesizer(GlyphSynthesizer):
    """
    Synthesizes glyphs by sampling from the MUSCIMA++ dataset
    """
    def __init__(
        self,
        assets: AssetRepository,
        mpp_style_domain: MuscimaPPStyleDomain,
        rng: random.Random,
    ):
        bundle = assets.resolve_bundle(MuscimaPPGlyphs)
        self.symbol_repository = bundle.load_symbol_repository()
        "The symbol repository used for synthesis"

        self.mpp_style_domain = mpp_style_domain
        "Dictates which MUSCIMA++ writer to use for synthesis"
        
        self.rng = rng
        "RNG used for randomization"
    
    @property
    def supported_glyphs(self) -> Set[str]:
        return set(_QUERY_TO_MPP_LOOKUP.keys())
    
    def synthesize_glyph(
        self,
        glyph_class: str,
        expected_glyph_type: Type[T] = Glyph
    ) -> T:
        assert type(glyph_class) is str, "Requested glyph class must be str type"

        # pick a glyph from the symbol repository
        if glyph_class in _QUERY_TO_MPP_LOOKUP:
            glyph = self.pick(_QUERY_TO_MPP_LOOKUP[glyph_class])
        else:
            raise Exception("Unsupported glyph class: " + glyph_class)

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
    
    def pick(self, glyph_class: str) -> Glyph:
        """Picks a random glyph from the symbol repository according to the
        current writer"""
        # get the list of glyphs to choose from
        # (if writer is missing this class, fall back on all writers)
        glyphs = self.symbol_repository.glyphs_by_class_and_writer.get(
            (glyph_class, self.mpp_style_domain.current_writer)
        ) or self.symbol_repository.glyphs_by_class.get(glyph_class)

        if glyphs is None or len(glyphs) == 0:
            raise Exception(
                f"The glyph class {glyph_class} is not present in " + \
                "the symbol repository"
            )
        
        # pick a random glyph from the list
        return self.rng.choice(glyphs)
