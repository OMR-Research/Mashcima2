from dataclasses import dataclass
from .Event import Event
from .Measure import Measure
from typing import List, Dict
from fractions import Fraction


@dataclass
class ScoreEvent:
    """An event that spans all score parts; not in the scene, just a view"""

    fractional_measure_onset: Fraction
    """How many quarter notes from the beginning of the measure this event occus"""

    events: List[Event]
    """All measure-events that have the same onset. The number of these events
    may be less than the number of parts (not all measure-events are present
    in all the parts). The order is thus also not defined."""

    @staticmethod
    def merge_from_measures(measures: List[Measure]) -> List["ScoreEvent"]:
        dictionary: Dict[Fraction, ScoreEvent] = {}
        
        for measure in measures:
            for event in measure.events:
                key = event.fractional_measure_onset
                if key not in dictionary:
                    dictionary[key] = ScoreEvent(
                        fractional_measure_onset=key,
                        events=[]
                    )
                dictionary[key].events.append(event)

        values = list(dictionary.values())
        values.sort(key=lambda e: e.fractional_measure_onset)
        return values
