from dataclasses import dataclass
from ..SceneObject import SceneObject
from fractions import Fraction


@dataclass
class Durable(SceneObject):
    """Durable is something that has duration (note or rest)"""
    type_duration: str
    fractional_duration: Fraction
    duration_dots: int
    measure_onset: Fraction

    # TODO: time-modification from tuplets
