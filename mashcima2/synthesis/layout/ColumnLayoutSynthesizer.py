from mashcima2.scene.visual.Stafflines import Stafflines
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.scene.semantic.Staff import Staff
from mashcima2.scene.semantic.Note import Note
from mashcima2.scene.semantic.Rest import Rest
from mashcima2.scene.semantic.Score import Score
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.scene.Sprite import Sprite
from mashcima2.scene.visual.HalfNote import HalfNote
from mashcima2.scene.visual.System import System
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from mashcima2.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from mashcima2.scene.visual.Glyph import Glyph
from typing import List
import abc


class _Column(abc.ABC):
    def __init__(self):
        self.glyphs: List[Glyph] = []

        self.time_position = 0
        "Where on the staff (staves) is this column placed"

    @abc.abstractmethod
    def position_glyphs(self):
        """Positions glyphs on staves according to the column's time position"""
        raise NotImplementedError


class _NotesColumn(_Column):
    def __init__(self):
        super().__init__()
        self.noteheads: List[Glyph] = []
    
    def add_notehead(self, notehead: Glyph):
        self.noteheads.append(notehead)

    def position_glyphs(self):
        pass


class _ClefsColumn(_Column):
    pass


# TODO: define a layout synthesizer interface and inherit
# IN -> semantic scene object graph
# OUT -> visual scene object graph
class ColumnLayoutSynthesizer:
    def __init__(self, glyph_synthesizer: GlyphSynthesizer):
        self.glyph_synthesizer = glyph_synthesizer

    # TODO: this API is still under development
    # def synthesize(self, stafflines: Stafflines, staff: Staff):
    #     time_position = 5
    #     TIME_STEP = 7

    #     for measure in staff.measures:
    #         for durable in measure.durables:
    #             if isinstance(durable, Note):
    #                 dummy_half_note_synthesizer(
    #                     stafflines.space,
    #                     stafflines.staff_coordinate_system.get_transform(
    #                         -4, # TODO: pitch to pitch_position
    #                         time_position
    #                     )
    #                 )
    #                 time_position += TIME_STEP
    #             elif isinstance(durable, Rest):
    #                 pass
    #         # TODO: barline
    #         time_position += TIME_STEP
    
    def synthesize_system(
        self,
        staves: List[Stafflines],
        score: Score,
        start_on_measure: int
    ) -> System:
        """Synthesizes a single system of music onto the provided staves"""
        system = System()

        assert len(staves) == score.staves_per_system, \
            "Given staves do not match the required number of staves per system"

        # TODO: dummy notehead synthesis
        for i in range(10):
            glyph = self.glyph_synthesizer.synthesize(SmuflGlyphClass.noteheadBlack)
            stafflines = staves[0]
            glyph.space.parent_space = stafflines.space
            glyph.space.transform = stafflines.staff_coordinate_system.get_transform(
                pitch_position=0.0,
                time_position=i * 5.0
            )

        return system
