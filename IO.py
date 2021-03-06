"""
Contains classes containing movement features for the car.
"""
import numpy as np
import warnings

class Movement:
    """Captures movement features for the car.

    Acceptable syntax:
        Movement(front=True, right=True)
        Movement(False, False, True, False) # left, right, front, back
        Movement(np.array([0, 1, 0, 0])) # left, right, front, back
        Movement(np_array=np.array([0, 1, 0, 1]))

    Note: If you want to initialize with a regular array instead of a numpy
    array, just unpack it. E.g.:
        movement = [False, False, True, False]
        Movement(*movement)

        Initializing with an np_array can be done either by passing in an
        np_array positionally or with np_array = (array).

    """
    DIR_TO_NUM = {
        (False, False, True, False): 0,
        (False, True, True, False): 1,
        (False, True, False, False): 2,
        (False, True, False, True): 3,
        (False, False, False, True): 4,
        (True, False, False, True): 5,
        (True, False, False, False): 6,
        (True, False, True, False): 7,
        (False, False, False, False): 8
    }

    def __init__(self, *args, **kwargs):
        """Initializes the Movement class.

        :left: Whether the car moves left.
        :right: Whether the car moves right.
        :front: Whether the car moves forward.
        :back: Whether the car moves back.
        :np_array: A numpy array from which to read movement values.
        """
        # Parse the arguments
        left, right, front, back = self._get_params(args, kwargs)

        # Moving in opposite directions goes nowhere
        if left and right:
            left = right = False
        if front and back:
            front = back = False

        # Initialize on the class
        self.left = left
        self.right = right
        self.front = front
        self.back = back

    def asNpArray(self, normalized = False):
        """Returns the instance of this class as a numpy array.

        :normalized: Whether the array should be normalized (i.e., [1,0,1,0] -> [0.5, 0, 0.5, 0])
        """
        output = list(map(int, [self.left, self.right, self.front, self.back]))
        output = np.array(output)

        if normalized:
            output = output / sum(output)

        return output

    def asNum(self):
        """Returns a number representing the direction that the
        movement class is toward, following the convention:
            7    0    1
             \   |   /

             6 – 8 – 2

             /   |   \
            5    4    3

        :returns: the number of the direction representing the class
        """
        return Movement.DIR_TO_NUM[(self.left, self.right, self.front, self.back)]

    def _get_params(self, args, kwargs):
        """Parses `args` and `kwargs` for the left, right, front, and back
        variables.
        """
        # The variables should be false if undefined
        left = right = front = back = False

        # We can get the parameters in many ways...
        # ...if np_array is in the keyword args
        if 'np_array' in kwargs:
            arg = kwargs['np_array']
            if arg.shape == (4,):
                return self._np_init(kwargs['np_array'])
            else:
                warnings.warn('Your numpy array does not have the correct shape. Should be (4,).', SyntaxWarning)
                print("Not accepting the keyword argument {}.".format(str(arg)))

        # ...if any of the positionals are numpy arrays
        for arg in args:
            if type(arg) is np.ndarray:
                if arg.shape == (4,):
                    return self._np_init(arg)
                else:
                    warnings.warn('Your numpy array does not have the correct shape. Should be (4,).', SyntaxWarning)
                    print("Not accepting the variadic positional argument {}.".format(arg))

        # ...if the first four are boolean
        if all(map(lambda x: type(x) is bool, args[:4])) and len(args) == 4:
            return args[:4]

        # ...or if any of the parameters are in kwargs
        if 'left' in kwargs:
            left = kwargs['left']
        if 'right' in kwargs:
            right = kwargs['right']
        if 'front' in kwargs:
            front = kwargs['front']
        if 'back' in kwargs:
            back = kwargs['back']
        
        return left, right, front, back

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

    def __repr__(self):
        """Represents the class as a string.
        """
        labels = ['left', 'right', 'front', 'back']
        ourMovement = [ labels[i] for i, val in enumerate([ self.left, self.right, self.front, self.back ]) if val ]
        if ourMovement:
            return '<IO.Movement: ' + '-'.join(ourMovement) + '>'
        else:
            return '<IO.Movement: no movement>'

    def __eq__(self, other):
        """Compares two different instances of the class by comparing
        their numerical representation.
        """
        return self.asNum() == other.asNum()

    def __hash__(self):
        """Returns a unique hash of the movement class.
        """
        return self.asNum()

class State:
    NUM_DISTANCES = 8
    NUM_VEL = 2
    
    def __init__(self, distances, velocity):
        """Initialize the State class.

        :velocity: An array of two numbers representing the velocity
        :distances: A vector of eight numbers representing the distances
        to the wall in eight directions.

        CONVENTION:
            7    0    1
             \   |   /

             6 – 8 – 2

             /   |   \
            5    4    3
        """
        self.velocity = np.array(velocity)
        self.distances = np.array(distances)
        self.velocity_magnitude = np.linalg.norm(self.velocity)

    def __repr__(self):
        """Represents the class as a string.
        """
        normed_vel = self.velocity
        # if self.velocity_magnitude != 0:
        #     normed_vel /= self.velocity_magnitude

        return '<IO.State: Moving towards {} with speed {}. Distances: {}>'.format(list(normed_vel), round(self.velocity_magnitude, 3), list(self.distances))
