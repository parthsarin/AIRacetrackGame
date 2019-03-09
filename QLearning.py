import IO # for processing state and movement
import bisect # for identifying which bucket values fall into
import contextlib # for silencing racetrack... YES IT BOTHERS ME THAT MUCH, OKAY
with contextlib.redirect_stdout(None):
    import racetrack # sadly, this is just for a single value
import Car # for the car's max velocity
import numpy as np # for everything math-y
import collections # for storing the q-table as a defaultdict

class QLState:
	DIST_MAX_BUCKET_RATIO = 2/3
	DIST_NUM_SMALLER_BUCKETS = 10
	VEL_NUM_BUCKETS = 10
	MAX_SCREEN = max(racetrack.SCREEN_SIZE)

	def __init__(self, state):
		if type(state) != IO.State and type(state) != np.ndarray:
			raise TypeError("QLState can only be initialized with a state of type IO.State.")

		#calculate what distances correspond to which buckets
		self._dist_buckets = [i * (QLState.DIST_MAX_BUCKET_RATIO * QLState.MAX_SCREEN / QLState.DIST_NUM_SMALLER_BUCKETS) \
			for i in range(QLState.DIST_NUM_SMALLER_BUCKETS+1) ]
		self._velocity_buckets= [ i*Car.MAX_VELOCITY/ QLState.VEL_NUM_BUCKETS for i in range(QLState.VEL_NUM_BUCKETS) ]

		if type(state) == IO.State:
			#figure out what bucket our distance belongs in
			self.distances = np.array([ bisect.bisect(self._dist_buckets, distance)-1 for distance in state.distances ])
			self.velocity = np.array([ bisect.bisect(self._velocity_buckets, vel)-1 for vel in state.velocity ])

		elif type(state) == np.ndarray:
			self.distances = state[:IO.State.NUM_DISTANCES]
			self.velocity = state[IO.State.NUM_DISTANCES:]
	
	def asNPArray(self, dist=True, vel=True):
		output = np.array([])

		if dist:
			output = np.array(list(output) + list(self.distances))

		if vel:
			output = np.array(list(output) + list(self.velocity))

		return output

	def __repr__(self):
		return "<QLState: distances: {}; velocity: {}>".format(str(list(self.distances)), str(list(self.velocity)))

class QLStateAction:
	def __init__(self, state, action):
		self.state = state
		self.action = action

	def __hash__(self):
		output = 0
		i = 0
		for val in self.state.distances:
			output += val * (11 ** i)
			i += 1

		for val in self.state.velocity:
			output += val * (11 ** i)
			i += 1

		output += self.action.asNum() * (11 ** i)

		return int(output)

def initArray():
	return collections.defaultdict(int)
