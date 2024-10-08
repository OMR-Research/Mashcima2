from mashcima2.scene.visual.Stafflines import Stafflines
from mashcima2.scene.semantic.Staff import Staff
from mashcima2.scene.semantic.Note import Note
from mashcima2.scene.semantic.Rest import Rest
from mashcima2.scene.semantic.BeamedGroup import BeamedGroup
from mashcima2.scene.semantic.ScoreMeasure import ScoreMeasure
from mashcima2.scene.semantic.Part import Part
from mashcima2.scene.semantic.Chord import Chord
from mashcima2.scene.semantic.Measure import Measure
from mashcima2.scene.semantic.StemValue import StemValue
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.scene.Sprite import Sprite
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.scene.visual.Stem import Stem
from mashcima2.scene.visual.LineGlyph import LineGlyph
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.geometry.Vector2 import Vector2
from mashcima2.geometry.Point import Point
from mashcima2.synthesis.glyph.LineSynthesizer import LineSynthesizer
from mashcima2.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from mashcima2.synthesis.glyph.SmashcimaGlyphClass import SmashcimaGlyphClass
from typing import List


class BeamStemSynthesizer:
    def __init__(self, line_synthesizer: LineSynthesizer):
        self.line_synthesizer = line_synthesizer

    def synthesize_beams_and_stems_for_measure(
        self,
        paper_space: AffineSpace,
        score_measure: ScoreMeasure
    ):
        # get all chords and beamed groups
        chords: List[Chord] = []
        groups: List[BeamedGroup] = []

        for score_event in score_measure.events:
            for event in score_event.events:
                for durable in event.durables:

                    if not isinstance(durable, Note):
                        continue

                    chord = Chord.of_note(durable)
                    if chord is not None and chord not in chords:
                        chords.append(chord)
                    
                    group = BeamedGroup.of_chord(chord)
                    if group is not None and group not in groups:
                        groups.append(group)
        
        # synthesize stems for all chords
        for chord in chords:
            self.synthesize_stem(paper_space, chord)

        # synthesize beam for each beamed group
        for group in groups:
            self.synthesize_beams(paper_space, group)

        # adjust stems for beamed groups
        for group in groups:
            self.adjust_stems_for_beam_group(group)

    # def synthesize_beams(self, noteheads: Notehead):
    #     pass

    def synthesize_stem(self, paper_space: AffineSpace, chord: Chord):
        # TODO: handle multiple noteheads
        notehead = Notehead.of_note(chord.notes[0], fail_if_none=True)

        # get stem orientation
        stem_value = chord.stem_value or self.infer_stem_orientation(chord)
        assert stem_value in [StemValue.none, StemValue.up, StemValue.down], \
            f"Invalid stem value {stem_value}, must be only up or down."
        
        # if no stem, do not render one
        if stem_value == StemValue.none:
            return

        # get both stem points
        # TODO: get a cloud of base points and aggregate to the one base point
        transform = paper_space.transform_from(notehead.space)
        stem_base = transform.apply_to(
            self.get_stem_base_point(notehead, stem_value)
        )
        stem_tip = self.get_stem_tip_point(stem_base, stem_value)

        # synthesize the stem glyph
        stem = Stem(
            glyph_class=SmuflGlyphClass.stem.value,
            space=AffineSpace(parent_space=paper_space),
            chord=chord
        )
        self.line_synthesizer.synthesize_line(
            glyph=stem,
            start_point=stem_base,
            end_point=stem_tip
        )
    
    def infer_stem_orientation(self, chord: Chord) -> StemValue:
        # NOTE: could be implemented in the future,
        # or can be subclassed and overriden by the user
        event = chord.get_event()
        onset = event.fractional_measure_onset
        measure = Measure.of_event(event, fail_if_none=True)
        part = Part.of_measure(measure, fail_if_none=True)
        measure_index = part.measures.index(measure)
        raise NotImplementedError(
            "Stem orientation inference is not supported. " + \
            "Provide explicit stem orientation in the scene semantic data. " + \
            f"Measure index: {measure_index}, onset: {onset}"
        )

    def get_stem_base_point(
        self,
        notehead: Notehead,
        orientation: StemValue
    ) -> Point:
        """Returns the point where the stem begins, in the notehead's space"""
        # TODO: account for notehead size or learn a distribution or something
        point = Point(1.0, 0)
        
        if orientation == StemValue.down:
            point = -point
        
        return point
    
    def get_stem_tip_point(
        self,
        base_point: Point,
        orientation: StemValue
    ) -> Point:
        """Returns the stem tip point in paper space, given the base point
        also in paper space"""
        # TODO: sample from a learned distribution
        delta_vector = Vector2(0.0, -5.0)

        if orientation == StemValue.down:
            delta_vector = -delta_vector
        
        return Point.from_origin_vector(base_point.vector + delta_vector)

    def synthesize_beams(self, paper_space: AffineSpace, group: BeamedGroup):
        # TODO: do a proper synth
        start = Stem.of_chord(group.chords[0], fail_if_none=True)
        end = Stem.of_chord(group.chords[-1], fail_if_none=True)

        beam = LineGlyph(
            glyph_class=SmashcimaGlyphClass.beam.value,
            space=AffineSpace(parent_space=paper_space)
        )
        self.line_synthesizer.synthesize_line(
            glyph=beam,
            start_point=paper_space.transform_from(start.space).apply_to(
                start.tip
            ),
            end_point=paper_space.transform_from(end.space).apply_to(
                end.tip
            ),
        )

    def adjust_stems_for_beam_group(self, group: BeamedGroup):
        # TODO ...
        pass
