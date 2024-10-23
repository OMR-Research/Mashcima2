from smashcima.scene.semantic.Clef import Clef
from smashcima.scene.semantic.Score import Score
from smashcima.scene.semantic.Event import Event
from smashcima.scene.semantic.Staff import Staff
from smashcima.scene.semantic.ScoreEvent import ScoreEvent
from smashcima.scene.semantic.Note import Note
from smashcima.scene.semantic.Rest import Rest
from smashcima.scene.semantic.MeasureRest import MeasureRest
from smashcima.scene.visual.Stafflines import Stafflines
from smashcima.scene.visual.Notehead import Notehead
from smashcima.scene.visual.RestGlyph import RestGlyph
from smashcima.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from smashcima.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from .ColumnBase import ColumnBase
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import random


# Notehead alignment
# ------------------
# There are 3 columns of noteheads, the center one is the default one and
# if a stem is pointing up, it's placed right of it; if down, it's placed
# left. If there is a one-tone step between two notes, then one of the noteheads
# kicks off to one of the side columns. Which direction it's kicked off depends
# on the stem direction, because the note has to kick off on the other side
# of the stem.


@dataclass
class _NoteheadContext:
    notehead: Notehead
    "The notehead"
    
    note: Note
    "A representative note of that notehead (WLOG the first one)"

    clef: Clef
    "What clef applies to the note"

    stafflines: Stafflines
    "What stafflines is the note placed onto"

    kick_asif_stem_up: bool
    "Perform kick off to the right, else to the left"

    kick_off: int = 0
    "Horizontal notehead column position: -1, 0, +1 for the three columns"


@dataclass
class _RestContext:
    glyph: RestGlyph
    "The rest glyph"

    clef: Clef
    "What clef applies to the rest"

    stafflines: Stafflines
    "What stafflines is the rest placed onto"


class NotesColumn(ColumnBase):
    def __post_init__(self):
        self.notehead_contexts: List[_NoteheadContext] = []
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

    def add_notehead(self, notehead: Notehead):
        assert len(notehead.notes) > 0

        self.glyphs.append(notehead)
        
        note = notehead.notes[0]
        event = Event.of_durable(note, fail_if_none=True)
        staff = Staff.of_durable(note, fail_if_none=True)
        clef = event.attributes.clefs[staff.staff_number]
        stafflines = self.get_stafflines_of_glyph(notehead)

        # TODO: get from stem orientation
        # for whole notes assume true
        kick_asif_stem_up=True

        self.notehead_contexts.append(_NoteheadContext(
            notehead=notehead,
            note=note,
            clef=clef,
            stafflines=stafflines,
            kick_asif_stem_up=kick_asif_stem_up
        ))

    def _position_glyphs(self):
        for stafflines in self.staves:
            self.kick_off_noteheads_on_stafflines(stafflines)
        self.position_noteheads()
        self.position_rests()
    
    def kick_off_noteheads_on_stafflines(self, stafflines: Stafflines):
        contexts = [
            c for c in self.notehead_contexts
            if c.stafflines is stafflines
        ]
        contexts.sort(key=lambda c: c.note.pitch.get_linear_pitch())
        
        # lets go from bottom up and kick notes off the center line
        last_linear_pitch = -2
        last_was_kicked_off = True
        for ctx in contexts:
            linear_pitch = ctx.note.pitch.get_linear_pitch()

            # reset kick off
            ctx.kick_off = 0

            # if the previous pitch was kicked off,
            # then the current does not need to be
            if last_was_kicked_off:
                last_was_kicked_off = False
                last_linear_pitch = linear_pitch
                continue

            # ok, now if we have enough space, we also don't need to kick off
            if abs(linear_pitch - last_linear_pitch) >= 2:
                last_was_kicked_off = False
                last_linear_pitch = linear_pitch
                continue

            # now we are definitely tight, we need to kick off
            # just we need to figure out the direction
            last_was_kicked_off = True
            last_linear_pitch = linear_pitch

            ctx.kick_off = 1 if ctx.kick_asif_stem_up else -1
        
    def position_noteheads(self):
        for ctx in self.notehead_contexts:
            notehead = ctx.notehead
            sl = ctx.stafflines

            # TODO: take kick-off into account
            pitch_position = ctx.clef.pitch_to_pitch_position(ctx.note.pitch)
            notehead.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=pitch_position,
                time_position=self.time_position # + self.rng.random() * 2 - 1
            )
    
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


def synthesize_notes_column(
    staves: List[Stafflines],
    rng: random.Random,
    glyph_synthesizer: GlyphSynthesizer,
    score: Score,
    score_event: ScoreEvent
) -> NotesColumn:
    column = NotesColumn(staves, rng.random())

    # === noteheads ===

    # notehead merging logic
    # (when two voices share a notehead)
    _all_noteheads: Dict[Tuple[int, int], Notehead] = dict()
    
    def _get_notehead(note: Note, stafflines_index: int) -> Optional[Notehead]:
        nonlocal _all_noteheads
        linear_pitch = note.pitch.get_linear_pitch()
        return _all_noteheads.get((stafflines_index, linear_pitch))

    def _store_notehead(note: Note, stafflines_index: int, notehead: Notehead):
        nonlocal _all_noteheads
        linear_pitch = note.pitch.get_linear_pitch()
        _all_noteheads[(stafflines_index, linear_pitch)] = notehead

    # go through all the notes and create notehead glyphs
    for event in score_event.events:
        for durable in event.durables:
            if isinstance(durable, Note):
                note: Note = durable
                stafflines_index = score.staff_index_of_durable(note)
                notehead = _get_notehead(note, stafflines_index)

                # another note for an existing notehead
                if notehead is not None:
                    notehead.notes = [*notehead.notes, note]
                    continue
                
                # new notehead for a note
                notehead = glyph_synthesizer.synthesize_glyph(
                    SmuflGlyphClass.notehead_from_type_duration(
                        note.type_duration
                    ).value,
                    expected_glyph_type=Notehead
                )
                notehead.space.parent_space = staves[stafflines_index].space
                notehead.notes = [*notehead.notes, note]
                _store_notehead(note, stafflines_index, notehead)
    
    # add noteheads to the column
    for notehead in _all_noteheads.values():
        column.add_notehead(notehead)

    # === rests ===

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
            rest = glyph_synthesizer.synthesize_glyph(
                glyph_class.value,
                expected_glyph_type=RestGlyph
            )
            rest.space.parent_space = stafflines.space
            rest.rest = durable
            column.add_rest(rest)
    
    return column
