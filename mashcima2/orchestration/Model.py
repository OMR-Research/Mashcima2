import abc
from ..scene.Scene import Scene
from typing import Optional


class Model(abc.ABC):
    """
    Model is the container for a specific synthesis pipeline. It:
    - Acts as the public facing API for the data consumer.
    - Constructs and wires together pipeline components (synthesizers,
        loaders, renderers). Acts as an IoC container.
    - Tracks steps, batches, and epochs during the synthesis process.
    """
    
    def __init__(self):
        self.scene: Optional[Scene] = None
        "The scene synthesized during the last invocation of this model"

    def __call__(self, *args, **kwargs):
        # create a fresh new scene that will contain the synthesized sample
        self.scene = Scene()

        # run the synthesis pipeline
        outputs = self.call(*args, **kwargs)

        # return whatever the model's call method returned
        return outputs

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        raise NotImplementedError(
            f"Model {self.__class__.__name__} does not have a `call()` "
            "method implemented."
        )
