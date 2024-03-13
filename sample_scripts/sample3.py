import random
import math

name = "sample3"


def moveTo(x, y, Pirate):
    position = Pirate.GetPosition()
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
    s = pirate.GetCurretPosition()
    x = s[0]
    y = s[1]

b = 0

def Checkisland(pirate):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    if (up == "island1" or down == "island1") and (left == "island1" or right == "island1"):
        return True
    if up == "island2" or down == "island2" or left == "island2"or right == "island2":
        return True
    if up == "island3" or down == "island3" or left == "island3" or right == "island3":
        return True
    else:
        return False

def IslandCoor(pirate):
    up = pirate.investige_up()
    down = pirate.investige_down()
    right = pirate.investige_right()
    left = pirate.investige_left()
    x, y = pirate.GetPosition()
    if up[0:-1] == "island" and down[0:-1] == "island" and right[0:-1] == "island" and left[0:-1] == "island":
        return "centre"    
    if up[0:-1] != "island" and right[0:-1] == "island" and left[0:-1] != "island" and down[0:-1] == "island":
        return "toprleft"
    if up[0:-1] != "island" and right[0:-1] != "island" and left[0:-1] == "island" and down[0:-1] == "island":
        return "topright"
    if up[0:-1] == "island" and right[0:-1] != "island" and left[0:-1] == "island" and down[0:-1] != "island":
        return "bottomright"
    if up[0:-1] == "island" and right[0:-1] == "island" and left[0:-1] != "island" and down[0:-1] != "island":
        return "bottomleft"
    if up[0:-1] == "island" and down[0:-1] == "island" and left[0:-1] == "island" and right[0:-1] != "island":
        return "midlright"
    if up[0:-1] == "island" and down[0:-1] == "island" and left[0:-1] != "island" and right[0:-1] == "island":
        return "midleft"
    if up[0:-1] != "island" and down[0:-1] == "island" and left[0:-1] == "island" and right[0:-1] == "island":
        return "topmid"
    if up[0:-1] == "island" and down[0:-1] != "island" and left[0:-1] == "island" and right[0:-1] == "island":
        return "bottommid"
    

    
def ActPirate(pirate):
    # # print("hell")
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    x, y = pirate.GetPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()
    # # print(s)
    # # print(pirate.GetCurrentTeamSignal())
    if (
        (up == "island1" and s[0] != "myCaptured")
        or (up == "island2" and s[1] != "myCaptured")
        or (up == "island3" and s[2] != "myCaptured")
    ):
        s = up[-1] + str(x) + "," + str(y - 1)
        b += 1
        pirate.setSignal("mid")
        # pirate.SetTeamSignal(s)

    if (
        (down == "island1" and s[0] != "myCaptured")
        or (down == "island2" and s[1] != "myCaptured")
        or (down == "island3" and s[2] != "myCaptured")
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        b += 1
        pirate.setSignal("mid")

        # pirate.SetTeamSignal(s)

    if (
        (left == "island1" and s[0] != "myCaptured")
        or (left == "island2" and s[1] != "myCaptured")
        or (left == "island3" and s[2] != "myCaptured")
    ):
        s = left[-1] + str(x - 1) + "," + str(y)
        b += 1
        # pirate.SetTeamSignal(s)

        pirate.setSignal("mid")


    if (
        (right == "island1" and s[0] != "myCaptured")
        or (right == "island2" and s[1] != "myCaptured")
        or (right == "island3" and s[2] != "myCaptured")
    ):
        s = right[-1] + str(x + 1) + "," + str(y)
        b += 1
        # pirate.SetTeamSignal(s)
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
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x) + "," + str(y + 1)
            pirate.setSignal("move")
    
    if (down == "friend"):
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x) + "," + str(y - 1)
            pirate.setSignal("move")
    
    if (left == "friend"):
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x - 1) + "," + str(y)
            pirate.setSignal("move")
    
    if (right == "friend" ) :
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            s = up[-1] + str(x + 1) + "," + str(y)
            pirate.setSignal("move")

    if (up != "friend" and up != "enemy" ):
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")
    
    if (down != "friend" and down != "enemy"):
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")
    
    if (left != "friend" and left != "enemy" ):
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")
    
    if (right != "friend" and right != "enemy"):
        if Checkisland(pirate) and b<= 4:
            pirate.setSignal("mid")
        else:
            pirate.setSignal("random")

    # print(pirate.GetCurrentTeamSignal())
    if pirate.GetYourSignal() =="mid":
        # print("highsoefji")
        return 0

    elif pirate.GetYourSignal() == "move":
        s = pirate.GetCurrentTeamSignal()
        l = s.split(",")
        x = int(l[0][1:])
        y = int(l[1])
        return moveTo(x, y, pirate)
    
    elif pirate.GetYourSignal() == "random":
        return random.randint(1,4)

def ActTeam(team):
    l = team.trackPlayers()
    s = team.GetYourSignal()

    if s:
        island_no = int(s[0])
        signal = l[island_no - 1]
        if signal == "myCaptured":
            team.SetYourSignal("")