from dataclasses import dataclass
from ..SceneObject import SceneObject
from typing import List
from .Part import Part
from .ScoreMeasure import ScoreMeasure


@dataclass
class Score(SceneObject):
    """Represents a whole music score (a single MusicXML file)"""
    
    parts: List[Part]
    "List of parts that this score consists of"

    @property
    def staff_count(self) -> int:
        """How many staves does a single system have"""
        return sum(p.staff_count for p in self.parts)
    
    def first_staff_index_of_part(self, part: Part) -> int:
        """Given a part returns the staff index (zero-based) of the first staff
        in that part, relative to the system (the score, all the instruments)"""
        index = 0

        for p in self.parts:
            if p is part:
                return index
            else:
                index += p.staff_count

        raise Exception("The given part is not a part of this score.")
    
    def get_score_measure(self, measure_index: int) -> ScoreMeasure:
        """
        Returns a view of the score from an all-parts temporal perspective.
        This view is constructed each time you call this method and is not
        stored in the data model.
        """
        return ScoreMeasure.from_part_measures([
            self.parts[i].measures[measure_index]
            for i in range(len(self.parts))
        ])

    def validate(self):
        "Runs various consistency validation checks on the entire score"
        self._validate_consistent_measure_count()
        
        for p in self.parts:
            p.validate()
    
    def _validate_consistent_measure_count(self):
        """All parts must have the same number of measures"""
        counts = [len(p.measures) for p in self.parts]
        
        if len(counts) == 0:
            return
        
        first_count = counts[0]
        for c in counts:
            if c != first_count:
                raise Exception(
                    "The score's parts have differing number of measures."
                )
