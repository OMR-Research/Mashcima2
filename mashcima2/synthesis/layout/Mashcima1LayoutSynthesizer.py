from mashcima2.scene.visual.Stafflines import Stafflines
from mashcima2.scene.semantic.Staff import Staff
from mashcima2.scene.semantic.Note import Note
from mashcima2.scene.semantic.Rest import Rest
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.scene.Sprite import Sprite
from mashcima2.scene.visual.HalfNote import HalfNote
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.Rectangle import Rectangle


def dummy_half_note_synthesizer(
    parent_space: AffineSpace,
    transform: Transform
) -> HalfNote:
    local_space = AffineSpace(
        parent_space=parent_space,
        transform=transform
    )
    sprites = [
        Sprite.debug_box(local_space, Rectangle(-1, -1, 2, 2)), # notehead
        Sprite.debug_box(local_space, Rectangle(0, -10, 1, 10)) # stem
    ]
    half_note = HalfNote(
        space=local_space,
        sprites=sprites
    )
    return half_note


# TODO: define a layout synthesizer interface and inherit
# IN -> semantic scene object graph
# OUT -> visual scene object graph
class Mashcima1LayoutSynthesizer:
    def synthesize(self, stafflines: Stafflines, staff: Staff):
        time_position = 5
        TIME_STEP = 7

        for measure in staff.measures:
            for durable in measure.durables:
                if isinstance(durable, Note):
                    dummy_half_note_synthesizer(
                        stafflines.space,
                        stafflines.staff_coordinate_system.get_transform(
                            -4, # TODO: pitch to pitch_position
                            time_position
                        )
                    )
                    time_position += TIME_STEP
                elif isinstance(durable, Rest):
                    pass
            # TODO: barline
            time_position += TIME_STEP
