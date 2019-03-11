"""
Some debug functions.
"""
import pickle
import AI_QLearning
import QLearning

def resetQLearningMem(player):
	"""Resets the q-learning table
	"""
	blankTable = QLearning.initArray()
	with open(AI_QLearning.MEMORY_FILE, 'wb') as f:
		pickle.dump(blankTable, f)
