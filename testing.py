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
import IO
import debug
from testing_harness import * # I know, I know... Here be dragons, but like, they're nice dragons, I promise!

"""
AI Tests
"""
def MIBPenFlashyFlash():
	"""Clears the Q-learning memory
	"""
	debug.resetQLearningMem()

@run_test("The AI learns to move forward if it gets rewards for doing so.", category="AI", silence=True)
def AITest1():
	startingState = IO.State([10, 8, 6, 8, 10, 8, 6, 8], [0,0])
	front = IO.Movement(front=True)

	for i in range(100):
		# AI.runAI(startingState)
		AI.trainAI(startingState, front, 100) # moving forward is, like, really cool!

	outcome = (AI.runAI(startingState) == front)
	MIBPenFlashyFlash() # be sure to do this so that the AI doesn't end up confused with previous data
	return outcome

@run_test("The AI learns to move forward if it's next to a point that it knows to move forward from.", category="AI", silence=True)
def AITest2():
	startingState = IO.State([10, 8, 6, 8, 10, 8, 6, 8], [0,0])
	front = IO.Movement(front=True)

	for i in range(10):
		AI.trainAI(startingState, front, 100) # moving forward is, like, really cool!

	shiftedStartingState = IO.State([10, 9, 7, 9, 10, 7, 5, 7], [0,0]) # shifted to the left
	outcome = (AI.runAI(shiftedStartingState) == front)
	MIBPenFlashyFlash()
	return outcome

"""
Graphics Tests (...do these exist...?)
"""

if __name__ == '__main__':
	run_all_tests()