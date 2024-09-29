class Callback:
    """Base class for custom generative model callbacks"""

    def on_sample_begin(self):
        """Called at the start of generation of a data sample"""
        pass

    def on_sample_end(self):
        """Called at the end of generation of a data sample"""
        pass

    # TODO: on_epoch_being(epoch_index) could be maybe added in the future
