import math
import Map

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
    if div == 0:
    	return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def convertToTuple(vector2):
	return 1


"""
vision_line is a line from the edge of the map to the edge of the map
vision_line is the "vision" vector emanating from the car
vision_line should be of the form ((x1, y1), (x2, y2))
vision_line's first point (x1, y1) should be the point on the car
barriers is a set of barrier lines
"""







