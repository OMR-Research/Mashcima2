from mashcima2.scene.visual.Stafflines import Stafflines
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.scene.semantic.Staff import Staff
from mashcima2.scene.semantic.Note import Note
from mashcima2.scene.semantic.Rest import Rest
from mashcima2.scene.semantic.Score import Score
from mashcima2.scene.semantic.ScoreEvent import ScoreEvent
from mashcima2.scene.semantic.Measure import Measure
from mashcima2.scene.semantic.Part import Part
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
    
    @property
    @abc.abstractmethod
    def width(self) -> float:
        raise NotImplementedError
    
    @property
    @abc.abstractmethod
    def left_width(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def position_glyphs(self):
        """Positions glyphs on staves according to the column's time position"""
        raise NotImplementedError


class _NotesColumn(_Column):
    def __init__(self):
        super().__init__()
        self.noteheads: List[Notehead] = []
    
    def add_notehead(self, notehead: Notehead):
        self.glyphs.append(notehead)
        self.noteheads.append(notehead)

    def position_glyphs(self):
        for i, n in enumerate(self.noteheads):
            sl = n.stafflines
            n.space.parent_space = sl.space
            n.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=i, # TODO: pitch position
                time_position=self.time_position
            )

    @property
    def width(self) -> float:
        return max(
            n.sprites[0].physical_width
            for n in self.noteheads
        )
    
    @property
    def left_width(self) -> float:
        return self.width / 2


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

        columns: List[_Column] = []
        total_width = 0

        # TODO: while measures fit or linebreak is reached:
        for i in range(3):
            score_measure = score.get_score_measure(start_on_measure + i)

            # construct a column for each event
            for score_event in score_measure.events:
                column = self.synthesize_notes_column(staves, score, score_event)
                column.position_glyphs()
                total_width += column.width
                columns.append(column)

        # place columns side-by-side with fixed spacing
        SPACING = 3
        time_position = 0
        for column in columns:
            column.time_position = time_position + column.left_width
            column.position_glyphs()
            time_position += column.width + SPACING
        
        # stretch-out columns to fill the remaining space
        # TODO: ...

        # TODO: dummy notehead synthesis
        # for i in range(10):
        #     glyph: Notehead = self.glyph_synthesizer.synthesize(
        #         SmuflGlyphClass.noteheadBlack
        #     )
        #     stafflines = staves[0]
        #     glyph.space.parent_space = stafflines.space
        #     glyph.space.transform = stafflines.staff_coordinate_system.get_transform(
        #         pitch_position=0.0,
        #         time_position=i * 5.0
        #     )

        return system

    def synthesize_notes_column(
        self,
        staves: List[Stafflines],
        score: Score,
        score_event: ScoreEvent
    ) -> _NotesColumn:
        column = _NotesColumn()

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
        staff = Staff.of_durable(note)
        assert staff is not None, "The note is detached from any staff"

        measure = Measure.of_staff(staff)
        assert measure is not None, "The staff is detached from any measure"

        part = Part.of_measure(measure)
        assert part is not None, "The measure is detached from any part"
        
        part_index = score.parts.index(part)
        stafflines_index = sum(
            p.staff_count for p in score.parts[0:part_index]
        ) + (staff.staff_number - 1)
        stafflines = staves[stafflines_index]

        notehead: Notehead = self.glyph_synthesizer.synthesize(
            # TODO: decide based on note type_duration
            SmuflGlyphClass.noteheadBlack
        )
        notehead.notes = [note]
        notehead.stafflines = stafflines
        return notehead
