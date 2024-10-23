from enum import Enum


class StemValue(str, Enum):
    """Orientation of a stem for a note"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/stem-value/
    down = "down"
    up = "up"
    double = "double"
    none = "none"
