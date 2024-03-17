import random
import math

name = "sample3"


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

def setthem(pirate):
    s = pirate.getPosition()
    x = s[0]
    y = s[1]

b = 0

def checkIsland(pirate):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    if (up[0:-1] == "island" or down[0:-1] == "island") and (left[0:-1] == "island" or right[0:-1] == "island"):
        return True
    else:
        return False

def positionInIsland(pirate):
    up = pirate.investige_up()
    down = pirate.investige_down()
    right = pirate.investige_right()
    left = pirate.investige_left()
    x, y = pirate.getPosition()
    if up[0:-1] == "island" and down[0:-1] == "island" and right[0:-1] == "island" and left[0:-1] == "island":
        return "centre"    
    if up[0:-1] != "island" and right[0:-1] == "island" and left[0:-1] != "island" and down[0:-1] == "island":
        return "topleft"
    if up[0:-1] != "island" and right[0:-1] != "island" and left[0:-1] == "island" and down[0:-1] == "island":
        return "topright"
    if up[0:-1] == "island" and right[0:-1] != "island" and left[0:-1] == "island" and down[0:-1] != "island":
        return "bottomright"
    if up[0:-1] == "island" and right[0:-1] == "island" and left[0:-1] != "island" and down[0:-1] != "island":
        return "bottomleft"
    if up[0:-1] == "island" and down[0:-1] == "island" and left[0:-1] == "island" and right[0:-1] != "island":
        return "middleright"
    if up[0:-1] == "island" and down[0:-1] == "island" and left[0:-1] != "island" and right[0:-1] == "island":
        return "middleleft"
    if up[0:-1] != "island" and down[0:-1] == "island" and left[0:-1] == "island" and right[0:-1] == "island":
        return "topmiddle"
    if up[0:-1] == "island" and down[0:-1] != "island" and left[0:-1] == "island" and right[0:-1] == "island":
        return "bottommiddle"
    
def ActPirate(pirate):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    x, y = pirate.getPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()
    
    if (
        (up == "island1" and s[0] != "myCaptured")
        or (up == "island2" and s[1] != "myCaptured")
        or (up == "island3" and s[2] != "myCaptured")
    ):
        s = up[-1] + str(x) + "," + str(y - 1)
        b += 1
        pirate.setSignal("mid")

    if (
        (down == "island1" and s[0] != "myCaptured")
        or (down == "island2" and s[1] != "myCaptured")
        or (down == "island3" and s[2] != "myCaptured")
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        b += 1
        pirate.setSignal("mid")

    if (
        (left == "island1" and s[0] != "myCaptured")
        or (left == "island2" and s[1] != "myCaptured")
        or (left == "island3" and s[2] != "myCaptured")
    ):
        s = left[-1] + str(x - 1) + "," + str(y)
        b += 1

        pirate.setSignal("mid")


    if (
        (right == "island1" and s[0] != "myCaptured")
        or (right == "island2" and s[1] != "myCaptured")
        or (right == "island3" and s[2] != "myCaptured")
    ):
        s = right[-1] + str(x + 1) + "," + str(y)
        b += 1
        pirate.setSignal("mid")


    if (
        (up == "island1" and s[0] == "myCaptured")
        or (up == "island2" and s[1] == "myCaptured")
        or (up == "island3" and s[2] == "myCaptured") 
    ):
        pirate.setSignal("mid")

    if (
        (right == "island1" and s[0] == "myCaptured")
        or (right == "island2" and s[1] == "myCaptured")
        or (right == "island3" and s[2] == "myCaptured") 
    ):
        # pirate.SetTeamSignal(s)
        pirate.setSignal("mid")

    if (
        (down == "island1" and s[0] == "myCaptured")
        or (down == "island2" and s[1] == "myCaptured")
        or (down == "island3" and s[2] == "myCaptured") 
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        pirate.setSignal("mid")


    if (
            (left == "island1" and s[0] == "myCaptured")
            or (left == "island2" and s[1] == "myCaptured")
            or (left == "island3" and s[2] == "myCaptured") 
        ):
            pirate.setSignal("mid")

    if (up == "friend"):
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x) + "," + str(y + 1)
            pirate.setSignal("move")
    
    if (down == "friend"):
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x) + "," + str(y - 1)
            pirate.setSignal("move")
    
    if (left == "friend"):
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x - 1) + "," + str(y)
            pirate.setSignal("move")
    
    if (right == "friend" ) :
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x + 1) + "," + str(y)
            pirate.setSignal("move")

    if (up != "friend" and up != "enemy" ):
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")
    
    if (down != "friend" and down != "enemy"):
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")
    
    if (left != "friend" and left != "enemy" ):
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")
    
    if (right != "friend" and right != "enemy"):
        if checkIsland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")

    if pirate.getSignal() =="mid":
        return 0

    elif pirate.getSignal() == "move":
        s = pirate.GetCurrentTeamSignal()
        l = s.split(",")
        x = int(l[0][1:])
        y = int(l[1])
        return moveTo(x, y, pirate)
    
    elif pirate.getSignal() == "random":
        return random.randint(1,4)

def ActTeam(team):
    l = team.trackPlayers()
    s = team.getTeamSignal()

    if s:
        island_no = int(s[0])
        signal = l[island_no - 1]
        if signal == "myCaptured":
            team.setTeamSignal("")