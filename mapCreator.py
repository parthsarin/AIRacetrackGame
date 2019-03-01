from graphics import *
import pickle
DEFAULT_MAP_NAME = 'simple'

def drawTo(lines, win):
	for p1, p2 in lines:
		gline = Line(p1[0], p1[1], p2[0], p2[1])
		win.draw(gline)

def getBarrierLines(win):
	lines = set()
	p1 = win.getMouse()
	while(True):
		p2 = p1
		p1 = win.getMouse()
		key = win.checkKey()
		if key:
			if key == 'd':
				continue
			else:
				break;
		p1x, p1y = int(p1.x), int(p1.y)
		p2x, p2y = int(p2.x), int(p2.y)
		lines.add(((p1x, p1y), (p2x, p2y)))
		gline = Line(p1, p2)
		gline.setWidth(3)
		gline.draw(win)
		print("Now have line", p1, p2)
	return lines

def getRewardLines(win):
	lines = set()
	p1 = win.getMouse()
	while(True):
		p2 = p1
		p1 = win.getMouse()
		key = win.checkKey()
		if key:
			if key == 'd':
				continue
			elif key != 'r':
				break;
		lines.add((p1, p2))
		gline = Line(p1, p2)
		gline.setFill('green')
		gline.setWidth(3)
		gline.draw(win)
		print("Now have line", p1, p2)
	return lines


win = GraphWin("Create a map!", 600, 400)

barrierLines = getBarrierLines(win)
print("Now the reward lines!!!")
rewardLines = getRewardLines(win)
print("Now the starting position!")
start_p = win.getMouse()
start = (int(start_p.x), int(start_p.y))
map_data = (barrierLines, rewardLines, start)
pickle.dump(map_data, open(DEFAULT_MAP_NAME + ".map", "wb"))