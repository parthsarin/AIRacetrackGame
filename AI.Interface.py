"""
Interfaces with the AI algorithm.
"""
import IO

### AIs ###
import AI.LongestDistance as ld

CURRENT_DECISION_FN = ld.process

def runAI(distances):
    """Interfaces with the selected AI algorithm by sending it
    the input as a vector of eight numbers (distances in the
    eight directions) and returns an instance of the Movement
    class describing what the AI would do.

    :distances: A vector of eight numbers representing the distances
    to the wall in eight directions.

    CONVENTION:
        7    0    1
         \   |   /

         6 – X – 2

          /  |   \
         5   4    3

    :return: An instance of the IO.Movement class that describes where
    the car should move.
    """
    return CURRENT_DECISION_FN(distances)
