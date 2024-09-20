import xml.etree.ElementTree as ET
from ..scene.semantic.Score import Score
from ..scene.semantic.Part import Part
from ..scene.semantic.Measure import Measure
from ..scene.semantic.Staff import Staff
from ..scene.semantic.Durable import Durable
from ..scene.semantic.Note import Note
from ..scene.semantic.Rest import Rest
from ..scene.semantic.TypeDuration import TypeDuration
from ..scene.semantic.Pitch import Pitch
from typing import List, TextIO, Optional
from fractions import Fraction
from dataclasses import dataclass, field
import io


@dataclass
class _PartState:
    part_id: str
    "MusicXML ID of the currently parsed part, used for error localization"

    measure_number: Optional[str] = field(default=None)
    "Currently parsed measure number, or None if it was not yet defined/parsed"


IGNORED_MEASURE_ELEMENTS = set([
    # https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure-partwise/
    "direction", "harmony", "figured-bass", "print", "sound", "listening",
    "grouping", "link", "bookmark", "barline"
])


class MusicXmlLoader:
    """Loads MusicXML into the scene data model"""

    def __init__(self, errout: Optional[TextIO] = None):
        self._errout = errout or io.StringIO()
        "Print errors and warnings here"
        
        self._part_state: Optional[_PartState] = None
        "Part state, not None when parsing a part"

    def _error(self, *values):
        if self._part_state:
            p = self._part_state.part_id
            m = self._part_state.measure_number
            header = f"[ERROR][P:{p} M:{m}]:"
        else:
            header = f"[ERROR]:"
        print(header, *values, file=self._errout)

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
            part = self._load_part(score_part_element, part_element, part_id)
            parts.append(part)

        return Score(parts=parts)
    
    def _load_part(
        self,
        score_part_element: ET.Element,
        part_element: ET.Element,
        part_id: str
    ) -> Part:
        assert score_part_element.tag == "score-part" # part header
        assert part_element.tag == "part" # part measures
        assert score_part_element.attrib["id"] == part_id
        assert part_element.attrib["id"] == part_id

        # TODO: should split to staves according to linebreaks

        self._part_state = _PartState(part_id=part_id)

        measures: List[Measure] = []

        for measure_element in part_element:
            measure = self._load_measure(measure_element)
            measures.append(measure)
        
        self._part_state = None
        
        return Part(measures=measures)
    
    def _load_measure(self, measure_element: ET.Element) -> Measure:
        assert measure_element.tag == "measure"

        self._part_state.measure_number = measure_element.attrib.get("number")

        durables: List[Durable] = []

        for element in measure_element:
            if element.tag in IGNORED_MEASURE_ELEMENTS:
                continue
            elif element.tag == "note":
                durable = self._load_note(element)
                durables.append(durable)
            elif element.tag == "attributes":
                pass # TODO: process attributes
            elif element.tag == "backup":
                pass # TODO: process backup element
            elif element.tag == "forward":
                pass # TODO: process forward element
            else:
                self._error(
                    "Unexpected <measure> element:",
                    element,
                    element.attrib
                )
        
        return Measure(
            durables=durables
        )

    def _load_note(self, note_element: ET.Element) -> Durable:
        assert note_element.tag == "note"

        # <rest> or <pitch>
        rest_element = note_element.find("rest")
        is_measure_rest = False
        pitch: Optional[Pitch] = None
        if rest_element is not None:
            is_measure_rest = rest_element.attrib.get("measure") == "yes"
        else:
            pitch_element = note_element.find("pitch")
            step = pitch_element.find("step").text
            octave = pitch_element.find("octave").text
            alter = None
            alter_element = pitch_element.find("alter")
            if alter_element is not None:
                alter = alter_element.text
            pitch = Pitch.parse(octave, step, alter)

        # <type>, missing only for rest measures
        type_element = note_element.find("type")
        type_duration: Optional[TypeDuration] = None
        if type_element is not None:
            type_duration = TypeDuration(type_element.text)
        elif is_measure_rest:
            pass # leave type duration at None
        else:
            self._error("Note does not have <type>:", ET.tostring(note_element))

        # --- --- --- ---

        # TODO: handle measure rests (missing type_duration)

        durable_kwargs = {
            "type_duration": type_duration,
            "fractional_duration": Fraction(1, 999), # TODO: decode
            "duration_dots": 0, # TODO: decode
            "measure_onset": Fraction(1, 999) # TODO: decode
        }
        
        if note_element.find("rest") is not None:
            durable = Rest(**durable_kwargs)
        else:
            durable = Note(
                pitch=pitch,
                **durable_kwargs
            )
        
        return durable
