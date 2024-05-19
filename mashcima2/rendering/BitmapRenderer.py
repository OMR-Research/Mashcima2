import numpy as np
import cv2

from mashcima2.geometry.Transform import Transform
from ..scene.Scene import Scene
from ..scene.Sprite import Sprite
from ..scene.ViewBox import ViewBox
from ..geometry.units import mm_to_px


# Alpha compositing via the "over" operator + alpha premultiplication:
# https://en.wikipedia.org/wiki/Alpha_compositing


def _premultiplied_float32_alpha_overlay(canvas: np.ndarray, layer: np.ndarray):
    factor = (1 - layer[:, :, 3:4])
    canvas *= factor
    canvas += layer


def _uint8_to_float32(img: np.ndarray) -> np.ndarray:
    img = img.astype(np.float32)
    img /= 255
    return img


def _float32_to_uint8(img: np.ndarray) -> np.ndarray:
    img *= 255
    img = img.astype(np.uint8)
    return img


class BitmapRenderer:
    """Renders a scene into a bitmap RGBA opencv representation"""
    def __init__(
        self,
        dpi: float = 300
    ):
        self.dpi = float(dpi)
        "DPI at which the scene should be rasterized"

    def render(self, scene: Scene) -> np.ndarray:
        view_boxes = scene.find(ViewBox)
        assert len(view_boxes) == 1
        view_box = view_boxes[0]

        canvas_width = int(mm_to_px(view_box.rectangle.width, dpi=self.dpi))
        canvas_height = int(mm_to_px(view_box.rectangle.height, dpi=self.dpi))

        # in alpha premultiplied float32 format
        canvas = np.zeros(
            shape=(canvas_height, canvas_width, 4),
            dtype=np.float32
        )

        # converts from scene millimeter coordinate system
        # to the canvas pixel coordinate system
        scene_to_canvas_transform = (
            Transform.translate(view_box.rectangle.top_left_corner.vector)
                .then(Transform.scale(mm_to_px(1, dpi=self.dpi)))
        )

        for sprite in scene.find(Sprite):
            # TODO: have the transform be built up recursively
            # (by traversing the space hierarchy and looking for sprites)

            # build up a transform that converts from sprite's local pixel space
            # to canvas global pixel space, while going through the scene space
            complete_transform = (
                sprite.get_pixels_to_scene_transform()
                .then(sprite.transform) # recursive scene hierarchy transforms
                .then(scene_to_canvas_transform)
            )
            
            # TODO: this is awful slow... needs to map only the neighborhood
            # of the sprite, not the whole canvas (consider interpolation blur!)
            sprite_bitmap = sprite.bitmap
            sprite_bitmap = cv2.cvtColor(sprite_bitmap, cv2.COLOR_RGBA2mRGBA)
            sprite_bitmap = _uint8_to_float32(sprite_bitmap)
            new_layer = cv2.warpAffine(
                src=sprite_bitmap,
                M=complete_transform.matrix,
                dsize=(canvas_width, canvas_height),
                # flags=cv2.INTER_AREA, # use for decimation (downscaling)
                flags=cv2.INTER_LINEAR, # use for upscaling
                borderMode=cv2.BORDER_CONSTANT
            )
            # TODO: specify proper interpolation (say, based on the determinant)
            _premultiplied_float32_alpha_overlay(canvas, new_layer)

        # convert to uint8 RGBA (BGRA actually) and return
        canvas = _float32_to_uint8(canvas)
        canvas = cv2.cvtColor(canvas, cv2.COLOR_mRGBA2RGBA)
        return canvas
