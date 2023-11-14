import numpy as np
from mashcima.Space import Space
from mashcima.ScenePoint import ScenePoint
from mashcima.SceneImage import SceneImage
from mashcima.Model import Model
from random import Random
import mashcima as mc
from mashcima.Rectangle import Rectangle


class WordModel(Model):
    def validate_input(self, *args, **kwargs):
        pass
    
    def validate_output(self, *args, **kwargs):
        assert "word" in kwargs
        assert type(kwargs["word"]) is str
        assert len(kwargs["word"]) > 0


class LetterImageModel(Model):
    def validate_input(self, *args, **kwargs):
        # "random" argument
        assert type(args[0]) is Random
        
        # "letter" argument
        assert type(args[1]) is str
        assert len(args[1]) == 1
    
    def validate_output(self, *args, **kwargs):
        assert "image" in kwargs
        assert type(kwargs["image"]) is SceneImage


def bounding_box_compositor(bounding_boxes):
    space = Space.current
    if space is None:
        raise Exception("Compositor can only be called in the context of a space")

    bboxes = [bbox.elevate_into(space) for bbox in bounding_boxes]
    x = min([bbox.left for bbox in bboxes])
    y = min([bbox.top for bbox in bboxes])
    w = max([bbox.right for bbox in bboxes]) - x
    h = max([bbox.bottom for bbox in bboxes]) - y
    return Rectangle(x, y, w, h)


def image_compositor(images):
    space = Space.current
    if space is None:
        raise Exception("Compositor can only be called in the context of a space")

    return "TODO"


@mc.model(contract=WordModel)
def word_model(random: Random):
    word = random.choice([
        "lorem", "ipsum", "dolor"
    ])

    return {
        "word": word
    }


@mc.model(contract=LetterImageModel)
def letter_image_model(random: Random, letter: str):
    # TODO: load the mnist digits, etc...
    return {
        "letter": letter,
        "image": SceneImage(0, 0, 10, 30,
            np.zeros(shape=(2, 10), dtype=np.uint8)),
        "bounding_box": Rectangle(0, 1, 2, 3)
    }


@mc.model
def word_image_model(random: Random):
    space = Space.current

    # register default dependency implementations
    space.try_register(WordModel, lambda: word_model)
    space.try_register(LetterImageModel, lambda: letter_image_model)

    # resolve model dependencies
    _word_model = space.resolve(WordModel)
    _letter_image_model = space.resolve(LetterImageModel)

    # get the word string
    word = _word_model(random)["word"]

    bounding_boxes = []
    images = []

    # synthesize letter images in correct places
    position = 0
    for i, letter in enumerate(word):
        with space.create_child("letter_" + str(i)) as subspace:
            _letter_image_model(random, letter)
            bounding_box = subspace["bounding_box"]
            subspace.x = position - bounding_box.left
            position += bounding_box.width + 10
            bounding_boxes.append(bounding_box)
            images.append(subspace["image"])

    # get the composite bounding box
    # TODO: get bounding boxes via some scene query system
    # TODO: scene queries
    bounding_box = bounding_box_compositor(bounding_boxes)

    # get the composite image
    image = image_compositor(images)

    return {
        "bounding_box": bounding_box,
        "image": image
    }


with Space() as space:
    word_image_model(Random())
    space.debug_print()
