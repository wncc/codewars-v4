import random
from math import floor
def move_Pirate(ip,jp,kp,lp):
    move_prob=str(1)*ip+str(2)*jp+str(3)*kp+str(4)*lp
    return int(move_prob[random.choice(range(ip+jp+kp+lp))])

def ActPirate(Pirate):
    invR=[Pirate.investigate_nw()  , Pirate.investigate_up()  , Pirate.investigate_ne(), 
          Pirate.investigate_left(),                           Pirate.investigate_right(),  
          Pirate.investigate_se()  , Pirate.investigate_down(), Pirate.investigate_sw()]

    
    #canvas dimensions 
    lR= Pirate.GetDimensionX()
    bR= Pirate.GetDimensionY()

    #collecting Pirate's position
    PiratePos=Pirate.GetPosition()
    PirateX= PiratePos[0]
    PirateY= PiratePos[1]

    #collecting Pirate's inital signal
    iSignal=Pirate.GetInitialSignal() #R,xx:yy,A
    temp=iSignal.split(',') 
    baseCoordinates=temp[1].split(':') #coordinates in the form ['xx','yy']
    Bx = int(baseCoordinates[0])
    By = int(baseCoordinates[1])
    aType=temp[2]


    #attack on enemies based on Pirate investigation
    if 'enemy-base' in invR:
        Pirate.DeployVirus(200)              
        #Case Pirate detects enemy base (X condition):                            
        if invR[1]== 'enemy-base' or invR[6]== 'enemy-base' :
            Ax = PirateX
        if invR[2] == 'enemy-base' or invR[4] == 'enemy-base' or invR[5] == 'enemy-base':
            Ax = PirateX+1
        if invR[0]== 'enemy-base' or invR[3]== 'enemy-base' or invR[7] == 'enemy-base':
            Ax = PirateX-1
        #Case Pirate detects enemy base (Y condition):
        if invR[5] == 'enemy-base' or invR[6] == 'enemy-base' or invR[7] == 'enemy-base':
            Ay = PirateY+1
        if invR[4] == 'enemy-base' or invR[3] == 'enemy-base':
            Ay = PirateY
        if invR[1]=='enemy-base' or invR[2] == 'enemy-base' or invR[0] == 'enemy-base':
            Ay = PirateY-1

        sigX=str(Ax)
        sigY=str(Ay)
        if len(sigX)<len(str(lR)):
            sigX='0'*(len(str(lR))-len(sigX))+sigX
        if len(sigY)<len(str(bR)):
            sigY='0'*(len(str(bR))-len(sigY))+sigY
        sendSignal=sigX+':'+sigY  
        Pirate.setSignal('D '+sendSignal)     

        return 0

    #if Pirate encounters enemy
    if 'enemy' in invR:
        Pirate.DeployVirus(200)



    bSignal=Pirate.GetCurrentBaseSignal()

    if aType=='A':
        if bSignal != '':
            ebaseCoordinates=bSignal.split(':') #coordinates in the form ['xx','yy']
            EBx = int(ebaseCoordinates[0])
            EBy = int(ebaseCoordinates[1])        
            #Attacking enemy base!!!!
            if (EBx-PirateX) >= 0:
                goX=2
            if (EBx-PirateX) < 0:
                goX=4
            if (EBy-PirateY) >= 0:
                goY=3
            if (EBy-PirateY) < 0:
                goY=1
            return random.choice([goX,goY])

    #wall bounce
    if PirateX == int(baseCoordinates[0]) and PirateY == int(baseCoordinates[1]):
        Pirate.setSignal('N')
        
    if 'wall' in invR:
        Pirate.setSignal('W')
               
    cSignal = Pirate.GetYourSignal()
        
    if cSignal == 'N':
        #forward Pirate movement
         #Coordinate System
        Dx = (lR-1-2*Bx)/(lR-1)
        Dy = (bR-1-2*By)/(bR-1)
        S = 3* max(lR,bR)           
        C1 = floor((S*abs(Dx))/(abs(Dx)+abs(Dy)))
        C2 = floor((S*abs(Dy))/(abs(Dx)+abs(Dy)))
        ip = floor((C2*By)/(bR-1)) + floor(S*5/6)
        lp = floor((C1*Bx)/(lR-1)) + floor(S*5/6)
        kp = floor((C2*(bR-1-By))/(bR-1)) + floor(S*5/6)
        jp = floor((C1*(lR-1-Bx))/(lR-1)) + floor(S*5/6)
    
        return move_Pirate(ip,jp,kp,lp)
    
        
    if cSignal == 'W':
        return random.randint(1,4)
    
   

def ActBase(base):
    #base investigation of surroundings
    invB=[base.investigate_nw()  , base.investigate_up()  , base.investigate_ne(), 
          base.investigate_left(),                          base.investigate_right(),  
          base.investigate_se()  , base.investigate_down(), base.investigate_sw()]
    
    #canvas dimension
    lB= base.GetDimensionX()
    bB= base.GetDimensionY()

    #position of base
    basePos=base.GetPosition()   
    baseX=str(basePos[0])
    baseY=str(basePos[1])
    if len(baseX)<len(str(lB)):
        baseX='0'*(len(str(lB))-len(baseX))+baseX
    if len(baseY)<len(str(bB)):
        baseY='0'*(len(str(bB))-len(baseY))+baseY
    
    #inital Pirate generation
    if base.GetElixir() > 500:
        ttype='R'    
        atype=random.choice(['A','V'])
        base.create_Pirate(ttype+','+baseX+':'+baseY+','+atype) #R,xx:yy,A
    
    #once the Pirate sends attack signal to base:
    for i in base.GetListOfSignals():
        if i != '':
            if i[0]=='D':
                temp = i.split(' ')
                temp = temp[1]
                base.SetYourSignal(temp)
                break 

    #if base detects enemy bot
    if  'enemy' in invB:
        base.DeployVirus(200)

               
    return
