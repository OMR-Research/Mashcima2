import xml.etree.ElementTree as ET
from ..scene.semantic.Score import Score
from ..scene.semantic.Part import Part
from ..scene.semantic.Measure import Measure
from ..scene.semantic.Staff import Staff
from ..scene.semantic.Durable import Durable
from ..scene.semantic.Note import Note
from ..scene.semantic.Rest import Rest
from typing import List
from fractions import Fraction


class MusicXmlLoader:
    """Loads MusicXML into the scene data model"""

    def load_file(self, path: str) -> Score:
        """Loads a score from a MusicXML file"""
        # TODO: handle .mxl files as well
        # TODO: accept Path instance as well
        with open(path, "r") as file:
            tree = ET.parse(file)
        return self.load(tree)

    def load(self, tree: ET.ElementTree) -> Score:
        """Loads a score from a MusicXML XML tree"""
        score_partwise_element = tree.getroot()
        if score_partwise_element.tag != "score-partwise":
            raise Exception("The loader expects the <score-partwose> " + \
                            "tag to be the root of the file.")
        
        score = self._load_score_partwise(score_partwise_element)
        score.validate()
        return score
    
    def _load_score_partwise(self, score_partwise_element: ET.Element) -> Score:
        assert score_partwise_element.tag == "score-partwise"

        parts: List[Part] = []

        # go through all the parts
        part_list_element = score_partwise_element.find("part-list")
        for score_part_element in part_list_element:
            part_id = score_part_element.attrib.get("id")
            if part_id is None:
                raise Exception("<score-part> element is missing an ID.")

            # find the part element
            part_elements = [
                p for p in score_partwise_element.findall("part")
                if p.attrib.get("id") == part_id
            ]
            if len(part_elements) == 0:
                raise Exception(f"Cannot find <part> with ID '{part_id}'.")
            part_element = part_elements[0]

            # and parse it
            part = self._load_part(score_part_element, part_element)
            parts.append(part)

        return Score(parts=parts)
    
    def _load_part(
        self,
        score_part_element: ET.Element,
        part_element: ET.Element
    ) -> Part:
        assert score_part_element.tag == "score-part" # part header
        assert part_element.tag == "part" # part measures

        # TODO: should split to staves according to linebreaks

        measures: List[Measure] = []

        for measure_element in part_element:
            measure = self._load_measure(measure_element)
            measures.append(measure)
        
        return Part(measures=measures)
    
    def _load_measure(self, measure_element: ET.Element) -> Measure:
        assert measure_element.tag == "measure"

        durables: List[Durable] = []

        for element in measure_element:
            if element.tag == "note":
                durable = self._load_note(element)
                durables.append(durable)
            elif element.tag == "attributes":
                pass
        
        return Measure(
            durables=durables
        )

    def _load_note(self, note_element: ET.Element) -> Durable:
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
