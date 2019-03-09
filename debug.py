"""
Some debug functions.
"""
import pickle
import AIQlearningCtsStateSpace
import QLearning

def resetQLearningMem():
	"""Resets the q-learning table
	"""
	blankTable = QLearning.initArray()
	with open(AIQlearningCtsStateSpace.MEMORY_FILE, 'wb') as f:
		pickle.dump(blankTable, f)
