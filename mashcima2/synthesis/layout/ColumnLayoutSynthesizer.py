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
from mashcima2.geometry.Point import Point
from mashcima2.geometry.Vector2 import Vector2
from mashcima2.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from mashcima2.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.rendering.traverse_sprites import traverse_sprites
from typing import List
import abc
import random
from dataclasses import dataclass


@dataclass
class _GlyphOnStafflines:
    glyph: Glyph
    stafflines: Stafflines

    def __post_init__(self):
        assert self.glyph.space.parent_space is self.stafflines.space, \
            "The given glyph must be on the given stafflines"


class _Column(abc.ABC):
    def __init__(self, staves: List[Stafflines], rng_seed: float):
        self.staves = staves
        "Reference to the list of stafflines we render onto"
        
        self.glyphs_on_stafflines: List[_GlyphOnStafflines] = []
        "List of all glyphs within this column"

        self.time_position = 0
        "Where on the staff (staves) is this column placed"

        self.rng_seed = rng_seed
        "Seed for the local RNG used for glyph positioning"

        self.rng = random.Random(self.rng_seed)
        "The RNG that should be used for randomizing glyph positioning"

        # temporal dimensions of the column, must be manually recalculated
        self.width = 0
        self.left_width = 0
        self.right_width = 0

        self.__post_init__()
    
    def __post_init__(self):
        # can be overriden in child classes
        pass
    
    def add_glyph(self, glyph: Glyph, stafflines: Stafflines):
        """Adds a glyph into the column"""
        self.glyphs_on_stafflines.append(
            _GlyphOnStafflines(glyph=glyph, stafflines=stafflines)
        )
    
    def recalculate_dimensions(self):
        """Updates all the width values"""
        # reset all
        self.width = 0
        self.left_width = 0
        self.right_width = 0

        # map sprite corners to the stafflines space
        # relative to its time position
        points: List[Vector2] = []
        for glyph_on_stafflines in self.glyphs_on_stafflines:
            glyph = glyph_on_stafflines.glyph
            stafflines = glyph_on_stafflines.stafflines
            column_origin = stafflines.staff_coordinate_system.get_transform(
                0,
                self.time_position
            ).apply_to(Vector2(0, 0))
            for (sprite, transform) in traverse_sprites(
                glyph.space,
                include_pixels_transform=True,
                include_sprite_transform=True,
                include_root_space_transform=True # all the way to staff space
            ):
                corners = [
                    transform.apply_to(Vector2(0, 0)),
                    transform.apply_to(Vector2(sprite.pixel_width, 0)),
                    transform.apply_to(Vector2(0, sprite.pixel_height)),
                    transform.apply_to(
                        Vector2(sprite.pixel_width, sprite.pixel_height)
                    )
                ]
                corners = [p - column_origin for p in corners]
                points += corners

        # recalculate widths
        if len(points) > 0:
            self.left_width = -min(p.x for p in points)
            self.right_width = max(p.x for p in points)
            self.width = self.left_width + self.right_width

    def position_glyphs(self):
        """Positions glyphs on staves according to the column's time position"""
        # reset RNG before any positioning
        self.rng = random.Random(self.rng_seed)
        self._position_glyphs()
        self.recalculate_dimensions()

    @abc.abstractmethod
    def _position_glyphs(self):
        """Glyph positioning implementation"""
        raise NotImplementedError
    
    def place_debug_boxes(self):
        """For debugging purposes - places sprites that visualize the column"""
        for stafflines in self.staves:
            topleft = stafflines.staff_coordinate_system.get_transform(
                pitch_position=4,
                time_position=self.time_position - self.left_width
            ).apply_to(Vector2(0, 0))
            bottomright = stafflines.staff_coordinate_system.get_transform(
                pitch_position=-4,
                time_position=self.time_position + self.right_width
            ).apply_to(Vector2(0, 0))
            Sprite.debug_box(
                space=stafflines.space,
                rectangle=Rectangle(
                    x=topleft.x,
                    y=topleft.y,
                    width=bottomright.x - topleft.x,
                    height=bottomright.y - topleft.y
                ),
                fill_color=(0, 0, 0, 0),
                border_width=0.2 # mm
            )


class _NotesColumn(_Column):
    def __post_init__(self):
        self.noteheads: List[Notehead] = []
    
    def add_notehead(self, notehead: Notehead):
        self.add_glyph(notehead, notehead.stafflines)
        self.noteheads.append(notehead)

    def _position_glyphs(self):
        for i, n in enumerate(self.noteheads):
            sl = n.stafflines
            n.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=i*2, # TODO: pitch position
                time_position=self.time_position + self.rng.random() * 2 - 1
            )


class _BarlinesColumn(_Column):
    def _position_glyphs(self):
        for glyph_on_stafflines in self.glyphs_on_stafflines:
            barline = glyph_on_stafflines.glyph
            sl = glyph_on_stafflines.stafflines

            barline.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=0, # centered on the staff
                time_position=self.time_position
            )


class _ClefsColumn(_Column):
    pass


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
            
            # column for the barlines
            column = self.synthesize_barlines(staves, score)
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

        # TODO: DEBUG ONLY: place debug rectangles around columns
        # for column in columns:
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

    def synthesize_barlines(
        self,
        staves: List[Stafflines],
        score: Score
    ) -> _Column:
        column = _BarlinesColumn(staves, self.rng.random())

        for stafflines in staves:
            barline = self.glyph_synthesizer.synthesize_glyph(
                SmuflGlyphClass.barlineSingle.value,
                expected_glyph_type=Glyph
            )
            barline.space.parent_space = stafflines.space
            column.add_glyph(barline, stafflines)

        return column
