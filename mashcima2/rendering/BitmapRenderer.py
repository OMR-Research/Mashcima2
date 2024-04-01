import numpy as np
import cv2
import warnings

from mashcima2.geometry.Transform import Transform
from ..scene.Scene import Scene
from ..scene.Sprite import Sprite
from ..geometry.units import mm_to_px


def _alpha_overlay_layer(canvas: np.ndarray, layer: np.ndarray) -> np.ndarray:
    # the "over" operator as described here:
    # https://en.wikipedia.org/wiki/Alpha_compositing
    
    with warnings.catch_warnings():
        # ignore division by zero warnings
        warnings.filterwarnings("ignore", "invalid value encountered")

        canvasBGR = canvas[:, :, 0:3]
        layerBGR = layer[:, :, 0:3]

        canvasA = canvas[:, :, 3:4] / 255
        layerA = layer[:, :, 3:4] / 255

        outA = canvasA + layerA * (1 - canvasA)

        outBGR = (canvasBGR*canvasA + layerBGR*layerA*(1-canvasA)) / outA

        return np.dstack((outBGR,outA*255)).astype(np.uint8)


class BitmapRenderer:
    """Renders a scene into a bitmap RGBA opencv representation"""
    def __init__(
        self,
        dpi: float = 300
    ):
        self.dpi = float(dpi)
        "DPI at which the scene should be rasterized"

    def render(self, scene: Scene) -> np.ndarray:
        canvas_width = int(mm_to_px(scene.view_box.width, dpi=self.dpi))
        canvas_height = int(mm_to_px(scene.view_box.height, dpi=self.dpi))

        canvas = np.zeros(
            shape=(canvas_height, canvas_width, 4),
            dtype=np.uint8
        )

        # converts from scene millimeter coordinate system
        # to the canvas pixel coordinate system
        scene_to_canvas_transform = (
            Transform.translate(scene.view_box.top_left_corner.vector)
                .then(Transform.scale(mm_to_px(1, dpi=self.dpi)))
        )

        # TODO: recursive and via a public iteration API with filtering by tags
        for sprite in scene._children:
            if not isinstance(sprite, Sprite):
                continue
            
            # build up a transform that converts from sprite's local pixel space
            # to canvas global pixel space, while going through the scene space
            complete_transform = (
                sprite.get_pixels_to_scene_transform()
                .then(sprite.transform) # recursive scene hierarchy transforms
                .then(scene_to_canvas_transform)
            )
            
            # TODO: this is awful slow... needs to map only the neighborhood
            # of the sprite, not the whole canvas, plus do faster alpha
            # compositing, say by using the premultiplied representation?
            print("Warping...")
            new_layer = cv2.warpAffine(
                src=sprite.bitmap,
                M=complete_transform.matrix,
                dsize=(canvas_width, canvas_height)
            )
            # TODO: specify proper interpolation !!! (say, based on the determinant)
            print("Compositing...")
            canvas = _alpha_overlay_layer(canvas, new_layer)
            print("Done.")

        return canvas
