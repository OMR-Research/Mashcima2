import abc
from typing import Set
from .SmuflGlyph import SmuflGlyph
from mashcima2.scene.Group import Group


class GlyphSynthesizer(abc.ABC):
    """
    Represents an interface for a synthesizer that produces glyphs,
    as defined in the SMuFL specification, e.g.:
    https://www.w3.org/2019/03/smufl13/tables/individual-notes.html
    """
    @abc.abstractmethod
    def synthesize(self, glyph: SmuflGlyph) -> Group:
        raise NotImplementedError
    
    @property
    @abc.abstractmethod
    def supported_glyphs(self) -> Set[SmuflGlyph]:
        raise NotImplementedError
