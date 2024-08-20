import abc
from typing import Set
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.geometry.Transform import Transform
from mashcima2.scene.AffineSpace import AffineSpace


class GlyphSynthesizer(abc.ABC):
    """
    Represents an interface for a synthesizer that produces glyphs
    """
    @abc.abstractmethod
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
        raise NotImplementedError
    
    @property
    @abc.abstractmethod
    def supported_glyphs(self) -> Set[str]:
        """Returns the set of supported glyphs"""
        raise NotImplementedError
