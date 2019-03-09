import IO
import bisect
import racetrack
import Car
import numpy as np
import collections

class QLState:
	DIST_MAX_BUCKET_RATIO = 2/3
	DIST_NUM_SMALLER_BUCKETS = 10
	VEL_NUM_BUCKETS = 10
	MAX_SCREEN = max(racetrack.SCREEN_SIZE)

	def __init__(self, state):
		if type(state) != IO.State:
			raise TypeError("QLState can only be initialized with a state of type IO.State.")

		#calculate what distances correspond to which buckets
		self._dist_buckets = [i * (QLState.DIST_MAX_BUCKET_RATIO * QLState.MAX_SCREEN / QLState.DIST_NUM_SMALLER_BUCKETS) \
			for i in range(QLState.DIST_NUM_SMALLER_BUCKETS+1) ]
		self._velocity_buckets= [ i*Car.MAX_VELOCITY/ QLState.VEL_NUM_BUCKETS for i in range(QLState.VEL_NUM_BUCKETS) ]

		#figure out what bucket our distance belongs in
		self.distances = np.array([ bisect.bisect(self._dist_buckets, distance)-1 for distance in state.distances ])
		self.velocity = np.array([ bisect.bisect(self._velocity_buckets, vel)-1 for vel in state.velocity ])
	
	def asNPArray(self, dist=True, vel=True):
		output = np.array([])

		if dist:
			output = np.array(list(output) + list(self.distances))

		if vel:
			output = np.array(list(output) + list(self.velocity))

		return output

	def __repr__(self):
		return "<QLState: distances: {}; velocity: {}>".format(str(list(self.distances)), str(list(self.velocity)))

	def __hash__(self):
		return hash(str(self.asNPArray))

def initArray():
	return collections.defaultdict(int)