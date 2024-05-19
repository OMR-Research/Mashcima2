from mashcima2.scene.visual.Stafflines \
    import Stafflines, StaffCoordinateSystem
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.scene.Sprite import Sprite
from mashcima2.geometry.Vector2 import Vector2
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.units import px_to_mm


MUSCIMA_LINE_WIDTH = px_to_mm(1.5, dpi=300)
MUSCIMA_STAFF_SPACE = px_to_mm(28.75, dpi=300)


class NaiveStaffCoordinateSystem(StaffCoordinateSystem):
    def __init__(self, staff_space: float):
        self.staff_space = staff_space
    
    def get_transform(
        self,
        pitch_position: float,
        time_position: float
    ) -> Transform:
        return Transform.translate(
            Vector2(
                x=time_position,
                y=self.staff_space * (-pitch_position / 2)
            )
        )


# TODO: define a StafflinesSynthesizer interface and inherit
class NaiveStafflinesSynthesizer:
    """Simple stafflines synthesizer that just creates straight stafflines"""
    def synthesize(
        self,
        parent_space: AffineSpace,
        position: Vector2,
        width: float,
        staff_space: float = MUSCIMA_STAFF_SPACE,
        line_width: float = MUSCIMA_LINE_WIDTH
    ) -> Stafflines:
        local_space = AffineSpace(
            parent_space=parent_space,
            transform=Transform.translate(position)
        )
        sprites = [
            Sprite.rectangle(
                local_space,
                Rectangle(
                    x=0,
                    y=i * staff_space - line_width / 2,
                    width=width,
                    height=line_width
                ),
                fill_color=(0, 0, 0, 255),
                dpi=300
            )
            for i in range(-2, 3)
        ]
        return Stafflines(
            space=local_space,
            sprites=sprites,
            staff_coordinate_system=NaiveStaffCoordinateSystem(
                staff_space=staff_space
            )
        )
