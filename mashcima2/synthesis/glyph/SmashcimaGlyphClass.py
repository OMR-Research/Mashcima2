from enum import Enum


class SmashcimaGlyphClass(str, Enum):
    """
    Enum that represents glyphs that are missing in the SMuFL format
    (e.g. beams and slurs) or that are specific to the synthesizer in some way"""
    
    beam = "smashcima::beam"
    beamHook = "smashcima::beamHook"
    slur = "smashcima::slur"
