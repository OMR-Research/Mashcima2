from smashcima.scene.visual.Stafflines import Stafflines
from smashcima.scene.visual.Glyph import Glyph
from smashcima.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from smashcima.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from .ColumnBase import ColumnBase
from typing import List
import random


class BarlinesColumn(ColumnBase):
    # TODO: synthesize tall barlines for piano (multi-staff parts)

    def add_barline(self, barline: Glyph):
        self.add_glyph(barline)

    def _position_glyphs(self):
        for barline in self.glyphs:
            sl = self.get_stafflines_of_glyph(barline)

            barline.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=0, # centered on the staff
                time_position=self.time_position
            )


def synthesize_barlines_column(
    staves: List[Stafflines],
    rng: random.Random,
    glyph_synthesizer: GlyphSynthesizer
) -> BarlinesColumn:
    column = BarlinesColumn(staves, rng.random())

    for stafflines in staves:
        barline = glyph_synthesizer.synthesize_glyph(
            SmuflGlyphClass.barlineSingle.value
        )
        barline.space.parent_space = stafflines.space
        column.add_barline(barline)

    return column
