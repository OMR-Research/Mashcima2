from dataclasses import dataclass
from .Durable import Durable
from .TypeDuration import TypeDuration
from fractions import Fraction


@dataclass
class MeasureRest(Durable):
    def __init__(self, fractional_duration: Fraction):
        """Constructs the measure rest, given the fractional duration of
        the whole measure (the number of beats)"""
        super().__init__(
            type_duration=TypeDuration.whole,
            duration_dots=0,
            fractional_duration=fractional_duration
        )
