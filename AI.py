"""
Interfaces with the AI algorithm.
"""
import IO

### AIs ###
import AI_longest_distance as ld
import AI_antonio as best
import AI_QLearning as ql
import QLearning

### CURRENT AI PARAMS ###
# # Q-learning
# CURRENT_DECISION_FN = ql.process
# CURRENT_TRAIN_FN = ql.train
# CURRENT_DATA = ql.loadQTable()
# CURRENT_SAVE_FN = ql.writeQTable
# DEFAULT_SAVE_PATH = ql.MEMORY_FILE

# Longest distance
# CURRENT_DECISION_FN = ld.process
# CURRENT_TRAIN_FN = lambda a, b, c, d: None
# CURRENT_DATA = None
# CURRENT_SAVE_FN = lambda a, b: None
# DEFAULT_SAVE_PATH = None

# Antonio
CURRENT_DECISION_FN = best.process
CURRENT_TRAIN_FN = lambda x, y, z, a: x
CURRENT_DATA = None
CURRENT_SAVE_FN = lambda x, y: x
DEFAULT_SAVE_PATH = None

class Driver:
    def __init__(self):
        """Instantiates the driver by copying the module globals onto
        the object.
        """
        self.decision_fn = CURRENT_DECISION_FN
        self.train_fn = CURRENT_TRAIN_FN
        self.ai_data = CURRENT_DATA
        self.save_fn = CURRENT_SAVE_FN

    def runAI(self, state):
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

        return self.decision_fn(state, self.ai_data, NUM_TO_DIR)

    def trainAI(self, state, action, reward):
        """Trains the AI that the action it performed gave it a
        particular reward.

        :state: The state from which the AI performed the action.
        :type state: IO.State
        :action: The action the AI performed.
        :type action: IO.Movement
        :reward: The reward the AI recieved.
        :type reward: float
        """
        self.ai_data = self.train_fn(state, action, reward, self.ai_data)

    def saveAIData(self, path=DEFAULT_SAVE_PATH):
        """Saves the AI data to the disk.
        """
        self.save_fn(self.ai_data, path)
