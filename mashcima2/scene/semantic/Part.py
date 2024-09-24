from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List, Optional
from .Measure import Measure
from nameof import nameof


@dataclass
class Part(SceneObject):
    """Represents a single part (an instrument) of a score"""
    
    measures: List[Measure] = field(default_factory=list)
    "A part consists of a list of measures"

    staff_count: int = 1
    "Number of staves for this part (each measure should have all of them)"

    @staticmethod
    def of_measure(measure: Measure) -> Optional["Part"]:
        """Returns the part corresponding to a given measure"""
        links = [
            l for l in measure.inlinks
            if isinstance(l.source, Part) and l.name == nameof(l.source.measures)
        ]
        if len(links) == 0:
            return None
        elif len(links) == 1:
            return links[0].source
        else:
            raise Exception("There is more than one part for the measure")

    def append_measure(self, measure: Measure):
        self.measures = [*self.measures, measure]

    def validate(self):
        "Runs various consistency validation checks on the entire part"
        self._validate_consistent_staves()
    
    def _validate_consistent_staves(self):
        """All measures must have the same number of staves, ordered properly"""
        for mi, measure in enumerate(self.measures):
            # check count
            assert len(measure.staves) == self.staff_count, \
                f"Measure {mi} has {len(measure.staves)} staves but should " + \
                f"have {self.staff_count}"

            # check order and value
            for si in range(self.staff_count):
                assert measure.staves[si].staff_number == si + 1, \
                    f"Measure {mi} has incorrect staff numbers"
