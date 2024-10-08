from .Model import Model
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
from mashcima2.synthesis.page.SimplePageSynthesizer import SimplePageSynthesizer
from mashcima2.scene.visual.Page import Page
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

        # define default sub-synthesizers to be used by this model
        self.container.type(ColumnLayoutSynthesizer)
        self.container.interface(
            StafflinesSynthesizer,
            NaiveStafflinesSynthesizer
        )
        self.container.interface(
            GlyphSynthesizer,
            MuscimaPPGlyphSynthesizer
        )
        self.container.type(SimplePageSynthesizer)

        self.pages: List[Page] = []
        "Pages that will be synthesized during model invocation"

    def __call__(self, annotation_file_path: str) -> np.ndarray:
        return super().__call__(annotation_file_path)

    def call(self, annotation_file_path: str):
        # resolve services
        # (must be done first so that callback handlers are registered)
        callbacks = self.container.resolve(CallbackTrigger)
        layout_synthesizer = self.container.resolve(ColumnLayoutSynthesizer)
        page_synthesizer = self.container.resolve(SimplePageSynthesizer)

        # start the synthesis
        callbacks.trigger_on_sample_begin()

        # load the symbolic part
        score = MusicXmlLoader().load_file(annotation_file_path)
        self.scene.add(score)

        # until you run out of music
        # 1. synthesize a page of stafflines
        # 2. fill the page with music
        self.pages = []
        next_measure_index = 0
        next_page_origin = Vector2(0, 0)
        _PAGE_SPACING = 10 # 1cm
        while next_measure_index < score.measure_count:
            # prepare the next page of music
            page = page_synthesizer.synthesize_page(next_page_origin)
            page.space.parent_space = self.scene.space
            self.scene.add(page)
            self.pages.append(page)

            next_page_origin += Vector2(
                page.view_box.rectangle.width + _PAGE_SPACING,
                0
            )

            # synthesize music onto the page
            systems = layout_synthesizer.fill_page(
                page,
                score,
                start_on_measure=next_measure_index
            )
            next_measure_index = systems[-1].last_measure_index + 1

        # add objects to scene that are transitively linked from objects
        # already in scene
        self.scene.add_closure()

        # render PNG (only first page)
        renderer = BitmapRenderer(dpi=150) # TODO: DPI reduced for speed...
        bitmap = renderer.render(self.scene, self.pages[0].view_box)

        # add white background
        # TODO: synthesize background
        mask = bitmap[:, :, 3] == 0
        bitmap[mask, :] = 255

        callbacks.trigger_on_sample_end()

        return bitmap
