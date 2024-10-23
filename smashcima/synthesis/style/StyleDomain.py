import abc


class StyleDomain(abc.ABC):
    """Style domain represents one aspect along side of which the style
    of a synthesized data sample can be affected. For example, the choice
    of a background patch to use for background synthesis would be a style
    dimension that can be captured by a style domain. Where the domain are all
    the possible background patches to choose from. Similarly, the specific
    writer of a handwritten glyph dataset in the context of all of its writers
    would represent a style domain."""
    
    def pick_style(self):
        """This method is called by the Styler before a new sample is
        synthesized. This method should pick a concrete value out of the
        described domain of values."""
        raise NotImplementedError
