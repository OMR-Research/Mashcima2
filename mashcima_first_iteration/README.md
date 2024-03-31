This folder contains the first iteration of the idea. It was unnecessarily complex, difficult to understand, overly focused on extensibility and forgot to be simple. I'm scrapping this, but I want the code to remain here for a while, so that I can copy-paste the Scene-related code.

The idea for the second iteration is to make something aking to NLTK - lots of modular pieces of code, that fit together via a set of well-designed interfaces. That is a better design.

Now for the next iteration, I will simply coerse Mashcima 1 into this structured form. Let's see how that goes. Also Mashcima 2 should be a separate pypy package `mashcima2`, like OpenCV, or DeepScore, or UDPipe, or other systems that have evolved too dramatically to stay a single package. *-- Jiří Mayer, 2024-03-31*


# Mashcima 2

A library and a framework for synthesizing images containing music, intended for use as training data for OMR models.


## Basic overview and design motivations

Currently I'm just trying to get the overall architecture going, so that any synthesizer developed in this framework is easily extensible. This is an overview/tutorial of what I've come to so far:


### Considering all the requirements

> This is just a rant about how complex the problem is. Just skip to the next heading for the tutorial.

Basic unit of synthesis is a *model*, as in *generative model*. We have lots of requirements about this model:

- It should roughly be a function `f(z) --> (x, y)` (where `z` are parameters, rng seed, etc...)
- Models should be recursively composable and reusable (e.g. a digit image model should be used by a number image model)
- It may produce more data, than just `x` and `y`, so really it produces a dictionary of values, that can even be extended in the future
- a model is a blackbox, only modifiable by its parameters (so models should be written with extensibility in mind - this means proper abstraction layers and modularity)
- parameters of a model can be another model (so that we can swap out lower-level models if necessary, within high-level models) ... but this makes it painful to create the high-level models ... so we need something like an IoC container and dependency injection
- when wirting a model, it's unlikely we will cover all the possible annotation formats; e.g. say we write a one-staff music synthesizer and we produce PrIMuS agnostic and the image. Then someone comes along with MuNG and now what? The synthesis process definitely internally has all the information necessary to produce MuNG annotation, but we cannot get it from the direct model output. Therefore: we need to remember all the inner-model results as well and keep them in some hierarchical datastructure, so that people can utilize the data after the model is developed.

There are also requirements on the data passed between the models. We are not only producing simple data (strings, numbers), but we are producing spatial-data (images, bounding boxes, masks, vectors, points). Spatial data poses some challenges when combining lower-level model results into one larger composite result:

- spatial data is translation-symmetric
- when spatial data traverses the model hierarchy, it's coordinates need to change reference frames
- aggregating this data from lower-level models into composite results is complicated, depends on the data type (bounding boxes are different to images, which are different to segmentation masks)

> This messy text should be compiled to some ADRs...


### Introducing Mashcima 2

> If the tutorial does not make sense to you, it's ok. This is just a sketch for me so that **I** don't forget stuff.

There are two basic building blocks to the synthesizer:

- `Model` a process that acts on a space and synthesizes new objects within it
- `Space` s (hierarchical) space of objects and values, containing the synthesized data

Say we have a model that can synthesize MNIST digits. We first create and empty `Space` (a sandbox for the model to play in), and then we execute the model in its context:

```py
import mashcima as mc
from random import Random

@mc.model
def mnist_digit_model()
    # does some magic
    pass

with mc.Space() as space:
    random = Random()
    mnist_digit_model(random)

print(space["image"])
print(space["bounding_box"])
```

The model creates some objects within the space that we can then get and use.

When a model is executed, it has one space as its context only. It should produce all of its outputs into that space. The space represents that model's level of abstraction. You can have multiple models run after one another within one space if they somehow build on top of each other. If the model uses lower-level models, they should be run in child-spaces, because they will produce outputs assuming they are top-level (but they aren't in such a case).

Let's start with basics and let's write a model that generates words (no spatial objects, just strings):

```py
import mashcima as mc
from random import Random

@tf.model
def vovel_model(random: Random):
    vovel = random.choice([
        "a", "e", "i", "o", "u", "y"
    ])

    # items returned here will become part of the context Space
    return {
        "vovel": vovel,
        "vovel_upper": vovel.upper()
    }

@tf.model
def word_model(random: Random):
    space = Space.current # get the current space context

    length = random.randint(3, 8)

    word = ""
    for i in range(length):
        # create a subspace for the vovel model
        with space.create_child("vovel_" + str(i)) as subspace:
            vovel = vovel_model(random)["vovel"]
            # the dictionary is added to subspace but also just returned
            word += vovel

    return {
        "word": word
    }
```

When we want to use the `word_model` we can let it create the `word` object in the root space, but should we ever need the data from the internal `vovel_model`s, we can enumerate over the child spaces and extract any additional data.

Try going through [`mashcima.prototyping.__main__`](mashcima/prototyping/__main__.py), it contains more examples.


### To be figured out

- Training epochs, dataset shuffling, its API, RNG passing
- Dataset downloading & preparation
- Filters (it's going to be a post-processing model, sth. like a compositor)
- Space querying (e.g. give me bounding boxes of all quarter notes)
