from mashcima2.scene.visual.Stafflines import Stafflines
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.scene.semantic.Staff import Staff
from mashcima2.scene.semantic.Note import Note
from mashcima2.scene.semantic.Score import Score
from mashcima2.scene.semantic.ScoreEvent import ScoreEvent
from mashcima2.scene.semantic.Event import Event
from mashcima2.scene.semantic.Measure import Measure
from mashcima2.scene.semantic.Part import Part
from mashcima2.scene.visual.System import System
from mashcima2.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from mashcima2.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from ..BeamStemSynthesizer import BeamStemSynthesizer
from ...glyph.LineSynthesizer import LineSynthesizer
from .Column import Column
from .BarlinesColumn import synthesize_barlines_column
from .ClefsColumn import synthesize_header_clefs
from .NotesColumn import NotesColumn, synthesize_notes_column
from typing import List
import random


class SystemState:
    def __init__(self):
        self.columns: List[Column] = []
        "List of columns in this system"

        self.total_width = 0
        "Total width of all the columns, if stacked most tightly"
    
    def append_column(self, column: Column):
        column.position_glyphs()
        self.total_width += column.width
        self.columns.append(column)


# TODO: define a layout synthesizer interface and inherit
# IN -> semantic scene object graph
# OUT -> visual scene object graph
class ColumnLayoutSynthesizer:
    def __init__(self, glyph_synthesizer: GlyphSynthesizer, rng: random.Random):
        self.glyph_synthesizer = glyph_synthesizer
        self.rng = rng

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
        system = System() # TODO: has no fields so far...

        assert len(staves) == score.staff_count, \
            "Given staves do not match the required number of staves per system"

        state = SystemState()

        # synthesize header = start of the system signatures
        state.append_column(
            synthesize_header_clefs(
                staves, self.rng, self.glyph_synthesizer,
                score, start_on_measure
            )
        )

        # TODO: while measures fit or linebreak is reached:
        for i in range(3):
            score_measure = score.get_score_measure(start_on_measure + i)

            # construct a column for each event
            for score_event in score_measure.events:
                state.append_column(
                    synthesize_notes_column(
                        staves, self.rng, self.glyph_synthesizer,
                        score, score_event
                    )
                )
            
            # column for the barlines
            state.append_column(
                synthesize_barlines_column(
                    staves, self.rng, self.glyph_synthesizer
                )
            )

        # place columns side-by-side with fixed spacing
        SPACING = 3
        time_position = 0
        for column in state.columns:
            column.time_position = time_position + column.left_width
            column.position_glyphs()
            time_position += column.width + SPACING
        
        # stretch-out columns to fill the remaining space
        # TODO: ...

        # TODO: DEBUG ONLY: place debug rectangles around columns
        # for column in state.columns:
        #     column.place_debug_boxes()

        # === phase 2: beams and stems ===

        # TODO: get paper_space as an argument
        paper_space = staves[0].space.parent_space

        line_synthesizer = LineSynthesizer()
        beam_stem_synthesizer = BeamStemSynthesizer(line_synthesizer)

        # TODO: DEBUG: just testing out the line synth
        for column in state.columns:
            if isinstance(column, NotesColumn):
                for notehead_context in column.notehead_contexts:
                    beam_stem_synthesizer.synthesize_stem(
                        paper_space,
                        notehead_context.notehead
                    )

        return system
