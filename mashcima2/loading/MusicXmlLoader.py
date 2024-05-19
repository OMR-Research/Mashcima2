import xml.etree.ElementTree as ET
from ..scene.semantic.Durable import Durable
from ..scene.semantic.Note import Note
from ..scene.semantic.Rest import Rest
from ..scene.semantic.Measure import Measure
from ..scene.semantic.Staff import Staff
from typing import List
from fractions import Fraction


class MusicXmlLoader:
    """Loads MusicXML into the scene data model"""

    # TODO: the loader is simple, the goal now is to have the main structure
    # in-place. For example, it currently only loads very basic monophonic
    # scores.

    def load_file(self, path: str) -> Staff:
        with open(path, "r") as file:
            tree = ET.parse(file)
        return self.load(tree)

    def load(self, tree: ET.ElementTree) -> Staff:
        # we expect a score-partwise organized MusicXML file
        assert tree.getroot().tag == "score-partwise"

        # TODO: should split to staves according to linebreaks

        measures: List[Measure] = []

        part_element = tree.getroot().find("part")
        for measure_element in part_element:
            measure = self.load_measure(measure_element)
            measures.append(measure)
        
        return Staff(measures=measures)
    
    def load_measure(self, measure_element: ET.Element) -> Measure:
        durables: List[Durable] = []

        for element in measure_element:
            if element.tag == "note":
                durable = self.load_note(element)
                durables.append(durable)
            elif element.tag == "attributes":
                pass
        
        return Measure(
            durables=durables
        )

    def load_note(self, note_element: ET.Element) -> Durable:
        type_element = note_element.find("type")

        durable_kwargs = {
            "type_duration": type_element.text,
            "fractional_duration": Fraction(1, 999), # TODO: decode
            "duration_dots": 0, # TODO: decode
            "measure_onset": Fraction(1, 999) # TODO: decode
        }
        
        if note_element.find("rest") is not None:
            durable = Rest(**durable_kwargs)
        else:
            pitch_element = note_element.find("pitch")
            pitch = pitch_element.find("step").text + \
                pitch_element.find("octave").text
            durable = Note(
                pitch=pitch, # TODO: decode pitch alter
                **durable_kwargs
            )
        
        return durable
