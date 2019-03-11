"""
RACER
"""
import IO
from statistics import mean
DIST_DIFF_TO_ACT = 70
DIST_NOT_FORWARD = 200

def isNear(dirs):
    if mean(dirs) < DIST_DIFF_TO_ACT:
        return True
    return False


def process(state, data, NUM_TO_DIR):
    IGNORE_INDICES = {2, 3, 4, 5, 6}
    dists = state.distances
    # if right is significantly greater than left, or vice versa, act
    defaultDir = None
    rightDirs = dists[1:4]
    leftDirs = dists[5:8]
    r = None
    if isNear(leftDirs) and not isNear(rightDirs):
            if dists[0] < DIST_NOT_FORWARD:
                r = 2 #go right
            # else:
            #     r = 1 #go forward right

    if not r and isNear(rightDirs) and not isNear(leftDirs):
            if dists[0] < DIST_NOT_FORWARD:
                r = 7 #go left
            # else:
            #     r = 7 #go forward left

    if not r:
        sorted_distances = sorted(enumerate(dists), key=lambda x: x[1])[::-1]
        for direction in sorted_distances:
            if direction[0] in IGNORE_INDICES:
                continue
            r = direction[0]
            break

    return IO.Movement(**NUM_TO_DIR[r])
