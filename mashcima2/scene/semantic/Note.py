from dataclasses import dataclass
from typing import Optional
from fractions import Fraction
from ..SceneObject import SceneObject
from .Durable import Durable


@dataclass
class Note(Durable):
    pitch: str # TODO: better than string
