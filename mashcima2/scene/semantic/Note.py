from dataclasses import dataclass
from typing import Optional
from fractions import Fraction
from ..SceneObject import SceneObject
from .Durable import Durable
from .Pitch import Pitch


@dataclass
class Note(Durable):
    pitch: Pitch
    "Musical pitch of the note"
