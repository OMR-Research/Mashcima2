from enum import Enum


class NoteheadSide(str, Enum):
    """Represents the left or right side of a notehead. This type is used to
    codify on what side of the notehead a given stem should be attached."""
    left = "left"
    right = "right"
