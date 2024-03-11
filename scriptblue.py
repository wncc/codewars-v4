from random import randint

name = "scriptblue"


def moveTo(x, y, Pirate):
    position = Pirate.GetPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1


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
        pirate.SetTeamSignal(s)

    if (
        (down == "island1" and s[0] != "myCaptured")
        or (down == "island2" and s[1] != "myCaptured")
        or (down == "island3" and s[2] != "myCaptured")
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        pirate.SetTeamSignal(s)

    if (
        (left == "island1" and s[0] != "myCaptured")
        or (left == "island2" and s[1] != "myCaptured")
        or (left == "island3" and s[2] != "myCaptured")
    ):
        s = left[-1] + str(x - 1) + "," + str(y)
        pirate.SetTeamSignal(s)

    if (
        (right == "island1" and s[0] != "myCaptured")
        or (right == "island2" and s[1] != "myCaptured")
        or (right == "island3" and s[2] != "myCaptured")
    ):
        s = right[-1] + str(x + 1) + "," + str(y)
        pirate.SetTeamSignal(s)

    # print(pirate.GetCurrentTeamSignal())
    if pirate.GetCurrentTeamSignal() != "":
        s = pirate.GetCurrentTeamSignal()
        l = s.split(",")
        x = int(l[0][1:])
        y = int(l[1])
        # # print("moveto")
        return moveTo(x, y, pirate)

    else:
        return randint(1, 4)


def ActTeam(team):
    l = team.trackPlayers()
    s = team.GetYourSignal()

    if s:
        island_no = int(s[0])
        signal = l[island_no - 1]
        if signal == "myCaptured":
            team.SetYourSignal("")
