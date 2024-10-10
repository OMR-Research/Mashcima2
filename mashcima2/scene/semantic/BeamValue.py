from enum import Enum


class BeamValue(str, Enum):
    """Type of beam behaviour at a note"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/beam-value/
    backward_hook = "backward hook"
    begin = "begin"
    continue_beam = "continue"
    end = "end"
    forward_hook = "forward hook"
