"""
Methods for an AI that Q-learns how to drive a car.
"""
from pathlib import Path # for remembering the table
import numpy as np # for math
import collections # for storing (state, action) pairs
import pickle # for storing the table
import random
import errors
import QLearning
import itertools

import IO

MEMORY_FILE = 'memory/qlearning.mem'
REWARD_RANGE = 100
DEFAULT_LEARNING_RATE = .465
QLearningData = collections.namedtuple('QLearningData', ['state', 'action'])

def process(state, NUM_TO_DIR):
	"""Decides which direction to move based on the current state.

	:state: An instance of IO.State which describes the current state
	of the game.
	:NUM_TO_DIR: A dictionary that translates single-digit directions
	into a dictionary of booleans containing directional information.
	:LEARNING_RATE: A number between 0 and 1 that represents how fast
	the algorithm should learn.
	"""
	approximations = {}
	qtable = loadQTable()
	qstate = QLearning.QLState(state)

	for direction in NUM_TO_DIR:
		# Approximate the value of each action
		key = (tuple(qstate.distances), tuple(qstate.velocity), direction)
		approximations[direction] = qtable[key]

	print("Approximated ", approximations)

	# Sort and pick the action which gives the highest approximated value
	optimalDirection = sorted(approximations.items(), key=lambda x: x[1])[::-1][0]
	if approximations[optimalDirection[0]]== approximations[0]:
		return IO.Movement(front=True)
	return IO.Movement(**NUM_TO_DIR[optimalDirection[0]])

def train(state, action, reward, LEARNING_RATE = DEFAULT_LEARNING_RATE):
	"""Train the AI by adding the reward for a particular (state, action) pair
	to the table.

	:state: The state from which the action was taken.
	:action: The action that was taken.
	:reward: The reward that was recieved.
	"""
	qlstate = QLearning.QLState(state)
	known = QLearning.QLStateAction(qlstate, action)
	key = (tuple(known.state.distances), tuple(known.state.velocity), known.action.asNum())

	qtable = loadQTable()

	qtable['num_runs'] += 1
	qtable[key] = newValue(known, reward, known, qtable, LEARNING_RATE, qtable['num_runs'])

	writeQTable(qtable)

def newValue(known, known_reward, suppositional, qtable, LEARNING_RATE, num_runs):
	# Create a falloff function to weight the points we have info for
	kDecay = 1 # width of one standard deviation
	falloff_func = lambda x: np.exp(- np.pi * (x/kDecay) ** 2) # exponential decay

	old_reward = qtable[suppositional]

	old_state = suppositional.state.asNPArray()
	new_state = known.state.asNPArray()
	distance = np.linalg.norm(old_state-new_state)

	new_reward = (1-LEARNING_RATE) * old_reward + falloff_func(distance) * LEARNING_RATE * known_reward
	# new_reward = (old_reward + falloff_func(distance) * (1-LEARNING_RATE) * known_reward /num_runs) / (1 + falloff_func(distance) * (1-LEARNING_RATE) / num_runs)

	return new_reward

def loadQTable():
	"""Load the Q-table from the memory file by depickling it.
	"""
	tablePath = Path(MEMORY_FILE)
	if tablePath.exists():
		with tablePath.open('rb') as f:
			return pickle.load(f)
	else:
		raise errors.NoMemTable("Please create a q-learning table at {}.".format(MEMORY_FILE))

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
		raise errors.NoMemTable("Please create a q-learning table at {}.".format(MEMORY_FILE))