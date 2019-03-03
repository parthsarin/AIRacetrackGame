from pathlib import Path # for remembering the table
import numpy as np # for math
import pickle # for storing the table
import errors

import IO

def process(state, NUM_TO_DIR):
	approximations = {}
	for direction in NUM_TO_DIR:
		approximations[direction] = approximateValue(state, IO.Movement(**NUM_TO_DIR[direction]))

	print("Approximated ", approximations)
	optimalDirection = sorted(approximations.items(), key=lambda x: x[1])[::-1][0]
	if approximations[optimalDirection[0]]== approximations[0]:
		return IO.Movement(front=True)
	return IO.Movement(**NUM_TO_DIR[optimalDirection[0]])

def approximateValue(state, action):
	kDecay = 10
	falloff_func = lambda x: np.exp(- np.pi * (x/kDecay) ** 2) # exponential decay

	pred_value = 0

	state_vector = np.array(list(state.distances) + list(state.velocity))
	table = loadQTable()
	if table:
		for func_value in table:
			func_value_state_vector = np.array(list(func_value[0].distances) + list(func_value[0].velocity))
			distance = np.linalg.norm(state_vector-func_value_state_vector)
			pred_value += falloff_func(distance) * table[func_value]

		return pred_value
	else:
		return 0

def teach(state, action, reward):
	table = loadQTable()
	table[(state, action)] = reward
	writeQTable(table)

def loadQTable():
	tablePath = Path('memory/qlearning.mem')
	if tablePath.exists():
		with tablePath.open('rb') as f:
			return pickle.load(f)
	else:
		raise errors.NoMemTable("Please create a q-learning table at memory/qlearning.")

def writeQTable(table):
	tablePath = Path('memory/qlearning.mem')
	if tablePath.exists():
		with tablePath.open('wb') as f:
			pickle.dump(table, f)
	else:
		raise errors.NoMemTable("Please create a q-learning table at memory/qlearning.") 