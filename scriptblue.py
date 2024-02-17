from random import randint,choice

def investigate(Pirate):
        return (Pirate.investigate_nw(), Pirate.investigate_up(), Pirate.investigate_ne(),
                Pirate.investigate_left(), "blank", Pirate.investigate_right(),
                Pirate.investigate_sw(), Pirate.investigate_down(), Pirate.investigate_se())

def moveTo(x,y,Pirate):
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

def moveAway(x,y,Pirate):
        position=Pirate.GetPosition()
        if position[0] == x and position[1] == y:
                return randint(1,4)
        if randint(1,2)==1:
                return (position[0]<x)*2+2
        else:
                return (position[1]>y)*2+1

def circleAround(x,y,radius,Pirate,initial = "abc",clockwise=True):
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
        surr=investigate(Pirate)
        if "enemy-base" in surr:
                index=surr.index("enemy-base")
                oppo_base=Pirate.GetPosition()
                Pirate.setSignal("e"+str(oppo_base[0]+(index%3)-1)+","+str(oppo_base[1]+(int(index/3))-1))
                if Pirate.GetVirus()>100:
                        Pirate.DeployVirus(Pirate.GetVirus())
                        return circleAround(oppo_base[0]+(index%3)-1,oppo_base[1]+(int(index/3))-1,1,Pirate)
        if "enemy" in surr:
                if 'Defender' in Pirate.GetInitialSignal() and Pirate.GetElixir()>2000:
                        Pirate.DeployVirus(1600)
                index=surr.index("enemy")
                enemy=Pirate.GetPosition()
                Pirate.setSignal("r"+str(enemy[0]+(index%3)-1)+","+str(enemy[1]+(int(index/3))-1))
                if Pirate.GetVirus()>200:
                        if Pirate.GetVirus()>1000:
                                if Pirate.GetVirus()>10000:
                                        Pirate.DeployVirus(1000)
                                else:
                                        Pirate.DeployVirus(500)
                        else:
                                Pirate.DeployVirus(200)
                        return circleAround(enemy[0]+(index%3)-1,enemy[1]+(int(index/3))-1,1,Pirate)
        elif Pirate.GetYourSignal() != "" and Pirate.GetYourSignal()[0] == 'r':
                Pirate.setSignal("")
        baseSignal=Pirate.GetCurrentBaseSignal()
        base_signal=baseSignal[1:].split(",")
        if baseSignal != "" and baseSignal[0] == "b": #and Pirate.GetVirus()>1:
                base_signal=[float(base_signal[0]),float(base_signal[1])]
                return circleAround(base_signal[0],base_signal[1],randint(0,2),Pirate,clockwise=choice([True,False]))
        if 'Defender' in Pirate.GetInitialSignal():
                if Pirate.GetYourSignal() == "":
                        if 'Defender1' in Pirate.GetInitialSignal():
                                Pirate.setSignal("do200")
                        else:
                                Pirate.setSignal("du200")
                if Pirate.GetYourSignal()[0] == 'd':
                        if Pirate.GetYourSignal()[1] == "o":
                                if Pirate.GetYourSignal()[2:] == "1":
                                        Pirate.setSignal("du201")
                                base_position=Pirate.GetInitialSignal()[11:]
                                base_position=base_position.split()
                                base_position=[int(base_position[0]),int(base_position[1])]
                                number=int(Pirate.GetInitialSignal()[10])
                                Pirate.setSignal(Pirate.GetYourSignal()[:2]+str(int(Pirate.GetYourSignal()[2:])-1))
                                return circleAround(base_position[0],base_position[1],1,Pirate,[base_position[0]+1*((number%4)-1)*((number%2)-1),base_position[1]+1*(number%4-2)*(number%2)],number%2==0)
                        else:
                                if Pirate.GetYourSignal()[2:] == "1":
                                        Pirate.setSignal("do201")
                                Pirate.setSignal(Pirate.GetYourSignal()[:2]+str(int(Pirate.GetYourSignal()[2:])-1))
        if 'Attacker' in Pirate.GetInitialSignal():
                num=int(Pirate.GetInitialSignal()[8])
                base_position=Pirate.GetInitialSignal()[9:]
                base_position=base_position.split(",")
                if Pirate.GetVirus()>1000:
                        if num==0:
                                return circleAround(Pirate.GetDimensionX()-int(base_position[0]),Pirate.GetDimensionY()-int(base_position[1]),randint(1,3),Pirate)
                        elif num==1:
                                return circleAround(Pirate.GetDimensionX()-int(base_position[0]),int(base_position[1]),randint(1,3),Pirate)
                        elif num==2:
                                return circleAround(int(base_position[0]),Pirate.GetDimensionY()-int(base_position[1]),randint(1,3),Pirate)
                if Pirate.GetVirus()>2000:
                        if num==3:
                                return circleAround(Pirate.GetDimensionX()-int(base_position[0]),Pirate.GetDimensionY()-int(base_position[1]),randint(1,3),Pirate)
                        elif num==4:
                                return circleAround(Pirate.GetDimensionX()-int(base_position[0]),int(base_position[1]),randint(1,3),Pirate)
                        elif num==5:
                                return circleAround(int(base_position[0]),Pirate.GetDimensionY()-int(base_position[1]),randint(1,3),Pirate)
        if baseSignal != "" and baseSignal[0] == "e": 
                if Pirate.GetInitialSignal() == 'Attacker' or randint(1,3)==1:
                        if Pirate.GetVirus()<100:
                                pass
                        else:
                                base_signal=[float(base_signal[0]),float(base_signal[1])]
                                return circleAround(base_signal[0],base_signal[1],1,Pirate)
                if Pirate.GetInitialSignal() == 'Destroyer':
                        base_signal=[float(base_signal[0]),float(base_signal[1])]
                        return circleAround(base_signal[0],base_signal[1],1,Pirate)
        selfSignal=Pirate.GetYourSignal()
        selfSignal=selfSignal.split(",")
        if baseSignal != "" and baseSignal[0] == "r":
                if selfSignal != [""] and selfSignal[0] != "E":
                        if randint(1,10)==1:
                                base_signal=[float(base_signal[0]),float(base_signal[1])]
                                return circleAround(base_signal[0],base_signal[1],1,Pirate)
        if selfSignal == [""] or selfSignal[0] == "r":
                move=randint(1,4)
                Pirate.setSignal("U,"+str(move)+","+str(int(Pirate.GetElixir())))
                return move
        elif selfSignal[0]=="U":
                li=[1,2,3,4]
                dic={1:3,3:1,2:4,4:2}
                li.remove(int(dic[int(selfSignal[1])]))
                move=choice(li)
                if int(Pirate.GetElixir()) > int(selfSignal[2]):
                        Pirate.setSignal("E,"+str(move)+","+str(int(Pirate.GetElixir())))
                else:
                        Pirate.setSignal("U,"+str(move)+","+str(int(Pirate.GetElixir())))
                return move
        elif selfSignal[0]=="E":
                if int(Pirate.GetElixir()) <= int(selfSignal[2])+5:
                        dic={1:3,3:1,2:4,4:2}
                        move=dic[int(selfSignal[1])]
                        Pirate.setSignal("U,"+str(move)+","+str(int(Pirate.GetElixir())))
                        return move
                else:
                        li=[1,2,3,4]
                        dic={1:3,3:1,2:4,4:2}
                        li.remove(dic[int(selfSignal[1])])
                        move=choice(li)
                        Pirate.setSignal("E,"+str(move)+","+str(int(Pirate.GetElixir())))
                        return move
        return randint(1,4)

