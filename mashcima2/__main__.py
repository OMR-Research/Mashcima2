from .geometry.Transform import Transform
from .scene.Scene import Scene
from .geometry.Rectangle import Rectangle
from .geometry.Vector2 import Vector2
from .scene.Sprite import Sprite
from .scene.ViewBox import ViewBox
# from .rendering.InkscapeRenderer import InkscapeRenderer
from .rendering.BitmapRenderer import BitmapRenderer
import cv2
from .scene.visual.HalfNote import HalfNote
from .scene.AffineSpace import AffineSpace
from .synthesis.page.NaiveStafflinesSynthesizer \
    import NaiveStafflinesSynthesizer
from .loading.MusicXmlLoader import MusicXmlLoader
from .synthesis.layout.Mashcima1LayoutSynthesizer \
    import Mashcima1LayoutSynthesizer


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
img2.transform = Transform.rotateDegCC(5).then(img2.transform)

staff = MusicXmlLoader().load_file("testing/input.musicxml")
scene.add(staff)

stafflines = NaiveStafflinesSynthesizer().synthesize(
    scene.space, Vector2(10, 100), 100
)
Mashcima1LayoutSynthesizer().synthesize(stafflines, staff)
scene.add_closure()

# render PNG
renderer = BitmapRenderer()
bitmap = renderer.render(scene)
print(bitmap.shape)
cv2.imwrite("testing/render.png", bitmap)
