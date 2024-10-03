from mashcima2.scene.visual.Glyph import Glyph
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
        parent_space: AffineSpace,
        start_point: Point,
        end_point: Point,
        glyph_class: str,
        width=0.5
    ) -> Glyph:
        delta = end_point.vector - start_point.vector
        length = delta.magnitude
        angle_deg = -math.atan2(delta.y, delta.x) * 180 / math.pi
        sprite_transform = Transform.rotateDegCC(angle_deg)
        glyph_transform = Transform.translate(start_point.vector)

        glyph = Glyph(glyph_class=glyph_class)
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
        glyph.space.transform = glyph_transform
        glyph.space.parent_space = parent_space
        return glyph
