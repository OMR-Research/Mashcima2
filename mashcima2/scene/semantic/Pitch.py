from enum import Enum
from dataclasses import dataclass, field


class Octave(int, Enum):
    """Octave number of the scientific picth notation"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/octave/
    o0 = 0
    o1 = 1
    o2 = 2
    o3 = 3
    o4 = 4
    o5 = 5
    o6 = 6
    o7 = 7
    o8 = 8
    o9 = 9


class Step(str, Enum):
    """Step name of the scientific pitch notation"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/step/
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class Alter(int, Enum):
    """Semitone alter number (based on MusicXML)"""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/semitones/
    flat = -1
    none = 0
    sharp = 1


@dataclass
class Pitch:
    """Represents an audible pitch in the scientific pitch notation."""
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pitch/
    octave: Octave
    step: Step
    alter: Alter = field(default=Alter.none)

    @staticmethod
    def parse(octave: str, step: str, alter: str | None = None) -> "Pitch":
        return Pitch(
            octave=Octave(int(octave)),
            step=Step(step),
            alter=Alter.none if alter is None else Alter(int(alter))
        )
