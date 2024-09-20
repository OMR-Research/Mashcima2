from dataclasses import dataclass
from ..SceneObject import SceneObject
from fractions import Fraction
from .TypeDuration import TypeDuration


@dataclass
class Durable(SceneObject):
    """Durable is something that has duration (note or rest)"""
    type_duration: TypeDuration
    
    # TODO: load/define these:
    fractional_duration: Fraction
    duration_dots: int
    measure_onset: Fraction

    # TODO: time-modification from tuplets
