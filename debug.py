"""
Some debug functions.
"""
import pickle
import AIQlearningCtsStateSpace

def resetQLearningMem():
	"""Resets the q-learning table
	"""
	blankTable = {}
	with open(AIQlearningCtsStateSpace.MEMORY_FILE, 'wb') as f:
		pickle.dump(blankTable, f)
