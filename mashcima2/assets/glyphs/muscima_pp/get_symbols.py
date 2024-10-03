from muscima.io import CropObject
from typing import List, Type, TypeVar, Callable, Optional
from .MppPage import MppPage
from .MppGlyphMetadata import MppGlyphMetadata
from .MppGlyphClass import MppGlyphClass
from mashcima2.scene.Sprite import Sprite
from mashcima2.geometry.Point import Point
from mashcima2.scene.visual.Glyph import Glyph
from mashcima2.scene.visual.Notehead import Notehead
from mashcima2.scene.visual.RestGlyph import RestGlyph
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
    glyph_class: MppGlyphClass,
    sprite_origin: Optional[Callable[[CropObject], Point]] = None
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
                bitmap_origin=(
                    sprite_origin(o) if sprite_origin else Point(0.5, 0.5)
                ),
                dpi=MUSCIMA_PP_DPI
            )
        ]
        glyphs.append(glyph)

    return glyphs


def _get_y_position_of_staff_line(
    page: MppPage,
    obj: CropObject,
    line_from_top: int = 0
) -> int:
    """
    Given a CropObject it finds the y-coordinate of the corresponding staff line
    """
    staff = page.get_outlink_to(obj, "staff")
    staff_line = None
    line = 0
    for l in staff.outlinks:
        resolved_link = page.id_lookup[l]
        if resolved_link.clsname == "staff_line":
            if line == line_from_top:  # counted from top, from zero
                staff_line = resolved_link
                break
            line += 1
    assert staff_line is not None
    return (staff_line.top + staff_line.bottom) // 2


def _get_symbols_centered_on_line(
    page: MppPage,
    clsname: str,
    glyph_type: Type[T],
    glyph_class: MppGlyphClass,
    line_from_top: int,
    when_center_outside_recenter: bool = False
) -> List[T]:
    """
    Returns list of symbols with given clsname centered on given line index
    """
    def _sprite_origin(obj: CropObject) -> Point:
        line_y = _get_y_position_of_staff_line(
            page,
            obj,
            line_from_top=line_from_top
        )
        origin_y = (line_y - obj.top) / obj.height
        if (origin_y < 0 or origin_y > 1) and when_center_outside_recenter:
            origin_y = 0.5
        return Point(0.5, origin_y)

    return _crop_objects_to_single_sprite_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname == clsname
        ],
        page=page,
        glyph_type=glyph_type,
        glyph_class=glyph_class,
        sprite_origin=_sprite_origin
    )


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


def get_whole_rests(page: MppPage) -> List[RestGlyph]:
    glyphs = _get_symbols_centered_on_line(
        page,
        clsname="whole_rest",
        glyph_type=RestGlyph,
        glyph_class=MppGlyphClass.wholeRest,
        line_from_top=1
    )
    # NOTE: these checks were in the old version, but they make situation
    # worse, because some rests are so big that they should be over the staff,
    # not touching the staff. So it's better to keep the original center.
    # for glyph in glyphs:
    #     origin = glyph.sprites[0].bitmap_origin
    #     if origin.y < -0.5 or origin.y > 0.5:
    #         glyph.sprites[0].bitmap_origin = Point(origin.x, 0.0)
    return glyphs


def get_half_rests(page: MppPage) -> List[RestGlyph]:
    glyphs = _get_symbols_centered_on_line(
        page,
        clsname="half_rest",
        glyph_type=RestGlyph,
        glyph_class=MppGlyphClass.halfRest,
        line_from_top=2
    )
    # NOTE: these checks were in the old version, but they make situation
    # worse, because some rests are so big that they should be over the staff,
    # not touching the staff. So it's better to keep the original center.
    # for glyph in glyphs:
    #     origin = glyph.sprites[0].bitmap_origin
    #     if origin.y < -1.5 or origin.y > 0.5:
    #         glyph.sprites[0].bitmap_origin = Point(origin.x, 1.0)
    return glyphs


def get_quarter_rests(page: MppPage) -> List[RestGlyph]:
    return _get_symbols_centered_on_line(
        page,
        clsname="quarter_rest",
        glyph_type=RestGlyph,
        glyph_class=MppGlyphClass.quarterRest,
        line_from_top=2,
        when_center_outside_recenter=True
    )


def get_eighth_rests(page: MppPage) -> List[RestGlyph]:
    return _get_symbols_centered_on_line(
        page,
        clsname="8th_rest",
        glyph_type=RestGlyph,
        glyph_class=MppGlyphClass.eighthRest,
        line_from_top=2,
        when_center_outside_recenter=True
    )

def get_sixteenth_rests(page: MppPage) -> List[RestGlyph]:
    return _get_symbols_centered_on_line(
        page,
        clsname="16th_rest",
        glyph_type=RestGlyph,
        glyph_class=MppGlyphClass.sixteenthRest,
        line_from_top=2,
        when_center_outside_recenter=True
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


def get_g_clefs(page: MppPage) -> List[Glyph]:
    return _get_symbols_centered_on_line(
        page,
        clsname="g-clef",
        glyph_type=Glyph,
        glyph_class=MppGlyphClass.gClef,
        line_from_top=3
    )


def get_f_clefs(page: MppPage) -> List[Glyph]:
    return _get_symbols_centered_on_line(
        page,
        clsname="f-clef",
        glyph_type=Glyph,
        glyph_class=MppGlyphClass.fClef,
        line_from_top=1
    )


def get_c_clefs(page: MppPage) -> List[Glyph]:
    return _crop_objects_to_single_sprite_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname == "c-clef"
        ],
        page=page,
        glyph_type=Glyph,
        glyph_class=MppGlyphClass.cClef
    )
