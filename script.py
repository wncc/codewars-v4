from random import randint,choice

def investigate(Pirate):
        return (Pirate.investigate_nw(), Pirate.investigate_up(), Pirate.investigate_ne(),
                Pirate.investigate_left(), "blank", Pirate.investigate_right(),
                Pirate.investigate_sw(), Pirate.investigate_down(), Pirate.investigate_se())

def moveTo(x, y, Pirate):
        position=Pirate.GetPosition()
        if position[0] == x and position[1] == y:
                return 0
        if position[0] == x:
                return (position[1]<y)*2+1
        if position[1] == y :
                return (position[0]>x)*2+2  
        if randint(1,2)==1:
                return (position[0]>x)*2+2
        else:
                return (position[1]<y)*2+1

def moveAway(x, y, Pirate):
        position=Pirate.GetPosition()
        if position[0] == x and position[1] == y:
                return randint(1,4)
        if randint(1,2)==1:
                return (position[0]<x)*2+2
        else:
                return (position[1]>y)*2+1

def circleAround(x, y, radius, Pirate, initial = "abc", clockwise=True):
        position=Pirate.GetPosition()
        rx=position[0]
        ry=position[1]
        pos=[[x+i,y+radius] for i in range(-1*radius,radius+1)]
        pos.extend([[x+radius,y+i] for i in range(radius-1,-1*radius-1,-1)])
        pos.extend([[x+i,y-radius] for i in range(radius-1,-1*radius-1,-1)])
        pos.extend([[x-radius,y+i] for i in range(-1*radius+1,radius)])
        if [rx,ry] not in pos:
                if initial != "abc":
                        return moveTo(initial[0],initial[1],Pirate)
                if rx in [x+i for i in range(-1*radius,radius+1)] and ry in [y+i for i in range(-1*radius,radius+1)]:
                        return moveAway(x,y,Pirate)
                else :
                        return moveTo(x,y,Pirate)
        else:
                index=pos.index([rx,ry])
                return moveTo(pos[(index+(clockwise*2)-1)%len(pos)][0],pos[(index+(clockwise*2)-1)%len(pos)][1],Pirate)
        
def ActPirate(Pirate):
        pass

def ActTeam(Pirate):
        pass