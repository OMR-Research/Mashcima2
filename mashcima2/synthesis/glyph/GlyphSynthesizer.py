import abc
from typing import Set, Type, TypeVar
from mashcima2.scene.visual.Glyph import Glyph


T = TypeVar("T", bound=Glyph)


class GlyphSynthesizer(abc.ABC):
    """
    Represents an interface for a synthesizer that produces glyphs
    """
    @abc.abstractmethod
    def synthesize_glyph(self, glyph_type: Type[T], glyph_class: str) -> T:
        """Synthesizes a new glyph
        
        :glyph_class What glyph to synthesize.
        :glyph_type What python type does the user expect to get
        """
        raise NotImplementedError
    
    def verify_glyph_type_and_class(
        self,
        glyph_type: Type[T],
        glyph_class: str,
        glyph: Glyph
    ):
        """Call this method before returning a synthesized glyph to verify it
        has the type and class that the user expect"""
        if not isinstance(glyph, glyph_type):
            raise Exception(
                f"The user expected type {glyph_type} but got " + \
                f"{type(glyph)} instance."
            )
        if glyph.glyph_class != glyph_class:
            raise Exception(
                f"The user requested class {glyph_class} but " + \
                f"got {glyph.glyph_class} instead"
            )

    @property
    @abc.abstractmethod
    def supported_glyphs(self) -> Set[str]:
        """Returns the set of supported glyphs"""
        raise NotImplementedError
