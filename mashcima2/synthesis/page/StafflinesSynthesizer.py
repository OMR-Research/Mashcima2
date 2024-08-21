from ...geometry.Vector2 import Vector2
from ...scene.AffineSpace import AffineSpace
from ...scene.visual.Stafflines import Stafflines
import abc


class StafflinesSynthesizer(abc.ABC):
    """
    Interface for a stafflines synthesizer
    """

    @abc.abstractmethod
    def synthesize(
        self,
        parent_space: AffineSpace,
        position: Vector2,
        width: float,
    ) -> Stafflines:
        """
        Synthesizes a new Stafflines visual object.

        :param AffineSpace parent_space: Stafflines will be placed into this space.
        :param Vector2 position: Position of the left endpoint of the middle staffline.
        :param float width: Width of the staff in millimeters.
        """
        raise NotImplementedError
