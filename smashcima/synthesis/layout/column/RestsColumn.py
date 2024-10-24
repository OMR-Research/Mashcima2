from smashcima.scene.semantic.Clef import Clef
from smashcima.scene.semantic.Score import Score
from smashcima.scene.semantic.Event import Event
from smashcima.scene.semantic.Staff import Staff
from smashcima.scene.semantic.ScoreEvent import ScoreEvent
from smashcima.scene.semantic.Rest import Rest
from smashcima.scene.visual.Stafflines import Stafflines
from smashcima.scene.visual.RestGlyph import RestGlyph
from smashcima.scene.visual.LedgerLine import LedgerLine
from smashcima.synthesis.glyph.SmashcimaGlyphClass import SmashcimaGlyphClass
from smashcima.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from smashcima.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from smashcima.synthesis.glyph.LineSynthesizer import LineSynthesizer
from smashcima.geometry.Point import Point
from smashcima.random_between import random_between
from .ColumnBase import ColumnBase
from typing import List
from dataclasses import dataclass
import random


@dataclass
class _RestContext:
    glyph: RestGlyph
    "The rest glyph"

    clef: Clef
    "What clef applies to the rest"

    stafflines: Stafflines
    "What stafflines is the rest placed onto"


class RestsColumn(ColumnBase):
    def __post_init__(self):
        self.rest_contexts: List[_RestContext] = []

    def add_rest(self, glyph: RestGlyph):
        assert glyph.rest is not None
        
        self.glyphs.append(glyph)

        rest = glyph.rest
        event = Event.of_durable(rest, fail_if_none=True)
        staff = Staff.of_durable(rest, fail_if_none=True)
        clef = event.attributes.clefs[staff.staff_number]
        stafflines = self.get_stafflines_of_glyph(glyph)

        self.rest_contexts.append(_RestContext(
            glyph=glyph,
            clef=clef,
            stafflines=stafflines
        ))
    
    def _position_glyphs(self):
        self.position_rests()
    
    def position_rests(self):
        for ctx in self.rest_contexts:
            rest = ctx.glyph.rest
            glyph = ctx.glyph
            clef = ctx.clef
            sl = ctx.stafflines

            display_pitch = rest.display_pitch \
                or RestGlyph.default_display_pitch(
                    clef, rest.type_duration
                )
            pitch_position = RestGlyph.display_pitch_to_glyph_pitch_position(
                clef, display_pitch, rest.type_duration
            )

            glyph.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=pitch_position,
                time_position=self.time_position
            )


def synthesize_rests_column(
    column: RestsColumn,
    staves: List[Stafflines],
    glyph_synthesizer: GlyphSynthesizer,
    line_synthesizer: LineSynthesizer,
    score: Score,
    score_event: ScoreEvent,
    rng: random.Random
):
    # for all the rests (including measure rests)
    for event in score_event.events:
        for durable in event.durables:
            if not isinstance(durable, Rest): # inlcudes MeasureRest
                continue
            
            stafflines_index = score.staff_index_of_durable(durable)
            stafflines = staves[stafflines_index]

            # create the rest
            glyph_class = SmuflGlyphClass.rest_from_type_duration(
                durable.type_duration
            )
            rest_glyph = glyph_synthesizer.synthesize_glyph(
                glyph_class.value,
                expected_glyph_type=RestGlyph
            )
            rest_glyph.space.parent_space = stafflines.space
            rest_glyph.rest = durable
            column.add_rest(rest_glyph)

            # create ledger line for whole/half rests
            # (and attach it under the glyph space for simplicity)
            _synthesize_ledger_line_if_necessary(
                rest=durable,
                rest_glyph=rest_glyph,
                glyph_class=glyph_class,
                line_synthesizer=line_synthesizer,
                rng=rng
            )


def _synthesize_ledger_line_if_necessary(
    rest: Rest,
    rest_glyph: RestGlyph,
    glyph_class: SmuflGlyphClass,
    line_synthesizer: LineSynthesizer,
    rng: random.Random
):
    # the rest is not whole nor half, no ledger line needed
    if glyph_class not in [SmuflGlyphClass.restWhole, SmuflGlyphClass.restHalf]:
        return

    event = Event.of_durable(rest, fail_if_none=True)
    staff = Staff.of_durable(rest, fail_if_none=True)
    clef = event.attributes.clefs[staff.staff_number]
    display_pitch = rest.display_pitch \
        or RestGlyph.default_display_pitch(
            clef, rest.type_duration
        )
    pitch_position = RestGlyph.display_pitch_to_glyph_pitch_position(
        clef, display_pitch, rest.type_duration
    )

    # the rest is still within the staff, no ledgerline needed
    if abs(pitch_position) < 4:
        return
        
    width = rest_glyph.get_bbox_in_space(rest_glyph.space).width \
        * random_between(1.2, 2.5, rng)
    
    line = line_synthesizer.synthesize_line(
        glyph_type=LedgerLine,
        glyph_class=SmashcimaGlyphClass.ledgerLine.value,
        start_point=Point(-width / 2, 0),
        end_point=Point(width / 2, 0)
    )
    line.space.parent_space = rest_glyph.space
    line.affected_rest = rest_glyph