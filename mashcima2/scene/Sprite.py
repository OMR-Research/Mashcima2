import numpy as np

from .SceneObject import SceneObject
from ..geometry.Vector2 import Vector2
from ..geometry.Transform import Transform
from ..geometry.Point import Point
from ..geometry.Rectangle import Rectangle
from ..geometry.units import px_to_mm, mm_to_px


class Sprite(SceneObject):
    """Sprite is a bitmap image within the scene hierarchy"""
    
    def __init__(
        self,
        bitmap: np.ndarray,
        bitmap_origin: Point = Point(0.5, 0.5),
        dpi: float = 300
    ):
        super().__init__()

        assert len(bitmap.shape) == 3 # [H, W, C]
        assert bitmap.shape[2] == 4 # BGRA
        assert bitmap.dtype == np.uint8

        self.bitmap = bitmap
        "The numpy opencv BGRA bitmap for the sprite"

        self.bitmap_origin = bitmap_origin
        """Origin point of the sprite in the normalized pixel space (0.0 - 1.0),
        that is, where does the sprite overlap with the scene object's origin"""

        self.dpi = float(dpi)
        """What is the DPI of the sprite image, another words, how to scale
        the sprite - how to determine the scene size in millimeters,
        when we have the size in pixels"""
    
    @property
    def pixel_width(self) -> int:
        return self.bitmap.shape[1]
    
    @property
    def pixel_height(self) -> int:
        return self.bitmap.shape[0]
    
    @property
    def physical_width(self) -> float:
        return px_to_mm(self.pixel_width, dpi=self.dpi)
    
    @property
    def physical_height(self) -> float:
        return px_to_mm(self.pixel_height, dpi=self.dpi)
    
    def get_pixels_to_scene_transform(self) -> Transform:
        """Returns a transform that converts from local pixel space
        to local scene space"""
        return (
            Transform.translate(Vector2(
                -self.bitmap_origin.x * self.pixel_width,
                -self.bitmap_origin.y * self.pixel_height
            ))
            .then(Transform.scale(px_to_mm(1, dpi=self.dpi)))
        )

    @staticmethod
    def debug_box(
        rectangle: Rectangle,
        fill_color = (0, 0, 255, 64), # BGRA
        border_color = (0, 0, 255, 255), # BGRA
        border_width: float = 1,
        dpi: float = 300
    ) -> "Sprite":
        """Creates a rectangular box image sprite with the desired properties"""
        pixel_width = int(mm_to_px(rectangle.width, dpi=dpi))
        pixel_height = int(mm_to_px(rectangle.height, dpi=dpi))
        border_width_px = int(mm_to_px(border_width, dpi=dpi))

        bitmap = np.zeros(
            shape=(pixel_height, pixel_width, 4),
            dtype=np.uint8
        )

        # paint fill
        bitmap[:,:] = fill_color

        # paint border
        bitmap[:border_width_px, :] = border_color
        bitmap[-border_width_px:, :] = border_color
        bitmap[:, :border_width_px] = border_color
        bitmap[:, -border_width_px:] = border_color

        # create the sprite instance
        sprite = Sprite(
            bitmap=bitmap,
            bitmap_origin=Point(0.5, 0.5),
            dpi=dpi
        )
        sprite.transform = Transform.translate(rectangle.center.vector)
        return sprite
