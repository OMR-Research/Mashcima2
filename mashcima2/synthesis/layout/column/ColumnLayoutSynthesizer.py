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
from .Column import Column
from .ColumnBase import ColumnBase
from .BarlinesColumn import synthesize_barlines_column
from .ClefsColumn import synthesize_header_clefs
from typing import List
import random


class _NotesColumn(ColumnBase):
    def __post_init__(self):
        self.noteheads: List[Notehead] = []
    
    def add_notehead(self, notehead: Notehead):
        self.add_glyph(notehead)
        self.noteheads.append(notehead)

    def _position_glyphs(self):
        for i, n in enumerate(self.noteheads):
            sl = n.stafflines
            
            note = n.notes[0]
            event = Event.of_durable(note, fail_if_none=True)
            staff = Staff.of_durable(note, fail_if_none=True)
            clef = event.attributes.clefs[staff.staff_number]
            if isinstance(note, Note):
                pitch_position = clef.pitch_to_pitch_position(note.pitch)
            else:
                pitch_position = 0 # TODO: HACK: rests
            
            n.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=pitch_position,
                time_position=self.time_position + self.rng.random() * 2 - 1
            )


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
                    self.synthesize_notes_column(staves, score, score_event)
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

        return system

    def synthesize_notes_column(
        self,
        staves: List[Stafflines],
        score: Score,
        score_event: ScoreEvent
    ) -> _NotesColumn:
        column = _NotesColumn(staves, self.rng.random())

        for event in score_event.events:
            for durable in event.durables:
                if isinstance(durable, Note):
                    # TODO: handle shared noteheads for multiple notes
                    notehead = self.synthesize_notehead(staves, score, durable)
                    column.add_notehead(notehead)
                else:
                    print("Unhandled durable:", type(durable))
                    # TODO: hack: create notehead even for a rest...
                    notehead = self.synthesize_notehead(staves, score, durable)
                    column.add_notehead(notehead)

        return column

    def synthesize_notehead(
        self,
        staves: List[Stafflines],
        score: Score,
        note: Note
    ) -> Notehead:
        staff = Staff.of_durable(note, fail_if_none=True)
        measure = Measure.of_staff(staff, fail_if_none=True)
        part = Part.of_measure(measure, fail_if_none=True)
        
        part_index = score.parts.index(part)
        stafflines_index = sum(
            p.staff_count for p in score.parts[0:part_index]
        ) + (staff.staff_number - 1)
        stafflines = staves[stafflines_index]

        notehead = self.glyph_synthesizer.synthesize_glyph(
            SmuflGlyphClass.notehead_from_type_duration(
                note.type_duration
            ).value,
            expected_glyph_type=Notehead
        )
        notehead.space.parent_space = stafflines.space
        notehead.notes = [note]
        notehead.stafflines = stafflines
        return notehead
