"""
Module which opens a graphics window in which users can draw their own
maps that can later be loaded as racetracks. Users can also add a start
point and reward gates.
"""
from graphics import * # Here be dragons.
import pickle
DEFAULT_MAP_NAME = 'simple2'
MAP_WIDTH = 800
MAP_HEIGHT = 600

def drawTo(lines, win):
	"""Draws a line on a window.

	:lines: Two points describing the line to be drawn.
	:win: The window to draw on.
	"""
	for p1, p2 in lines:
		gline = Line(p1[0], p1[1], p2[0], p2[1])
		win.draw(gline)

def getBarrierLines(win):
	"""Allows the user to draw the barrier lines by clicking
	on the screen until they press 'd'.

	:win: The active window
	"""
	lines = set()
	p1 = win.getMouse()
	while(True):
		p2 = p1
		p1 = win.getMouse()

		# Press 'd' to return
		key = win.checkKey()
		if key:
			if key == 'd':
				continue
			else:
				break;

		# Add the line to the internal variable
		p1x, p1y = int(p1.x), int(p1.y)
		p2x, p2y = int(p2.x), int(p2.y)
		lines.add(((p1x, p1y), (p2x, p2y)))

		# Draw the line
		gline = Line(p1, p2)
		gline.setWidth(3)
		gline.draw(win)

		print("Now have line", p1, p2)

	return lines

def getRewardLines(win):
	"""Allows the user to draw the reward lines by clicking
	on the screen until they press 'r'.

	:win: The active window
	"""
	lines = set()
	p1 = win.getMouse()
	while(True):
		p2 = p1
		p1 = win.getMouse()

		# Press 'r' to return or 'd' to ignore this line (??)
		key = win.checkKey()
		if key:
			if key == 'd':
				continue
			elif key != 'r':
				break

		# Add the line to the internal variable
		lines.add((p1, p2))
		
		# Draw the line
		gline = Line(p1, p2)
		gline.setFill('green')
		gline.setWidth(3)
		gline.draw(win)

		print("Now have line", p1, p2)

	return lines


if __name__ == '__main__':
	# Initialize the window to create a map
	win = GraphWin("Create a map!", MAP_WIDTH, MAP_HEIGHT)

	# Get barrier lines until the user presses 'd'
	barrierLines = getBarrierLines(win)

	# Get reward lines until the user presses 'r'
	print("Now the reward lines!!!")
	rewardLines = getRewardLines(win)

	# Get the mouse click on the starting point
	print("Now the starting position!")
	start_p = win.getMouse()
	start = (int(start_p.x), int(start_p.y))
	shape = (MAP_WIDTH, MAP_HEIGHT)

	# Save the map data
	map_data = (barrierLines, rewardLines, start, shape)
	pickle.dump(map_data, open(DEFAULT_MAP_NAME + ".map", "wb"))