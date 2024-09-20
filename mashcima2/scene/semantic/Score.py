from dataclasses import dataclass
from ..SceneObject import SceneObject
from typing import List
from .Part import Part


@dataclass
class Score(SceneObject):
    """Represents a whole music score (a single MusicXML file)"""
    
    parts: List[Part]
    "List of parts that this score consists of"

    def validate(self):
        "Runs various consistency validation checks on the entire score"
        self._validate_consistent_measure_count()
    
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
