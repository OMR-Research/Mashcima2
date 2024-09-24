from muscima.io import CropObject
from typing import List
from .MppPage import MppPage
from .MppGlyphMetadata import MppGlyphMetadata
from mashcima2.scene.Sprite import Sprite
from mashcima2.geometry.Point import Point
from mashcima2.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.Notehead import Notehead
import numpy as np


# source:
# https://pages.cvc.uab.es/cvcmuscima/index_database.html
MUSCIMA_PP_DPI = 300


def mpp_mask_to_sprite_bitmap(mask: np.ndarray):
    """True/False pixel mask to black on transparent BGRA uint8 bitmap"""
    assert len(mask.shape) == 2
    assert mask.dtype == np.uint8
    alpha = mask * 255
    color = np.zeros_like(mask)
    bitmap = np.stack([color, color, color, alpha], axis=2)
    return bitmap


def get_black_noteheads(page: MppPage) -> List[Notehead]:
    crop_objects: List[CropObject] = [
        o for o in page.crop_objects
        if o.clsname == "notehead-full"
        and not page.has_outlink_to(o, "ledger_line")
    ]

    noteheads: List[Notehead] = []
    for o in crop_objects:
        notehead = Notehead(assigned_glyph_class=SmuflGlyphClass.noteheadBlack)
        MppGlyphMetadata.stamp_glyph(notehead, page)
        notehead.sprites = [
            Sprite(
                space=notehead.space,
                bitmap=mpp_mask_to_sprite_bitmap(o.mask),
                bitmap_origin=Point(0.5, 0.5),
                dpi=MUSCIMA_PP_DPI
            )
        ]
        noteheads.append(notehead)

    return noteheads
