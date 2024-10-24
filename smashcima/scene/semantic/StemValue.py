from enum import Enum


class StemValue(str, Enum):
    """Orientation of a stem for a note"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/stem-value/
    down = "down"
    up = "up"
    none = "none"

    # double = "double"
    # We assign stem orientations to chords and a chord cannot have a double
    # stem orientation. Only a notehead does. Therefore this value does not
    # make sense in our context. Should the value be encountered in MusicXML,
    # the parser must deal with it somehow. Stem synthesizers assume a chord
    # has only one well determined stem orientation.