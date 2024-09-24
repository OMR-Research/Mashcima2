from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List
from .Measure import Measure


@dataclass
class Part(SceneObject):
    """Represents a single part (an instrument) of a score"""
    
    measures: List[Measure] = field(default_factory=list)
    "A part consists of a list of measures"

    staff_count: int = 1
    "Number of staves for this part (each measure should have all of them)"

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
