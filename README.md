# CS: 41 Final Project
Members: Jade Lintott (jlintott), Colin Norick (cnorick), Antonio Ferris (antoniof), Parth Sarin (psarin)

There are a few executables in this file:

```
racetrack.py	-	Play the racing game against an AI!
testing.py		-	Run our fully-functional testing suite.
mapCreator.py	-	Design custom maps to play the game on.
```

`racetrack.py` is the main file. Running it will initialize the game with both one human player and one AI player. There are a couple different options for the AI (which you can swap out in `AI.py` by setting the globals at the top). One is merely a set of rules that takes in the distance to the walls and will move in the direction it has farthest to move. This is suprisingly effective and honestly Sam recommending we do that was just a honking good idea. There is also a QLearning implementation.

`testing.py` is a file that the AI team made to test simple behaviors in their AI. It comes with `testing_harness.py` which is a rather nice testing harness and allows you to use decorators to turn functions into tests. We think this alone is a significant contribution to the Python world.

`mapCreator.py` is a file which allows you to create custom maps for the AI to drive on. You can change the map that `racetrack.py` uses on line 133. To create a map, follow these steps:

1. Open `mapCreator.py`
2. Click on the screen to draw connected lines which will be the barriers for the car. Press `d` to make the next click disconnected from the last.
3. Once you're done drawing the barriers, hold `r` and click. Your click will be one end of a reward gate. Click again (without holding anything) to fix the opposite end. Press `d` to make your next click discontinuous and keep clicking to draw reward gates.
4. Once all the reward gates have been drawn, hold `q` and click. The console should have outputted an enthusiastic message for you to pick the starting point. Your next click will be the starting point for the car and the program will close. The map will be stored as `new.map`.

## Controlling the Car
This is pretty straightforward:

```
up		-	Accelerates forward
down	-	Accelerates backwards
right	-	Turns the steering wheel 90 degrees clockwise
left	-	Turns the steering wheel 90 degrees counter-clockwise
```

By default, when you crash into a wall, the car will reset to the starting point. You can change this in `racetrack.py` by changing `RESET` to `False` on line 31.

## Changing the AI
We have a set of variables that dictate the AI in use that can be commented in and out as below. The first one is the Q-Learning implementation. The second is the longest distance based set of rules. The third is Antonio's (minor) changes to the longest distance AI that he seems unreasonably proud of. Just comment these in and out to see each one.

```python
### AIs ###
import AI_longest_distance as ld
import AI_antonio as best
import AI_QLearning as ql
import QLearning

### CURRENT AI PARAMS ###
# # Q-learning
# CURRENT_DECISION_FN = ql.process
# CURRENT_TRAIN_FN = ql.train
# CURRENT_DATA = ql.loadQTable()
# CURRENT_SAVE_FN = ql.writeQTable
# DEFAULT_SAVE_PATH = ql.MEMORY_FILE
# BACKPROPOGATION = True
# BACKPROPOGATION_LEN = int(int(racetrack.FRAME_RATE) / 2)

# Longest distance
CURRENT_DECISION_FN = ld.process
CURRENT_TRAIN_FN = lambda a, b, c, d: None
CURRENT_DATA = None
CURRENT_SAVE_FN = lambda a, b: None
DEFAULT_SAVE_PATH = None
BACKPROPOGATION = False

# Antonio
# CURRENT_DECISION_FN = best.process
# CURRENT_TRAIN_FN = lambda x, y, z, a: x
# CURRENT_DATA = None
# CURRENT_SAVE_FN = lambda x, y: x
# DEFAULT_SAVE_PATH = None
# BACKPROPOGATION = False
```

Just a tip about the success rate (mileage? 😉) you're likely to achieve with each of these algorithms:


>**Q-learning**: This probably won't be very successful, but it will be very entertaining to watch the Car train... You can also tweak parameters in `Car.py` to make the experience more entertaining.  
>**longest_dist**: This is the most reliable. Kinda fun to race against.  
>**Antonio** (the person, not the AI): A knockoff of longest_distance but is more careful to avoid walls. This does cause some other problems though...


## The Parachute AI

I just want to reitrate that Sam is the best person ever for forcing us to implement a very simple AI too. We call it the parachute AI because it would catch us when the QLearning fell, and catch us it did. While we have had some mild sucess with the QLearning, this one is definitely more effective overall. The AI picks the direction that's the farthest away and moves in that direction.

## Q-Learning

Q-learning works by giving the AI a reward or punishment for its actions. Our journey to a "working" q-learning algorithm was very rough; we designed many of our own AI algorithms from scratch before settling on the current implementation which looks very much like the "traditional" q-learning implementation. When you run the Q-learning AI, it won't have any training data. For moderately trained AI's, see the videos. Some of them do pretty well! Mostly not, though...

> With <3 by @jpac