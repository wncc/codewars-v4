import random
import numpy as np
import math

name = "scriptred"

def moveTo(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if random.randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1


def moveAway(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return random.randint(1, 4)
    if random.randint(1, 2) == 1:
        return (position[0] < x) * 2 + 2
    else:
        return (position[1] > y) * 2 + 1


def circleAround(x, y, radius, Pirate, initial="abc", clockwise=True):
    position = Pirate.getPosition()
    rx = position[0]
    ry = position[1]
    pos = [[x + i, y + radius] for i in range(-1 * radius, radius + 1)]
    pos.extend([[x + radius, y + i] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x + i, y - radius] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x - radius, y + i] for i in range(-1 * radius + 1, radius)])
    if [rx, ry] not in pos:
        if initial != "abc":
            return moveTo(initial[0], initial[1], Pirate)
        if rx in [x + i for i in range(-1 * radius, radius + 1)] and ry in [
            y + i for i in range(-1 * radius, radius + 1)
        ]:
            return moveAway(x, y, Pirate)
        else:
            return moveTo(x, y, Pirate)
    else:
        index = pos.index([rx, ry])
        return moveTo(
            pos[(index + (clockwise * 2) - 1) % len(pos)][0],
            pos[(index + (clockwise * 2) - 1) % len(pos)][1],
            Pirate,
        )

def radius(pirate, x, y, x1, y1, r):
    pos = []
    for i in range(x1 - r, x1 + r + 1):
        for j in range(y1 - r, y1 + r + 1):
            pos.append((i, j))
    t = 0
    if (x, y) in pos:

        circleAround(x1, y1, r, pirate)
    else:
        return moveAway(x1, y1, pirate)


def ActPirate(pirate):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    x, y = pirate.getPosition()
    s = pirate.trackPlayers()
    tmp1 = ""
    tmp2 = ""
    tmp3 = ""
    tmp4 = ""
    if (
        (up == "island1" and s[0] != "myCaptured")
        or (up == "island2" and s[1] != "myCaptured")
        or (up == "island3" and s[2] != "myCaptured")
    ):
        s = up[-1] + str(x) + "," + str(y - 1)
        tmp1 = up[-1] + str(x - 2) + "," + str(y - 1)
        tmp2 = up[-1] + str(x + 2) + "," + str(y - 1)
        tmp3 = up[-1] + str(x) + "," + str(y - 3)
        tmp4 = up[-1] + str(x) + "," + str(y + 1)

        pirate.setTeamSignal(s)

    if (
        (down == "island1" and s[0] != "myCaptured")
        or (down == "island2" and s[1] != "myCaptured")
        or (down == "island3" and s[2] != "myCaptured")
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        tmp1 = up[-1] + str(x - 2) + "," + str(y + 1)
        tmp2 = up[-1] + str(x + 2) + "," + str(y + 1)
        tmp3 = up[-1] + str(x) + "," + str(y - 1)
        tmp4 = up[-1] + str(x) + "," + str(y + 3)
        pirate.setTeamSignal(s)

    if (
        (left == "island1" and s[0] != "myCaptured")
        or (left == "island2" and s[1] != "myCaptured")
        or (left == "island3" and s[2] != "myCaptured")
    ):
        s = left[-1] + str(x - 1) + "," + str(y)
        tmp1 = up[-1] + str(x - 3) + "," + str(y - 1)
        tmp2 = up[-1] + str(x + 1) + "," + str(y - 1)
        tmp3 = up[-1] + str(x - 1) + "," + str(y - 3)
        tmp4 = up[-1] + str(x - 1) + "," + str(y + 1)
        pirate.setTeamSignal(s)

    if (
        (right == "island1" and s[0] != "myCaptured")
        or (right == "island2" and s[1] != "myCaptured")
        or (right == "island3" and s[2] != "myCaptured")
    ):
        s = right[-1] + str(x + 1) + "," + str(y)
        tmp1 = up[-1] + str(x - 1) + "," + str(y - 1)
        tmp2 = up[-1] + str(x + 3) + "," + str(y - 1)
        tmp3 = up[-1] + str(x + 1) + "," + str(y - 3)
        tmp4 = up[-1] + str(x + 1) + "," + str(y + 1)
        pirate.setTeamSignal(s)

    if tmp1 != "":
        pirate.setSignal(tmp1)
        ln = 1
    elif tmp2 != "":
        pirate.setSignal(tmp2)
        rn = 1
    elif tmp3 != "":
        pirate.setSignal(tmp3)
        un = 1
    elif tmp4 != "":
        pirate.setSignal(tmp4)
        dn = 1

    if pirate.getTeamSignal() != "":
        s2 = pirate.getTeamSignal()
        l2 = s.split(",")
        x2 = int(l2[0][1:])
        y2 = int(l2[1])
        position = pirate.getPosition()
        if position[0] == x2 and position[1] == y2:
            return 0
        return moveTo(x2, y2, pirate)


    else:
        # print("randint")
        return random.randint(1, 4)


def ActTeam(team):
    pass
