"""
Provides an interface between the Graphics-level IO.State class
and the Q-learning AI. In particular, this file discretizes
the space of states so that the Q-learning AI can process them
more easily.
"""
import bisect # for identifying which bucket values fall into
import numpy as np # for everything math-y
import collections # for storing the q-table as a defaultdict

# In-house imports
import IO # for processing state and movement
import contextlib # for silencing racetrack... YES IT BOTHERS ME THAT MUCH, OKAY
with contextlib.redirect_stdout(None):
    import racetrack # sadly, this is just for a single value
    import Car # for the car's max velocity

class QLState:
	DIST_MAX_BUCKET_RATIO = 2/3
	DIST_NUM_SMALLER_BUCKETS = 10
	VEL_NUM_BUCKETS = 10
	MAX_SCREEN = max(racetrack.SCREEN_SIZE)

	def __init__(self, state):
		"""Initializes QLState from IO.State. QLState discretizes
		the state space so it can more easily be handled by the AI.

		:state: The current state of the game.
		:type state: IO.State
		"""
		if type(state) != IO.State:
			raise TypeError("QLState can only be initialized with a state of type IO.State.")

		"""Discretize the distance and velocity spaces into "buckets".
		This code might seem a little confusing, but let's go slowly and explain what each
		portion does...

			i * (QLState.DIST_MAX_BUCKET_RATIO * QLState.MAX_SCREEN /QLState.DIST_NUM_SMALLER_BUCKETS)
		
		This code divides the screen up into (almost) evenly spaced buckets, where the last 
		bucket is larger than the others. The last bucket has the value 
		(QLState.DIST_MAX_BUCKET_RATIO * QLState.MAX_SCREEN) and we divide the numbers
		from 0 to that value into QLState.DIST_NUM_SMALLER_BUCKETS buckets.

		The process for velocity is similar.
		"""
		self._dist_buckets = [i * (QLState.DIST_MAX_BUCKET_RATIO * QLState.MAX_SCREEN / QLState.DIST_NUM_SMALLER_BUCKETS) \
			for i in range(QLState.DIST_NUM_SMALLER_BUCKETS+1) ]
		self._velocity_buckets= [ i * Car.MAX_VELOCITY / QLState.VEL_NUM_BUCKETS for i in range(QLState.VEL_NUM_BUCKETS) ]

		"""I can tell you're just itching for another one of my essays, right?
		I'll keep this one short: `bisect.bisect` does all of the work for us!
		"""
		self.distances = np.array([ bisect.bisect(self._dist_buckets, distance)-1 for distance in state.distances ])
		self.velocity = np.array([ bisect.bisect(self._velocity_buckets, vel)-1 for vel in state.velocity ])

	def __repr__(self):
		return "<QLState: distances: {}; velocity: {}>".format(str(list(self.distances)), str(list(self.velocity)))

def initArray():
	return collections.defaultdict(int)
