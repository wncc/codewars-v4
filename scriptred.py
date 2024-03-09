# from random import randint

# def moveTo(x, y, Pirate):
#         position=Pirate.GetPosition()
#         if position[0] == x and position[1] == y:
#                 return 0
#         if position[0] == x:
#                 return (position[1]<y)*2+1
#         if position[1] == y :
#                 return (position[0]>x)*2+2
#         if randint(1,2)==1:
#                 return (position[0]>x)*2+2
#         else:
#                 return (position[1]<y)*2+1


# def ActPirate(pirate):
#         # print("hell")
#         up = pirate.investigate_up()
#         down = pirate.investigate_down()
#         left = pirate.investigate_left()
#         right = pirate.investigate_right()
#         x,y = pirate.GetPosition()
#         pirate.setSignal('')
#         s = pirate.trackPlayers()
#         print(s)
#         print(pirate.GetCurrentTeamSignal())
#         if (up == "island1" and s[0] !="myCaptured1") or (up == "island2" and s[1] != "myCaptured2") or (up == "island3" and s[2]!="myCaptured3"):
#                 s = up[-1] + str(x)+ ',' + str(y-1)
#                 # print(s)
#                 # print("herhe")
#                 # print(pirate._Pirate__myTeam._Team__base)
#                 pirate.SetTeamSignal(s)

#         if (down == "island1" and s[0] !="myCaptured1") or (down == "island2" and s[1] != "myCaptured2") or (down == "island3" and s[2]!="myCaptured3"):
#                 s = down[-1] + str(x)+ ',' + str(y+1)
#                 # print(s)
#                 # print("herhe")
#                 # print("herhe")
#                 # print(pirate._Pirate__myTeam._Team__base)
#                 pirate.SetTeamSignal(s)

#         if (left == "island1" and s[0] !="myCaptured1") or (left == "island2" and s[1] != "myCaptured2") or (left == "island3" and s[2]!="myCaptured3"):
#                 s = left[-1] + str(x-1) + ','+ str(y)
#                 # print("herhe")
#                 # print(s)
#                 # print("herhe")
#                 # print(pirate._Pirate__myTeam._Team__base)
#                 pirate.SetTeamSignal(s)

#         if (right == "island1" and s[0] !="myCaptured1") or (right == "island2" and s[1] != "myCaptured2") or (right == "island3" and s[2]!="myCaptured3"):
#                 s = right[-1] + str(x+1) + ',' + str(y)
#                 # print("herhe")
#                 # print(s)
#                 # print("herhe")
#                 # print(pirate._Pirate__myTeam._Team__base)
#                 pirate.SetTeamSignal(s)

#         print(pirate.GetCurrentTeamSignal())
#         if pirate.GetCurrentTeamSignal() != "":
#                 s = pirate.GetCurrentTeamSignal()
#                 l = s.split(',')
#                 x = int(l[0][1:])
#                 y = int(l[1])
#                 print("moveto")
#                 return moveTo(x,y,pirate)

#         else:
#                 print("randint")
#                 return randint(1,4)

# def ActTeam(team):
#        l = team.trackPlayers()
#        s = team.GetYourSignal()

#        if s:
#         #       print(s)
#                 island_no = int(s[0])
#                 signal = l[island_no-1]
#         #       print(signal)
#         #       print(island_no)
#                 if signal == "myCaptured" + str(island_no):
#                      print("signal reset here")
#                      team.SetYourSignal("")


from random import randint, choice

# ln=0
# rn=0
# un=0
# dn=0

# def investigate(Pirate):
#         return (Pirate.investigate_nw(), Pirate.investigate_up(), Pirate.investigate_ne(),
#                 Pirate.investigate_left(), "blank", Pirate.investigate_right(),
#                 Pirate.investigate_sw(), Pirate.investigate_down(), Pirate.investigate_se())
name = "scriptred"


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


def moveAway(x, y, Pirate):
    position = Pirate.GetPosition()
    if position[0] == x and position[1] == y:
        return randint(1, 4)
    if randint(1, 2) == 1:
        return (position[0] < x) * 2 + 2
    else:
        return (position[1] > y) * 2 + 1


def circleAround(x, y, radius, Pirate, initial="abc", clockwise=True):
    position = Pirate.GetPosition()
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


