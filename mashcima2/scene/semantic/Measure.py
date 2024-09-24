from dataclasses import dataclass, field
from typing import Optional
from fractions import Fraction
from ..SceneObject import SceneObject
from .Durable import Durable
from .Event import Event
from .Staff import Staff
from typing import List
from nameof import nameof


@dataclass
class Measure(SceneObject):
    """A measure of music for a single instrument (a single part)"""

    events: List[Event] = field(default_factory=list)
    "Links to all events within this measure"

    staves: List[Staff] = field(default_factory=list)
    """Links to all staves within this measure"""

    @staticmethod
    def of_staff(staff: Staff) -> Optional["Measure"]:
        """Returns the measure corresponding to a given staff"""
        links = [
            l for l in staff.inlinks
            if isinstance(l.source, Measure) and l.name == nameof(l.source.staves)
        ]
        if len(links) == 0:
            return None
        elif len(links) == 1:
            return links[0].source
        else:
            raise Exception("There is more than one measure for the staff")

    def add_durable(
        self,
        durable: Durable,
        onset: Fraction,
        staff_number: int
    ):
        """Adds a durable into the measure"""
        event = self.get_or_create_event(onset)
        event.durables = [*event.durables, durable]

        staff = self.get_or_create_staff(staff_number)
        staff.durables = [*staff.durables, durable]

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
    
    def get_or_create_staff(self, staff_number: int) -> Staff:
        """Returns staff with the given staff number"""
        matches = [s for s in self.staves if s.staff_number == staff_number]
        if len(matches) > 1:
            raise Exception("There are multiple staves with the same number!")
        elif len(matches) == 1:
            return matches[0]
        else:
            staff = Staff(staff_number=staff_number)
            self.staves = [*self.staves, staff]
            self.sort_staves_by_number()
            return staff
    
    def sort_staves_by_number(self):
        """Sorts staves by number, ascending"""
        self.staves.sort(key=lambda e: e.staff_number)
