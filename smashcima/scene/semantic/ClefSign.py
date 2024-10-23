from enum import Enum


class ClefSign(str, Enum):
    """The appearance of the clef sign (G, F, C)"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/clef-sign/
    
    G = "G"
    F = "F"
    C = "C"
    percussion = "percussion"
    TAB = "TAB"
    jianpu = "jianpu"
