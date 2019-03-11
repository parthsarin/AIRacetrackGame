"""
Whoo! Gotta love testing.

Here's the dealio (a.k.a. how to set up a test): 
1. Wrap it with the decorator
	@run_test("NAME OF TEST HERE")
	def test1():
		# ...

	If you want to silence the output of your function, you can do so with
	@run_test("NAME OF TEST HERE", silence=True)
	def test2():
		# ...

	You can also, optionally, assign categories to each of your tests with
	@run_test("NAME OF TEST HERE", category="AI")

2. Have it return a boolean as to whether it passed the test. 
If there are a bunch of tests, you can do this with a truthtable.
That's something like:
	outcome1 = (result1 == expected1)
	outcome2 = (result2 == expected2)
	allTests = [ outcome1, outcome2 ]
	return all( allTests ) # returns True if all tests are passed

3. Run `python3 testing.py`, sit back, and relax!
"""
import AI
import AI_QLearning
import IO
import debug
from testing_harness import * # I know, I know... Here be dragons, but like, they're nice dragons, I promise!

"""
AI Tests
"""
def MIBPenFlashyFlash(player):
	"""Clears the Q-learning memory
	"""
	debug.resetQLearningMem(player)

@run_test("The AI learns to move forward if it gets rewards for doing so.", category="AI", silence=True)
def AITest1():
	startingState = IO.State([100, 80, 60, 80, 100, 80, 60, 80], [0,0])
	front = IO.Movement(front=True)
	unsuspecting_driver = AI.Driver()

	for i in range(10):
		unsuspecting_driver.trainAI(startingState, front, 100) # moving forward is, like, really cool!

	outcome = (unsuspecting_driver.runAI(startingState) == front)
	MIBPenFlashyFlash(unsuspecting_driver) # be sure to do this so that the AI doesn't end up confused with previous data
	return outcome

@run_test("The AI learns to move forward if it's next to a point that it knows to move forward from.", category="AI", silence=True)
def AITest2():
	startingState = IO.State([100, 80, 60, 80, 100, 80, 60, 80], [0,0])
	front = IO.Movement(front=True)
	driver = AI.Driver()

	for i in range(10):
		driver.trainAI(startingState, front, 100) # moving forward is, like, really cool!

	shiftedStartingState = IO.State([100, 85, 75, 85, 100, 75, 55, 75], [0,0]) # shifted to the left
	outcome = (driver.runAI(shiftedStartingState) == front)
	MIBPenFlashyFlash(driver)
	return outcome

@run_test("The AI properly stores its Q-table.", category="AI", silence=False)
def AITest3():
	startingState = IO.State([100, 80, 60, 80, 100, 80, 60, 80], [0,0])
	front = IO.Movement(front=True)
	driver = AI.Driver()

	for i in range(10):
		driver.trainAI(startingState, front, 100) # moving forward is, like, really cool!

	ai_data = driver.ai_data

	driver.saveAIData() # write the data to the disk
	loaded_data = AI_QLearning.loadQTable()

	outcome = (ai_data == loaded_data) # the correct info is being written
	MIBPenFlashyFlash(driver)
	return outcome

"""
Graphics Tests (...do these exist...?)
"""

if __name__ == '__main__':
	run_all_tests()