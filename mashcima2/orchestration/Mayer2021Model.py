from .Model import Model
from ..scene.ViewBox import ViewBox
from ..scene.Sprite import Sprite
from ..geometry.Rectangle import Rectangle
from ..geometry.Vector2 import Vector2
from ..geometry.Transform import Transform
from ..loading.MusicXmlLoader import MusicXmlLoader
from ..synthesis.page.NaiveStafflinesSynthesizer \
    import NaiveStafflinesSynthesizer
from ..synthesis.layout.Mashcima1LayoutSynthesizer \
    import Mashcima1LayoutSynthesizer
from ..rendering.BitmapRenderer import BitmapRenderer
import numpy as np


class Mayer2021Model(Model):
    """
    Synthesizer that uses the original Mashcima 1 algorithm from:

    > Jiří Mayer and Pavel Pecina. Synthesizing Training Data for Handwritten
    > Music Recognition. 16th International Conference on Document Analysis
    > and Recognition, ICDAR 2021. Lausanne, September 8-10, pp. 626-641, 2021.
    """
    def __init__(self):
        super().__init__()

        # TODO: define interfaces and register their implementations
        # self.container.register(...)

    def __call__(self, annotation_file_path: str) -> np.ndarray:
        return super().__call__(annotation_file_path)

    def call(self, annotation_file_path: str):

        # TODO: move sub-component initialization into the IoC configuration
        # and then resolve them from the IoC container here
        
        # A4 paper portrait, mm
        self.scene.add(ViewBox(Rectangle(0, 0, 210, 297)))

        # create two debug boxes on the page
        img1 = Sprite.debug_box(self.scene.space, Rectangle(10, 10, 100, 20))
        img2 = Sprite.debug_box(self.scene.space, Rectangle(50, 25, 100, 20))
        img2.transform = Transform.rotateDegCC(5).then(img2.transform)

        # load the symbolic part
        staff = MusicXmlLoader().load_file(annotation_file_path)
        self.scene.add(staff)

        # synthesize stafflines
        stafflines = NaiveStafflinesSynthesizer().synthesize(
            self.scene.space, Vector2(10, 100), 100
        )
        Mashcima1LayoutSynthesizer().synthesize(stafflines, staff)
        
        # add objects to scene that are transitively linked from objects
        # already in scene
        self.scene.add_closure()

        # render PNG
        renderer = BitmapRenderer()
        bitmap = renderer.render(self.scene)

        return bitmap
