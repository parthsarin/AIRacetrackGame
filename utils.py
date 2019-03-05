import math


def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

def ccw(A,B,C):
		Ax, Ay = A
		Bx, By = B
		Cx, Cy = C
		return (Cy-Ay) * (Bx-Ax) > (By-Ay) * (Cx-Ax)

# Return true if line segments AB and CD intersect
def intersect(L1, L2):
	A, B = L1
	C, D = L2
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def dist(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def get_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


"""
vision_line is a line from the edge of the map to the edge of the map
vision_line is the "vision" vector emanating from the car
vision_line should be of the form ((x1, y1), (x2, y2))
vision_line's first point (x1, y1) should be the point on the car
barriers is a set of barrier lines
"""
def getMinDistanceToBarrier(vision_line, barriers):
	min_distance = 100000;
	car_point = vision_line[0]
	for barrier in barriers:
		if intersect(vision_line, barrier):
			intersection_point = get_intersection(vision_line, barrier)
			min_distance = math.min(dist(intersection_point, car_point), min_distance)
	return min_distance

"""
Generate 8 45 degree seperated lines
emanating from p starting at angle initial_angle
These lines stop when they hit max_x/min_x, or max_y/min_y

"""
def generateRadialLines(p, initial_angle, max_x, min_x, max_y, min_y):
	#Construct bounding box
	topLine = ((min_x, max_y), (max_x, max_y))
	botLine = ((min_x, min_y), (max_x, min_y))
	rightLine = ((max_x, min_y), (max_x, max_y))
	leftLine = ((min_x, min_y), (min_x, max_y))

	for i in range(8):
		angle = initial_angle + i * math.pi / 2


