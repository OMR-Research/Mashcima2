import random


def random_between(
    from_value: float,
    to_value: float,
    rng: random.Random
) -> float:
    """Returns a random float between two values"""
    return from_value + rng.random() * (to_value - from_value)
