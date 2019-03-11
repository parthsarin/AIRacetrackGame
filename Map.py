import pygame
import pickle
import utils
import math
import IO
"""Revision history:
 (not complete)
 @Colin changed the globals variable colros to RGB and moved globals to out of the class
"""
BARRIER_WIDTH = 5
BARRIER_COLOR = (0,0,0)
REWARD_GATE_WIDTH = 3
REWARD_GATE_COLOR = (0,255,0)
BARRIER_REWARD = -100
GATE_REWARD = 100
SEEN_GATES = True

class Map:



	def __init__(self, filename):
		#allow for filenames with or without .map
		if filename[-4:] != '.map':
			filename += '.map'
		with open(filename, 'rb') as f:
			map_data = pickle.load(f)
		self.barriers = map_data[0]
		self.reward_gates = set(map_data[1])
		self.starting_point = map_data[2]
		self.shape = map_data[3]
		self.seen_gates = set()

	def getState(self, car):
		distances = self.getDistances(car)
		velocityTuple = utils.convertToTuple(car.velocity)
		velocity = [velocityTuple[0], velocityTuple[1]]
		return IO.State(distances, velocity)



	def getImportantPoints(self, car):
		mid = car.position
		angle = car.angle * math.pi / 180 #car.angle is in degrees
		length_vec = pygame.Vector2(-math.cos(angle), math.sin(angle))
		length_vec.scale_to_length(car.p_length / 2)
		width_vec = pygame.Vector2(math.sin(angle), math.cos(angle))
		width_vec.scale_to_length(car.p_width / 2)
		corner_one = mid - width_vec - length_vec
		corner_two = mid - width_vec + length_vec
		corner_three = mid + width_vec + length_vec
		corner_four = mid + width_vec - length_vec
		return (corner_one, corner_two, corner_three, corner_four, mid)

	"""
	USE THIS FUNCTION for getting distances from car!
	This function generates 8 lines at 45 degree intervals around
	the car starting at the car's angle given and will return
	the distances from the car to the cloest barriers
	"""
	def getDistances(self, car):
		points = self.getImportantPoints(car)
		map(utils.convertToTuple, points)
		corner_one, corner_two, corner_three, corner_four, mid = points

		return self.getDistancesFromPoint(mid, car.angle * math.pi / 180)

	"""
	This function will 
	"""
	def reward(self, car):
		points = self.getImportantPoints(car)
		map(utils.convertToTuple, points)
		corner_one, corner_two, corner_three, corner_four, mid = points

		left = (corner_one, corner_two)
		front = (corner_two, corner_three)
		right = (corner_three, corner_four)
		back = (corner_four, corner_one)
		car_lines = [left, front, right, back]
		reward = 0
		for line in car_lines:
			if self.isIntersectingBarrier(line):
				return BARRIER_REWARD
			if reward != GATE_REWARD and self.isIntersectingRewardGate(line):
				reward = GATE_REWARD

		return reward

	def getDistancesFromPoint(self, p, angle):
		radial_lines = self.generateRadialLines(p, angle)
		distances = []
		for line in radial_lines:
			distances.append(self.getMinDistanceToBarrier(line))

		return distances

	def isIntersectingRewardGate(self, line):
		for reward_line in self.reward_gates - self.seen_gates:
			if utils.intersect(line, reward_line):
				if SEEN_GATES:
					self.seen_gates.add(reward_line)
				return True
		return False

	def isIntersectingBarrier(self, line):
		for barrier in self.barriers:
			if utils.intersect(line, barrier):
				return True
		return False

	def drawOnScreen(self, screen):
		#screen.fill(WHITE)
		for l in self.barriers:
			pygame.draw.line(screen, BARRIER_COLOR, [l[0][0], l[0][1]], [l[1][0], l[1][1]], BARRIER_WIDTH)

		for l in self.reward_gates:
			pygame.draw.line(screen, REWARD_GATE_COLOR, [l[0][0], l[0][1]], [l[1][0], l[1][1]], REWARD_GATE_WIDTH)



	def getMinDistanceToBarrier(self, vision_line):
		min_distance = 100000;
		car_point = vision_line[0]
		for barrier in self.barriers:
			if utils.intersect(vision_line, barrier):
				intersection_point = utils.get_intersection(vision_line, barrier)
				min_distance = min(utils.dist(intersection_point, car_point), min_distance)
		return min_distance

	def getBoundingIntersection(self, stub, pot_line1, pot_line2):
		p1 = utils.get_intersection(stub, pot_line1)
		p2 = utils.get_intersection(stub, pot_line2)
		if not p1:
			return p2
		if not p2:
			return p1
		d1 = utils.dist(p1, stub[0])
		d2 = utils.dist(p2, stub[0])
		if d1 < d2:
			return p1
		return p2


	"""
	Generate 8 45 degree seperated lines
	emanating from p starting at angle initial_angle
	These lines stop when they hit max_x/min_x, or max_y/min_y

	"""
	def generateRadialLines(self, p, initial_angle):
		max_x = self.shape[0]
		max_y = self.shape[1]
		min_x = 0
		min_y = 0

		lines = list()

		#Construct bounding box
		topLine = ((min_x, max_y), (max_x, max_y))
		botLine = ((min_x, min_y), (max_x, min_y))
		rightLine = ((max_x, min_y), (max_x, max_y))
		leftLine = ((min_x, min_y), (min_x, max_y))

		for i in range(8):
			angle = initial_angle - i * math.pi / 4

			if angle < 0:
				angle += 2 * math.pi

			stub = (p, (p[0] + math.cos(angle), p[1] + math.sin(angle)))

			if 0 <= angle <= math.pi / 2:
				last_point = self.getBoundingIntersection(stub, topLine, rightLine)
			elif math.pi / 2 <= angle <= math.pi:
				last_point = self.getBoundingIntersection(stub, topLine, leftLine)
			elif math.pi <= angle <= 3 * math.pi / 2:
				last_point = self.getBoundingIntersection(stub, botLine, leftLine)
			elif 3 * math.pi / 2 <= angle <= 2 * math.pi:
				last_point = self.getBoundingIntersection(stub, botLine, rightLine)
			else:
				raise Exception("Angle generated not in normal bounds")
				return None
			lines.append((p, last_point))
		
		return lines

	def __str__(self):
		s = "Barriers: " + repr(self.barriers) + "\n"
		s += "Reward Gates: " + repr(self.reward_gates) + "\n"
		s += "Starting Point: " + repr(self.starting_point) + "\n"
		s += "Shape: " + repr(self.shape) + "\n"
		return s


if __name__ == '__main__':
	test_map = Map('donut')
	print(test_map)



"""
we can weight them by the car's length to get smaller values easily
There is one way to solve this.
Involves a change to map structure to construct a list of reward gates
which must then be ticked off / tracked by the Map class
This would also preclude multiple cars on 1 map
or Map would need a list of cars to track...
for now, just front / back lines into this function?



"""