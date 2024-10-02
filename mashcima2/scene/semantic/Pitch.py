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
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    A = "A"
    B = "B"


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
    
    def get_linear_pitch(self, with_alters=False) -> int | float:
        """Converts the pitch object into a number where 0 is A0 note
        and then it increases by one for each tone. If you include alters,
        the returned value is a float with +-0.5 based on the alter."""
        lookup = ["C", "D", "E", "F", "G", "A", "B"]
        step_index = lookup.index(self.step.value)
        linear_pitch = self.octave.value * len(lookup) + step_index
        if with_alters:
            if self.alter == Alter.sharp:
                linear_pitch += 0.5
            elif self.alter == Alter.flat:
                linear_pitch -= 0.5
        return linear_pitch
    
    def __repr__(self) -> str:
        suffix = ""
        if self.alter == Alter.sharp:
            suffix += "+1"
        if self.alter == Alter.flat:
            suffix += "-1"
        return f"Pitch({self.step.value}{self.octave.value}{suffix})"


if __name__ == "__main__":
    # Prints out all the pitches and their linear representation
    # (linear representation is used for staff positioning and conversions)
    print("Pitches and their linear representation:")
    for octave in range(9):
        for step in ["C", "D", "E", "F", "G", "A", "B"]:
            pitch = Pitch.parse(octave, step)
            print(
                repr(pitch),
                str(pitch.get_linear_pitch()).zfill(2),
                end=" | "
            )
        print()
