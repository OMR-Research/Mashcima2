from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.LineGlyph import LineGlyph
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.scene.Sprite import Sprite
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.geometry.Point import Point
from mashcima2.geometry.Vector2 import Vector2
from mashcima2.geometry.Transform import Transform
import math


class LineSynthesizer:
    def synthesize_line(
        self,
        glyph: LineGlyph,
        start_point: Point,
        end_point: Point,
        width=0.5
    ) -> LineGlyph:
        delta = end_point.vector - start_point.vector
        length = delta.magnitude
        angle_deg = -math.atan2(delta.y, delta.x) * 180 / math.pi
        sprite_transform = Transform.rotateDegCC(angle_deg)
        glyph.space.transform = Transform.translate(start_point.vector)
        
        glyph.start_point = sprite_transform.apply_to(Point(0, 0))
        glyph.end_point = sprite_transform.apply_to(Point(length, 0))

        sprite = Sprite.rectangle(
            glyph.space,
            Rectangle(
                x=0,
                y=-width/2,
                width=length,
                height=width
            ),
            fill_color=(0, 0, 0, 255),
            dpi=300
        )
        sprite.bitmap_origin = Point(0.0, 0.5)
        sprite.transform = sprite_transform
        glyph.sprites = [sprite]

        return glyph
