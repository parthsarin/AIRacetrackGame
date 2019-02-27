"""
Contains classes containing movement features for the car.
"""
class Movement:
	def __init__(self, left, right, front, back):
		if left and right:
			left = right = False
		if front and back:
			front = back = False

		self.left = left
		self.right = right
		self.front = front
		self.back = back