from .NaiveLineSynthesizer import NaiveLineSynthesizer, T
from mashcima2.geometry.Vector2 import Vector2
from mashcima2.assets.AssetRepository import AssetRepository
from mashcima2.assets.glyphs.muscima_pp.MuscimaPPGlyphs import MuscimaPPGlyphs
from mashcima2.assets.glyphs.muscima_pp.MppGlyphClass import MppGlyphClass
from mashcima2.assets.glyphs.muscima_pp.LineList import LineList
from mashcima2.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from mashcima2.synthesis.glyph.SmashcimaGlyphClass import SmashcimaGlyphClass
from typing import Type, Dict
import random
import copy

# TODO: HACK
from mashcima2.synthesis.glyph.GlyphSynthesizer \
    import GlyphSynthesizer

_QUERY_TO_MPP_LOOKUP: Dict[str, str] = {
    SmuflGlyphClass.stem.value: MppGlyphClass.stem.value,
    SmashcimaGlyphClass.beam.value: MppGlyphClass.beam.value,
    SmashcimaGlyphClass.beamHook.value: MppGlyphClass.beamHook.value,
}


class MuscimaPPLineSynthesizer(NaiveLineSynthesizer):
    """
    Synthesizes line glyphs by sampling from the MUSCIMA++ dataset
    """
    def __init__(
        self,
        assets: AssetRepository,
        rng: random.Random,
        # callbacks: CallbackTrigger
        glyph_synth: GlyphSynthesizer # TODO: HACK
    ):
        self.rng = rng
        "RNG used for randomization"

        # TODO: cache this and reuse
        bundle = assets.resolve_bundle(MuscimaPPGlyphs)
        self.symbol_repository = bundle.load_symbol_repository()
        "The symbol repository used for synthesis"

        # self.current_writer = self.pick_writer()
        "What MPP writer to use for glyph synthesis"

        # TODO: HACK: move writer selection up to a dedicated system
        # listen to model synthesis callbacks
        # callbacks.add_callback(self)
        self.glyph_synth = glyph_synth
    
    # TODO: HACK
    @property
    def current_writer(self) -> int:
        return self.glyph_synth.current_writer
    
    def pick(
        self,
        glyph_type: Type[T],
        glyph_class: str,
        delta: Vector2,
    ) -> T:
        # translate glyph class
        if glyph_class not in _QUERY_TO_MPP_LOOKUP:
            raise Exception("Unsupported glyph class: " + glyph_class)
        mpp_glyph_class = _QUERY_TO_MPP_LOOKUP[glyph_class]

        # select the proper glyph list
        glyphs = self.symbol_repository.glyphs_by_class_and_writer.get(
            (mpp_glyph_class, self.current_writer)
        ) or self.symbol_repository.glyphs_by_class.get(mpp_glyph_class)
        assert isinstance(glyphs, LineList), \
            f"Got line glyphs without index for {mpp_glyph_class}"

        if glyphs is None or len(glyphs) == 0:
            raise Exception(
                f"The glyph class {glyph_class} is not present in " + \
                "the symbol repository"
            )

        # pick a random glyph from the list and copy it
        glyph = copy.deepcopy(
            glyphs.pick_line(delta.magnitude, self.rng)
        )

        assert type(glyph) is glyph_type, \
            f"Picked glyph is of different type: {type(glyph)}"
        
        # ensure the class
        glyph.glyph_class = glyph_class

        return glyph

