from .geometry.Transform import Transform
from .scene.Scene import Scene
from .geometry.Rectangle import Rectangle
from .scene.Sprite import Sprite
# from .rendering.InkscapeRenderer import InkscapeRenderer
from .rendering.BitmapRenderer import BitmapRenderer
import cv2


# prepare a scene
scene = Scene(
    view_box=Rectangle(0, 0, 210, 297) # A4 paper portrait, mm
)
img1 = Sprite.debug_box(rectangle=Rectangle(10, 10, 100, 20))
img2 = Sprite.debug_box(rectangle=Rectangle(50, 25, 100, 20))
scene.append(img1)
scene.append(img2)

img2.transform = Transform.rotateDegCC(5).then(img2.transform)


# render PNG
renderer = BitmapRenderer()
bitmap = renderer.render(scene)
print(bitmap.shape)
cv2.imwrite("test.png", bitmap)
