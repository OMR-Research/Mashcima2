from smashcima.scene.ScenePoint import ScenePoint
from smashcima.scene.Sprite import Sprite
from smashcima.geometry.Rectangle import Rectangle
from smashcima.geometry.Point import Point
from smashcima.geometry.Vector2 import Vector2
from smashcima.geometry.Transform import Transform
from .LineSynthesizer import LineSynthesizer, T
from typing import Type
import cv2
import numpy as np


class NaiveLineSynthesizer(LineSynthesizer):
    def __init__(self, color=(0, 0, 0, 255), line_width=0.5, dpi=300):
        self.color = color
        "Color of the lines"
        
        self.line_width = line_width
        "The width of the synthesized naive line"

        self.dpi = dpi
        "DPI at which to synthesize the line sprite"

    def synthesize_line(
        self,
        glyph_type: Type[T],
        glyph_class: str,
        start_point: Point,
        end_point: Point
    ) -> T:
        assert type(glyph_class) is str, "Requested glyph class must be str type"

        delta = end_point.vector - start_point.vector

        glyph = self.pick(
            glyph_type=glyph_type,
            glyph_class=glyph_class,
            delta=delta
        )

        # compute the transform from the picked glyph
        # to the desired placement
        # (frame is [origin, X unit, Y unit])
        from_origin = glyph.start_point.point.vector
        from_delta = glyph.end_point.point.vector - glyph.start_point.point.vector
        from_frame = np.float32([
            list(from_origin),
            list(from_origin + from_delta),
            list(from_origin + from_delta.normalize().rotate90degCC())
        ])

        to_origin=start_point.vector
        to_delta=delta
        to_frame = np.float32([
            list(to_origin),
            list(to_origin + to_delta),
            list(to_origin + to_delta.normalize().rotate90degCC())
        ])

        matrix = cv2.getAffineTransform(from_frame, to_frame)
        glyph.space.transform = Transform(matrix)

        return glyph
    
    def pick(
        self,
        glyph_type: Type[T],
        glyph_class: str,
        delta: Vector2,
    ) -> T:
        length = delta.magnitude

        glyph = glyph_type(
            glyph_class=glyph_class
        )

        # create a sprite, lying horizontally, centered on origin
        sprite = Sprite.rectangle(
            glyph.space,
            Rectangle(
                x=-length/2,
                y=-self.line_width/2,
                width=length,
                height=self.line_width
            ),
            fill_color=self.color,
            dpi=self.dpi
        )
        glyph.sprites = [sprite]

        # set the two points
        glyph.start_point = ScenePoint(
            point=Point(-length/2, 0),
            space=glyph.space
        )
        glyph.end_point = ScenePoint(
            point=Point(length/2, 0),
            space=glyph.space
        )

        return glyph
