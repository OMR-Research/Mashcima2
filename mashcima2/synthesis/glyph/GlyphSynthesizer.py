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
    def synthesize(self, glyph_class: str) -> Glyph:
        """Synthesizes a new glyph
        
        :glyph_class What glyph to synthesize.
        """
        raise NotImplementedError
    
    @property
    @abc.abstractmethod
    def supported_glyphs(self) -> Set[str]:
        """Returns the set of supported glyphs"""
        raise NotImplementedError
