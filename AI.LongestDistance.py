"""
An AI algorithm that always moves towards the distance which is
farthest away. (i.e., very simple!)
"""
import IO

def process(distances, velocity, NUM_TO_DIR):
    """From a vector of eight distances, return the direction
    that the car should move in by calculating the distance that
    is farthest away.

    :distances: A vector of eight numbers representing the distances
    to the wall in eight directions.
    :return: An instance of the IO.Movement class that describes where
    the car should move.
    """
    # Note to self: why would we ever move backwards?
    IGNORE_INDICES = {3, 4, 5} # don't move backwards

    sorted_distances = sorted(enumerate(distances), key=lambda x: x[1])[::-1]

    for direction in sorted_distances:
        if direction[0] in IGNORE_INDICES:
            continue

        return IO.Movement(**NUM_TO_DIR[direction[0]])