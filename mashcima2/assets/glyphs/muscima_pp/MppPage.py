from pathlib import Path
from muscima.io import parse_cropobject_list, CropObject
from typing import List, Dict
import re


class MppPage:
    def __init__(
        self,
        crop_objects: List[CropObject],
        mpp_writer: int,
        mpp_document: int
    ):
        self.crop_objects = crop_objects
        "List of cropobjects as they are loaded by the muscima library"

        self.id_lookup: Dict[int, CropObject] = {
            c.objid: c
            for c in self.crop_objects
        }
        "Dictionary for fast id lookup"

        self.mpp_writer = mpp_writer
        "Writer index (1 to 50) from the MUSCIMA++ dataset"

        self.mpp_document = mpp_document
        "Document index (1 to 20) from the MUSCIMA++ dataset"

    @staticmethod
    def load(path: Path) -> "MppPage":
        crop_objects: List[CropObject] = parse_cropobject_list(path)

        m = re.match(r"CVC-MUSCIMA_W-(\d+)_N-(\d+)_D-ideal", path.stem)
        mpp_writer = int(m.group(1))
        mpp_document = int(m.group(2))

        return MppPage(crop_objects, mpp_writer, mpp_document)
    
    def get(self, objid: int) -> CropObject:
        """Looks up a crop object by its integer ID"""
        return self.id_lookup[objid]
    
    def get_outlink_to(self, obj: CropObject, clsname: str) -> CropObject:
        """
        Returns the crop object at the end of any outlink
        with the given classname
        """
        for l in obj.outlinks:
            resolved_link = self.get(l)
            if resolved_link.clsname == clsname:
                return resolved_link
        raise Exception("Object has no outlink of requested clsname")

    def has_outlink_to(self, obj: CropObject, clsname: str) -> bool:
        """
        Tests that there is a crop object at the end of any outlink
        with the given classname
        """
        for l in obj.outlinks:
            resolved_link = self.get(l)
            if resolved_link.clsname == clsname:
                return True
        return False
