from mashcima2.scene.visual.Stafflines import Stafflines
from mashcima2.scene.semantic.Staff import Staff
from mashcima2.scene.semantic.Note import Note
from mashcima2.scene.semantic.Rest import Rest
from mashcima2.scene.AffineSpace import AffineSpace
from mashcima2.scene.Sprite import Sprite
from mashcima2.scene.visual.HalfNote import HalfNote
from mashcima2.geometry.Transform import Transform
from mashcima2.geometry.Rectangle import Rectangle
from mashcima2.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer


# TODO: define a layout synthesizer interface and inherit
# IN -> semantic scene object graph
# OUT -> visual scene object graph
class ColumnLayoutSynthesizer:
    """
    TODO: revise this text, no more tetris:
    Lays out glyphs onto a blank score using the tetris alorithm,
    combined with the W3C flexbox flex-grow behavior.

    The tetris algorithm:
    Everyhing happens in the staff coordinate space (vertically the units are
    staff spaces, horizontally they are millimeters). Blocks of various shapes
    (mostly rectangles) fall from the right side to the left, until they hit
    the already landed blocks. This creates the tightest-possible packing
    of all space-taking musical symbols. Then, if a target width is to be
    covered, additional space is inserted in between the blocks, though,
    not uniformly, but according to the flex-grow values of blocks. The higher
    the value, the more space will be distributed to that block. There may be
    multiple stacks, and a block participates in a number of these stacks
    (you'd have one stack for each staff and then possibly one for lyrics)

    A column is a cluster of glyphs with fixed position relative to each other,
    that takes up the entire height of a staff (or many staves/stacks).
    """
    pass