def ActBase(base):
        signals=base.GetListOfSignals()
        if len(signals)==0:
                for i in range(6):
                        base.create_Pirate('Attacker'+str(i)+str(base.GetPosition()[0])+","+str(base.GetPosition()[1]))
                for i in range(4):
                        base.create_Pirate('Defender1 '+str(i)+str(base.GetPosition()[0])+" "+str(base.GetPosition()[1]))
                for i in range(4):
                        base.create_Pirate('Defender2 '+str(i)+str(base.GetPosition()[0])+" "+str(base.GetPosition()[1]))
        numro=int((base.GetElixir()-500)/50)               
        for i in range(numro):
                base.create_Pirate('Collector')
        if base.GetElixir()>=500 and base.GetYourSignal() != "" and base.GetYourSignal()[0]=='e':
                for i in range(4):
                        base.create_Pirate("Destroyer")
        signals=base.GetListOfSignals()
        for signal in signals:
                if signal != "" and signal[0] == "e":
                        base.SetYourSignal(signal)
                if signal != "" and signal[0] == "r" and not( base.GetYourSignal() !=  "" and base.GetYourSignal()[0] == "e"):
                        base.SetYourSignal(signal)
        if base.GetYourSignal() !=  "":
                base.SetYourSignal(base.GetYourSignal())
        else :
                base.SetYourSignal("")
        surr = investigate(base)
        if "enemy" in surr:
                base.SetYourSignal("b"+str(base.GetPosition()[0])+","+str(base.GetPosition()[1]))
                if base.GetVirus()>800:
                        base.DeployVirus(800)
                else:
                        base.DeployVirus(base.GetVirus())
        if "enemy" not in surr and base.GetYourSignal() != "" and base.GetYourSignal()[0] == "b":
                base.SetYourSignal("")