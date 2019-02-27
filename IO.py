"""
Contains classes containing movement features for the car.
"""
import numpy as np
import warnings

class Movement:
	def __init__(self, *args, **kwargs):
		"""Initializes the Movement class. This can be done in two ways. Either with
		four boolean values or with an np_array.

			Note: If you want to initialize with a regular array, just unpack it. E.g.:
				movement = [False, False, True, False]
				Movement(*movement)

				Initializing with an np_array can be done either by passing in an
				np_array positionally or with np_array = (array).

		:left: Whether the car moves left.
		:right: Whether the car moves right.
		:front: Whether the car moves forward.
		:back: Whether the car moves back.
		:np_array: A numpy array from which to read movement values.
		"""
		# If np_array is in the keyword args
		if 'np_array' in kwargs:
			if arg.shape == (4,):
				left, right, front, back = \
					self._np_init(kwargs['np_array'])
			else:
				warnings.warn('Your numpy array does not have the correct shape. Should be (4,).', SyntaxWarning)
				print("Not accepting the keyword argument.")

		# If any of the positionals are numpy arrays
		for arg in args:
			if type(arg) is np.ndarray:
				if arg.shape == (4,):
					left, right, front, back = \
						self._np_init(arg)
				else:
					warnings.warn('Your numpy array does not have the correct shape. Should be (4,).', SyntaxWarning)
					print("Not accepting the variadic positional argument.")

		# If the first four are boolean
		if all(map(lambda x: type(x) is bool, args[:4])):
			left, right, front, back = \
				args[:4]
		
		# Have we defined the variables yet?
		try:
			left
		except NameError:
			# Ya done goofed.
			left, right, front, back = \
				[False]*4
			warnings.warn("Couldn't find any reasonable movement arguments. Taking all directions to be false.", SyntaxWarning)

		# Initialize with the four parameters
		if left and right:
			left = right = False
		if front and back:
			front = back = False

		self.left = left
		self.right = right
		self.front = front
		self.back = back

	def _np_init(self, np_array):
		"""Initializes the Movement class from a numpy array.

			Note: The syntax is the following:
				movement = np.array([0, 0, 1, 0]) # left, right, front, back
				movement = Movement(np_array = movement)
				# or...
				movement = Movement(movement)

		:np_array: A numpy array from which to read movement values.
		"""
		return tuple(map(bool, np_array))

	def asNpArray(self, normalized = False):
		"""Returns the instance of this class as a numpy array.

		:normalized: Whether the array should be normalized (i.e., [1,0,1,0] -> [0.5, 0, 0.5, 0])
		"""
		output = list(map(int, [self.left, self.right, self.front, self.back]))
		output = np.array(output)

		if normalized:
			output = output / sum(output)

		return output
