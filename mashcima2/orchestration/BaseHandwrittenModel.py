from .Model import Model
from ..scene.ViewBox import ViewBox
from ..geometry.Rectangle import Rectangle
from ..geometry.Vector2 import Vector2
from ..loading.MusicXmlLoader import MusicXmlLoader
from ..synthesis.page.NaiveStafflinesSynthesizer \
    import NaiveStafflinesSynthesizer
from ..synthesis.page.StafflinesSynthesizer import StafflinesSynthesizer
from ..synthesis.layout.column.ColumnLayoutSynthesizer \
    import ColumnLayoutSynthesizer
from ..rendering.BitmapRenderer import BitmapRenderer
from ..synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from ..synthesis.glyph.MuscimaPPGlyphSynthesizer import MuscimaPPGlyphSynthesizer
from mashcima2.scene.visual.Stafflines import Stafflines
from .CallbackTrigger import CallbackTrigger
import numpy as np
from typing import List


class BaseHandwrittenModel(Model):
    """
    Model that serves as the basic handwritten music synthesizer.
    The whole framework is being developed around this model currently
    and its name might change in the future. It aims to be like Mashcima1
    with the additions of using MXL input, polyphony and postprocessing.
    """
    def __init__(self):
        super().__init__()

        self.container.type(ColumnLayoutSynthesizer)
        self.container.interface(
            StafflinesSynthesizer,
            NaiveStafflinesSynthesizer
        )
        self.container.interface(
            GlyphSynthesizer,
            MuscimaPPGlyphSynthesizer
        )

    def __call__(self, annotation_file_path: str) -> np.ndarray:
        return super().__call__(annotation_file_path)

    def call(self, annotation_file_path: str):
        # resolve services
        # (must be done first so that callback handlers are registered)
        callbacks = self.container.resolve(CallbackTrigger)
        stafflines_synthesizer = self.container.resolve(StafflinesSynthesizer)
        layout_synthesizer = self.container.resolve(ColumnLayoutSynthesizer)

        # start the synthesis
        callbacks.trigger_on_sample_begin()

        # A4 paper portrait, mm
        self.scene.add(ViewBox(Rectangle(0, 0, 210, 297)))

        # load the symbolic part
        score = MusicXmlLoader().load_file(annotation_file_path)
        self.scene.add(score)

        # synthesize stafflines
        staves: List[Stafflines] = []
        for i in range(6):
            stafflines = stafflines_synthesizer.synthesize(
                self.scene.space, Vector2(10, 30 + i * 24), 180
            )
            staves.append(stafflines)
        
        # synthesize layout
        # layout_synthesizer.synthesize(stafflines, staff)
        layout_synthesizer.synthesize_system(
            staves=staves[0:score.staff_count],
            score=score,
            start_on_measure=0
        )
        
        # add objects to scene that are transitively linked from objects
        # already in scene
        self.scene.add_closure()

        # render PNG
        renderer = BitmapRenderer(dpi=150) # TODO: DPI reduced for speed...
        bitmap = renderer.render(self.scene)

        # add white background
        # TODO: synthesize background
        mask = bitmap[:, :, 3] == 0
        bitmap[mask, :] = 255

        callbacks.trigger_on_sample_end()

        return bitmap
