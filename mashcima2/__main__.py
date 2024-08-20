# import matplotlib.pyplot as plt
import numpy as np
# from .synthesis.glyph
import cv2
from .rendering.BitmapRenderer import BitmapRenderer
from .scene.ViewBox import ViewBox
from .geometry.Rectangle import Rectangle
from .geometry.Vector2 import Vector2
from .geometry.Transform import Transform
from .scene.Scene import Scene
from .scene.AffineSpace import AffineSpace
from .synthesis.glyph.MuscimaPPGlyphSynthesizer import MuscimaPPGlyphSynthesizer
from .assets.AssetRepository import AssetRepository
from .assets.datasets.MuscimaPP import MuscimaPP

assets = AssetRepository.default()
muscima_pp = assets.resolve_bundle(MuscimaPP)

scene = Scene()
scene.add(ViewBox(Rectangle(0, 0, 210, 297)))
MuscimaPPGlyphSynthesizer(muscima_pp).synthesize(
    glyph_class="smufl::noteheadBlack",
    parent_space=scene.space,
    transform=Transform.translate(Vector2(100, 100))
)
scene.add_closure()
bitmap = BitmapRenderer().render(scene)
cv2.imwrite("testing/render.png", bitmap)


# ===========================================
exit()

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




from mashcima2.orchestration.Mayer2021Model import Mayer2021Model

model = Mayer2021Model()

bitmap = model("testing/input.musicxml")

print(bitmap.shape)
cv2.imwrite("testing/render.png", bitmap)
