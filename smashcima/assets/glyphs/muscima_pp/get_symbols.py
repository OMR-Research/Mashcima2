from muscima.io import CropObject
from typing import List, Type, TypeVar, Callable, Optional
from .MppPage import MppPage
from .MppGlyphMetadata import MppGlyphMetadata
from .MppGlyphClass import MppGlyphClass
from smashcima.scene.Sprite import Sprite
from smashcima.scene.ScenePoint import ScenePoint
from smashcima.geometry.Point import Point
from smashcima.scene.visual.Glyph import Glyph
from smashcima.scene.visual.LineGlyph import LineGlyph
from smashcima.scene.visual.Notehead import Notehead
from smashcima.scene.visual.RestGlyph import RestGlyph
from smashcima.scene.visual.Stem import Stem
from smashcima.scene.visual.Beam import Beam
from smashcima.scene.visual.BeamHook import BeamHook
from smashcima.scene.visual.LedgerLine import LedgerLine
from .get_line_endpoints import get_line_endpoints
import numpy as np
import cv2


T = TypeVar("T", bound=Glyph)
U = TypeVar("U", bound=LineGlyph)

# source:
# https://pages.cvc.uab.es/cvcmuscima/index_database.html
MUSCIMA_PP_DPI = 300

TALL_BARLINE_THRESHOLD_PX = 150
BEAM_HOOK_MAX_WIDTH_PX = 25


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
        MppGlyphMetadata.stamp_glyph(glyph, page, int(o.objid))
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


def _crop_objects_to_line_glyphs(
    crop_objects: List[CropObject],
    page: MppPage,
    glyph_type: Type[U],
    glyph_class: MppGlyphClass,
    horizontal_line: bool,
    in_increasing_direction: bool,
) -> List[U]:
    glyphs: List[U] = []

    for o in crop_objects:
        # prepare the glyph
        glyph = glyph_type(
            glyph_class=glyph_class.value
        )
        MppGlyphMetadata.stamp_glyph(glyph, page, int(o.objid))
        sprite = Sprite(
            space=glyph.space,
            bitmap=_mpp_mask_to_sprite_bitmap(o.mask),
            bitmap_origin=Point(0.5, 0.5),
            dpi=MUSCIMA_PP_DPI
        )
        glyph.sprites = [sprite]

        # extract endpoints
        blurred_mask = cv2.medianBlur(o.mask, 5) # smooth out (5x5 window)
        points = get_line_endpoints(blurred_mask)
        points.sort(
            key=lambda p: p.x if horizontal_line else p.y,
            reverse=not in_increasing_direction
        )
        if len(points) < 2:
            # print(
            #     "Skipping line:", o.uid,
            #     "Has points:", len(points),
            #     "Is:", o.clsname
            # )
            continue
        glyph.start_point = ScenePoint(
            point=sprite.get_pixels_to_scene_transform().apply_to(points[0]),
            space=glyph.space
        )
        glyph.end_point = ScenePoint(
            point=sprite.get_pixels_to_scene_transform().apply_to(points[-1]),
            space=glyph.space
        )

        # return the glyph
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
    _EXCLUDE = set([
        # this is a double barline, accidentally annotated as simple
        "MUSCIMA-pp_1.0___CVC-MUSCIMA_W-32_N-09_D-ideal___70"
    ])
    return _crop_objects_to_single_sprite_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname in ["thin_barline"]
            and o.height < TALL_BARLINE_THRESHOLD_PX
            and o.uid not in _EXCLUDE
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


def get_stems(page: MppPage) -> List[Stem]:
    return _crop_objects_to_line_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname in ["stem"]
        ],
        page=page,
        glyph_type=Stem,
        glyph_class=MppGlyphClass.stem,
        horizontal_line=False, # vertical line
        in_increasing_direction=False # pointing upwards
    )


def get_beams(page: MppPage) -> List[Beam]:
    return _crop_objects_to_line_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname in ["beam"]
            and o.width > BEAM_HOOK_MAX_WIDTH_PX
        ],
        page=page,
        glyph_type=Beam,
        glyph_class=MppGlyphClass.beam,
        horizontal_line=True, # horizontal line
        in_increasing_direction=True # pointing to the right
    )


def get_beam_hooks(page: MppPage) -> List[BeamHook]:
    return _crop_objects_to_line_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname in ["beam"]
            and o.width <= BEAM_HOOK_MAX_WIDTH_PX
        ],
        page=page,
        glyph_type=BeamHook,
        glyph_class=MppGlyphClass.beamHook,
        horizontal_line=True, # horizontal line
        in_increasing_direction=True # pointing to the right
    )


def get_ledger_lines(page: MppPage) -> List[LedgerLine]:
    return _crop_objects_to_line_glyphs(
        crop_objects=[
            o for o in page.crop_objects
            if o.clsname in ["ledger_line"]
        ],
        page=page,
        glyph_type=LedgerLine,
        glyph_class=MppGlyphClass.ledgerLine,
        horizontal_line=True, # horizontal line
        in_increasing_direction=True # pointing to the right
    )
