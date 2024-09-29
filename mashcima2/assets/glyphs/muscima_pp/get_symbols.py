from muscima.io import CropObject
from typing import List, Type, TypeVar
from .MppPage import MppPage
from .MppGlyphMetadata import MppGlyphMetadata
from .MppGlyphClass import MppGlyphClass
from mashcima2.scene.Sprite import Sprite
from mashcima2.geometry.Point import Point
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.Notehead import Notehead
import numpy as np


T = TypeVar("T", bound=Glyph)

# source:
# https://pages.cvc.uab.es/cvcmuscima/index_database.html
MUSCIMA_PP_DPI = 300

TALL_BARLINE_THRESHOLD_PX = 150


def _mpp_mask_to_sprite_bitmap(mask: np.ndarray):
    """True/False pixel mask to black on transparent BGRA uint8 bitmap"""
    assert len(mask.shape) == 2
    assert mask.dtype == np.uint8
    alpha = mask * 255
    color = np.zeros_like(mask)
    bitmap = np.stack([color, color, color, alpha], axis=2)
    return bitmap


def _crop_objects_to_single_sprite_glyphs(
    crop_objects: List[CropObject],
    page: MppPage,
    glyph_type: Type[T],
    glyph_class: MppGlyphClass
) -> List[T]:
    glyphs: List[T] = []

    for o in crop_objects:
        glyph = glyph_type(
            glyph_class=glyph_class.value
        )
        MppGlyphMetadata.stamp_glyph(glyph, page)
        glyph.sprites = [
            Sprite(
                space=glyph.space,
                bitmap=_mpp_mask_to_sprite_bitmap(o.mask),
                bitmap_origin=Point(0.5, 0.5),
                dpi=MUSCIMA_PP_DPI
            )
        ]
        glyphs.append(glyph)

    return glyphs


################################################
# Code that actually extracts required symbols #
################################################


def get_full_noteheads(page: MppPage) -> List[Notehead]:
    return _crop_objects_to_single_sprite_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname == "notehead-full"
            and not page.has_outlink_to(o, "ledger_line")
        ],
        page=page,
        glyph_type=Notehead,
        glyph_class=MppGlyphClass.noteheadFull
    )


def get_empty_noteheads(page: MppPage) -> List[Notehead]:
    return _crop_objects_to_single_sprite_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname == "notehead-empty"
            and not page.has_outlink_to(o, "ledger_line")
        ],
        page=page,
        glyph_type=Notehead,
        glyph_class=MppGlyphClass.noteheadEmpty
    )


def get_normal_barlines(page: MppPage) -> List[Glyph]:
    return _crop_objects_to_single_sprite_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname in ["thin_barline"]
            and o.height < TALL_BARLINE_THRESHOLD_PX
        ],
        page=page,
        glyph_type=Glyph,
        glyph_class=MppGlyphClass.thinBarline
    )
