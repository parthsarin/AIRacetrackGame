"""
Methods for an AI that Q-learns how to drive a car.
"""
from pathlib import Path # for remembering the table
import numpy as np # for math
import collections # for storing (state, action) pairs
import pickle # for storing the table
import random
import errors

import IO

MEMORY_FILE = 'memory/qlearning.mem'
REWARD_RANGE = 100
DEFAULT_LEARNING_RATE = .465
QLearningData = collections.namedtuple('QLearningData', ['state', 'action'])

def process(state, NUM_TO_DIR, LEARNING_RATE = DEFAULT_LEARNING_RATE):
	"""Decides which direction to move based on the current state.

	:state: An instance of IO.State which describes the current state
	of the game.
	:NUM_TO_DIR: A dictionary that translates single-digit directions
	into a dictionary of booleans containing directional information.
	:LEARNING_RATE: A number between 0 and 1 that represents how fast
	the algorithm should learn.
	"""
	approximations = {}
	for direction in NUM_TO_DIR:
		# Approximate the value of each action
		approximations[direction] = approximateValue(state, IO.Movement(**NUM_TO_DIR[direction]), LEARNING_RATE)

	print("Approximated ", approximations)

	# Sort and pick the action which gives the highest approximated value
	optimalDirection = sorted(approximations.items(), key=lambda x: x[1])[::-1][0]
	if approximations[optimalDirection[0]]== approximations[0]:
		return IO.Movement(front=True)
	return IO.Movement(**NUM_TO_DIR[optimalDirection[0]])

def approximateValue(state, action, LEARNING_RATE):
	"""Approximates the expected reward for taking a given
	action from a given state.

	:state: An instance of IO.State which describes the current state
	of the game.
	:action: An instance of IO.Movement which describes the action
	the program is considering
	:LEARNING_RATE: A number between 0 and 1 that represents how fast
	the algorithm should learn.
	"""
	# Create a falloff function to weight the points we have info for
	kDecay = 1 # width of one standard deviation
	falloff_func = lambda x: np.exp(- np.pi * (x/kDecay) ** 2) # exponential decay

	# Create the values that will be modified in the loop
	pred_value_num = 0
	pred_value_denom = 0

	# Create a numpy vector representing the current state (shape: (11,))
	state_vector = buildMLVector(state.distances, state.velocity, state.velocity_magnitude)

	# Load the table
	table = loadQTable()

	# Create random noise
	random_val = (random.random()*200 - 100) * (1 - LEARNING_RATE) / (len(table)+1)

	if table:
		# loop over data points
		for func_value in table:
			# only compare the same action
			if func_value.action == action:
				# Build a comparable ML vector
				func_value_state_vector = buildMLVector(func_value.state.distances, func_value.state.velocity, func_value.state.velocity_magnitude)
				
				# Distance between the two points
				distance = np.linalg.norm(state_vector-func_value_state_vector)
				pred_value_num += falloff_func(distance) * table[func_value]
				pred_value_denom += falloff_func(distance)

		if pred_value_denom != 0:
			return pred_value_num / pred_value_denom + random_val
		else:
			return random_val
	else:
		return random_val

def buildMLVector(distances, velocity, magnitude):
	"""Rescale distances & velocity and combine them into a single vector.

	:distances: A numpy array of distances in eight directions
	:velocity: A numpy array representing velocity
	:magnitude: The magnitude of the velocity vector
	:returns: A numpy array representing the distance, velocity, and velocity magnitude
	"""
	if np.linalg.norm(distances) != 0:
		distances = distances / np.linalg.norm(distances)
	
	if magnitude != 0:
		velocity = velocity / magnitude

	return np.array(list(distances) + list(velocity) + [magnitude])

def train(state, action, reward):
	"""Train the AI by adding the reward for a particular (state, action) pair
	to the table.

	:state: The state from which the action was taken.
	:action: The action that was taken.
	:reward: The reward that was recieved.
	"""
	table = loadQTable()
	table[QLearningData(state, action)] = reward
	writeQTable(table)

def loadQTable():
	"""Load the Q-table from the memory file by depickling it.
	"""
	tablePath = Path(MEMORY_FILE)
	if tablePath.exists():
		with tablePath.open('rb') as f:
			return pickle.load(f)
	else:
		raise errors.NoMemTable("Please create a q-learning table at memory/qlearning.")

def writeQTable(table):
	"""Write the table to the MEMORY_FILE using pickle.
	Note: This function *rewrites* the table!

	:table: The table to be written to the memory file.
	"""
	tablePath = Path(MEMORY_FILE)
	if tablePath.exists():
		with tablePath.open('wb') as f:
			pickle.dump(table, f)
	else:
		raise errors.NoMemTable("Please create a q-learning table at memory/qlearning.") 