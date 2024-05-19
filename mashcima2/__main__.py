from .geometry.Transform import Transform
from .scene.Scene import Scene
from .geometry.Rectangle import Rectangle
from .scene.Sprite import Sprite
from .scene.ViewBox import ViewBox
# from .rendering.InkscapeRenderer import InkscapeRenderer
from .rendering.BitmapRenderer import BitmapRenderer
import cv2


# from .assets.AssetRepository import AssetRepository
# from .assets.datasets.MuscimaPP import MuscimaPP
# assets = AssetRepository.default()
# mpp = assets.resolve_bundle(MuscimaPP)


# from .scene.SceneObject import SceneObject
# from .scene.visual.Notehead import Notehead
# from .scene.semantic.Note import Note
# from fractions import Fraction

# note = Note(duration=Fraction(1, 1))
# notehead = Notehead(sprite=None, note=note)

# # print(notehead, notehead.inlinks, notehead.outlinks)
# # print(note, note.inlinks, note.outlinks)

# print(notehead.note)
# print(Notehead.of_note(note))


# prepare a scene
scene = Scene()
scene.add(ViewBox(Rectangle(0, 0, 210, 297))) # A4 paper portrait, mm
img1 = Sprite.debug_box(scene.space, Rectangle(10, 10, 100, 20))
img2 = Sprite.debug_box(scene.space, Rectangle(50, 25, 100, 20))
scene.add_closure()

img2.transform = Transform.rotateDegCC(5).then(img2.transform)


# render PNG
renderer = BitmapRenderer()
bitmap = renderer.render(scene)
print(bitmap.shape)
cv2.imwrite("test.png", bitmap)
