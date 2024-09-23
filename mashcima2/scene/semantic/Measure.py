from dataclasses import dataclass, field
from typing import Optional
from fractions import Fraction
from ..SceneObject import SceneObject
from .Durable import Durable
from .Event import Event
from typing import List


@dataclass
class Measure(SceneObject):
    # TODO: system-staff-grandstaff measure distinction!
    
    durables: List[Durable] = field(default_factory=list)
    "Links to all durables within this measure"

    events: List[Event] = field(default_factory=list)
    "Links to all events within this measure"

    def add_durable(
        self,
        durable: Durable,
        onset: Fraction
    ):
        """Adds a durable into the measure"""
        event = self.get_or_create_event(onset)
        event.durables = [*event.durables, durable]
        self.durables = [*self.durables, durable]

    def get_or_create_event(self, onset: Fraction) -> Event:
        """Returns event with the given onset"""
        matches = [e for e in self.events if e.fractional_measure_onset == onset]
        if len(matches) > 1:
            raise Exception("There are multiple events with the same onset!")
        elif len(matches) == 1:
            return matches[0]
        else:
            event = Event(fractional_measure_onset=onset)
            self.events = [*self.events, event]
            self.sort_events_by_onset()
            return event
    
    def sort_events_by_onset(self):
        """Sorts events by onset, ascending"""
        self.events.sort(key=lambda e: e.fractional_measure_onset)
        self.events = self.events # re-order links
