"""
Interfaces with the AI algorithm.
"""
import IO

### AIs ###
import AI_longest_distance as ld
import AI_QLearning as ql

CURRENT_DECISION_FN = ql.process
CURRENT_TRAIN_FN = ql.train

def runAI(state):
    """Interfaces with the selected AI algorithm by sending it
    the input as a vector of eight numbers (distances in the
    eight directions) and returns an instance of the Movement
    class describing what the AI would do.

    :return: An instance of the IO.Movement class that describes where
    the car should move.
    """
    NUM_TO_DIR = {
        0: { 'front': True },
        1: { 'front': True, 'right': True },
        2: { 'right': True },
        3: { 'right': True,'back': True },
        4: { 'back': True },
        5: { 'back': True,'left': True },
        6: { 'left': True },
        7: { 'left': True, 'front': True },
        8: {}
    }

    return CURRENT_DECISION_FN(state, NUM_TO_DIR)

def trainAI(state, action, reward):
    """Trains the AI that the action it performed gave it a
    particular reward.

    :state: The state from which the AI performed the action.
    :type state: IO.State
    :action: The action the AI performed.
    :type action: IO.Movement
    :reward: The reward the AI recieved.
    :type reward: float
    """
    CURRENT_TRAIN_FN(state, action, reward)