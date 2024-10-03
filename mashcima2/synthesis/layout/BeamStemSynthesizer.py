from mashcima2.scene.visual.Stafflines import Stafflines
from mashcima2.scene.semantic.Staff import Staff
from mashcima2.scene.semantic.Note import Note
from mashcima2.scene.semantic.Rest import Rest
from mashcima2.scene.Scene import Scene
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.scene.Sprite import Sprite
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.geometry.Vector2 import Vector2
from mashcima2.geometry.Point import Point
from mashcima2.synthesis.glyph.LineSynthesizer import LineSynthesizer


class BeamStemSynthesizer:
    def __init__(self, line_synthesizer: LineSynthesizer):
        self.line_synthesizer = line_synthesizer

    # def synthesize_beams_and_stems(self, scene: Scene):
    #     pass

    # def synthesize_beams(self, noteheads: Notehead):
    #     pass

    def synthesize_stem(self, paper_space: AffineSpace, notehead: Notehead):
        transform = paper_space.transform_from(notehead.space)
        stem_base = transform.apply_to(Vector2(1.0, 0))
        stem_top = transform.apply_to(Vector2(1.0, -5.0))

        self.line_synthesizer.synthesize_line(
            parent_space=paper_space,
            start_point=Point.from_origin_vector(stem_base),
            end_point=Point.from_origin_vector(stem_top),
            glyph_class="dummy-line"
        )
