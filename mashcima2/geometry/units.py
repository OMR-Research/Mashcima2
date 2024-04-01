from typing import Union


MILLIMETERS_IN_INCH = 24.4
"The number of millimeters in one inch"


INCHES_IN_MILLIMETER = 1 / MILLIMETERS_IN_INCH
"The number of inches in one millimeter"


def px_to_mm(pixels: Union[float, int], dpi: Union[float, int]) -> float:
    """Converts pixels to millimeters given a DPI"""
    return (float(pixels) / float(dpi)) * MILLIMETERS_IN_INCH


def mm_to_px(millimeters: Union[float, int], dpi: Union[float, int]) -> float:
    """Converts millimeters to pixels given a DPI"""
    return float(millimeters) * INCHES_IN_MILLIMETER * float(dpi)