# def ActPirate(Pirate):
#         Pirate._Pirate__myTeam.buildWalls(Pirate._Pirate__myTeam._Team__myGame._Game__island1, Pirate._Pirate__myTeam._Team__myGame._Game__island2, Pirate._Pirate__myTeam._Team__myGame._Game__island3, 1)
#         Pirate._Pirate__myTeam.buildWalls(Pirate._Pirate__myTeam._Team__myGame._Game__island1, Pirate._Pirate__myTeam._Team__myGame._Game__island2, Pirate._Pirate__myTeam._Team__myGame._Game__island3, 2)
#         Pirate._Pirate__myTeam.buildWalls(Pirate._Pirate__myTeam._Team__myGame._Game__island1, Pirate._Pirate__myTeam._Team__myGame._Game__island2, Pirate._Pirate__myTeam._Team__myGame._Game__island3, 3)
#         return randint(1, 4)

# def deployPirates():
#         # returns a list of coordinates to deploy pirates
#         pass

# def ActTeam(Team):
#         pass


# def setpos(pirate, x,y, x1 ,y1,r):


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
    x, y = pirate.GetPosition()
    s = pirate.trackPlayers()
    tmp1 = ""
    tmp2 = ""
    tmp3 = ""
    tmp4 = ""
    # pirate.setSignal("")
    if (
        (up == "island1" and s[0] != "myCaptured1")
        or (up == "island2" and s[1] != "myCaptured2")
        or (up == "island3" and s[2] != "myCaptured3")
    ):
        s = up[-1] + str(x) + "," + str(y - 1)
        tmp1 = up[-1] + str(x - 2) + "," + str(y - 1)
        tmp2 = up[-1] + str(x + 2) + "," + str(y - 1)
        tmp3 = up[-1] + str(x) + "," + str(y - 3)
        tmp4 = up[-1] + str(x) + "," + str(y + 1)

        pirate.SetTeamSignal(s)

    if (
        (down == "island1" and s[0] != "myCaptured1")
        or (down == "island2" and s[1] != "myCaptured2")
        or (down == "island3" and s[2] != "myCaptured3")
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        tmp1 = up[-1] + str(x - 2) + "," + str(y + 1)
        tmp2 = up[-1] + str(x + 2) + "," + str(y + 1)
        tmp3 = up[-1] + str(x) + "," + str(y - 1)
        tmp4 = up[-1] + str(x) + "," + str(y + 3)
        pirate.SetTeamSignal(s)

    if (
        (left == "island1" and s[0] != "myCaptured1")
        or (left == "island2" and s[1] != "myCaptured2")
        or (left == "island3" and s[2] != "myCaptured3")
    ):
        s = left[-1] + str(x - 1) + "," + str(y)
        tmp1 = up[-1] + str(x - 3) + "," + str(y - 1)
        tmp2 = up[-1] + str(x + 1) + "," + str(y - 1)
        tmp3 = up[-1] + str(x - 1) + "," + str(y - 3)
        tmp4 = up[-1] + str(x - 1) + "," + str(y + 1)
        pirate.SetTeamSignal(s)

    if (
        (right == "island1" and s[0] != "myCaptured1")
        or (right == "island2" and s[1] != "myCaptured2")
        or (right == "island3" and s[2] != "myCaptured3")
    ):
        s = right[-1] + str(x + 1) + "," + str(y)
        tmp1 = up[-1] + str(x - 1) + "," + str(y - 1)
        tmp2 = up[-1] + str(x + 3) + "," + str(y - 1)
        tmp3 = up[-1] + str(x + 1) + "," + str(y - 3)
        tmp4 = up[-1] + str(x + 1) + "," + str(y + 1)
        pirate.SetTeamSignal(s)

    # print("fjfjf")

    if tmp1 != "":
        print("not here")
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

    print("herhe")
    print(pirate.GetYourSignal())
    if pirate.GetYourSignal() != "":
        s2 = pirate.GetYourSignal()
        l2 = s.split(",")
        x2 = int(l2[0][1:])
        y2 = int(l2[1])
        position = pirate.GetPosition()
        if position[0] == x2 and position[1] == y2:
            return 0
        return moveTo(x2, y2, pirate)

    # elif pirate.GetCurrentTeamSignal() != "":
    #         s = pirate.GetCurrentTeamSignal()
    #         l = s.split(',')
    #         x1 = int(l[0][1:])
    #         y1 = int(l[1])
    #         print("moveto")
    #         return moveTo(x1,y1, pirate)

    else:
        print("randint")
        return randint(1, 4)


def ActTeam(team):
    pass
