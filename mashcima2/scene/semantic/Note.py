from dataclasses import dataclass
from typing import Optional
from fractions import Fraction
from ..SceneObject import SceneObject


@dataclass
class Note(SceneObject):
    duration: Fraction
