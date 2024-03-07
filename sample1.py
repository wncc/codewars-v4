from random import randint

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


def ActPirate(pirate):
        up = pirate.investigate_up()
        down = pirate.investigate_down()
        left = pirate.investigate_left()
        right = pirate.investigate_right()
        x,y = pirate.GetPosition()
        pirate.setSignal('')

        if up == "island1" or up == "island2" or up == "island3":
                s = down[-1] + str(x) + str(y-1)
                pirate.setTeamSignal(s)

        

        if down == "island1" or down == "island2" or down == "island3":
                s = down[-1] + str(x) + str(y+1)
                pirate.setTeamSignal(s)

        if left == "island1" or left == "island2" or left == "island3":
                s = down[-1] + str(x-1) + str(y)
                pirate.setTeamSignal(s)

        if right == "island1" or right == "island2" or right == "island3":
                s = down[-1] + str(x+1) + ',' + str(y)
                pirate.setTeamSignal(s)

        if pirate.getCurrentTeamSignal():
               s = pirate.getCurrentTeamSignal()
               l = s.split(',')
               x = int(l[0][1:])
               y = int(l[1])
               moveTo(x,y,pirate)

        else:
                return randint(1,4)
        
def ActTeam(team):
       l = team.trackPlayers()
       s = team.GetYourSignal()

       if s:
              island_no = int(s[0])
              signal = l[island_no-1]
              if signal == "myCaptured" + str(island_no):
                     signal = ""


        # if up == "enemy-team":
        #         if x < 10:
        #                 msg_x = '0' + str(x)
        #         else: 
        #                 msg_x = str(x)
        #         if y-1 < 10:
        #                 msg_y = '0' + str(y-1)
        #         else:
        #                 msg_y = str(y-1)
        #         msg = "team" + msg_x + msg_y
        #         pirate.setSignal(msg)
        #         if pirate.GetVirus() > 500:
                        # pirate.DeployVirus(500)
        # if down == "enemy" and pirate.GetVirus() > 1000:
        #         pirate.DeployVirus(100)
        # elif down == "enemy-team":
                
        #         if x < 10:
        #                 msg_x = '0' + str(x)
        #         else: 
        #                 msg_x = str(x)
        #         if y+1 < 10:
        #                 msg_y = '0' + str(y+1)
        #         else:
        #                 msg_y = str(y+1)
        #         msg = "team" + msg_x + msg_y
        #         pirate.setSignal(msg)
        #         if pirate.GetVirus() > 500:
        #                 pirate.DeployVirus(500)
        
        # if left == "enemy" and pirate.GetVirus() > 1000:
        #         pirate.DeployVirus(100)
        # elif left == "enemy-team":
        #         if x - 1 < 10:
        #                 msg_x = '0' + str(x-1)
        #         else: 
        #                 msg_x = str(x-1)
        #         if y < 10:
        #                 msg_y = '0' + str(y)
        #         else:
        #                 msg_y = str(y)
        #         msg = "team" + msg_x + msg_y
        #         pirate.setSignal(msg)
        #         if pirate.GetVirus() > 500:
        #                 pirate.DeployVirus(500)
                
        # if right == "enemy" and pirate.GetVirus() > 1000:
        #         pirate.DeployVirus(100)
        # elif right == "enemy-team":
        #         x,y = pirate.GetPosition()
        #         if x+1 < 10:
        #                 msg_x = '0' + str(x+1)
        #         else: 
        #                 msg_x = str(x+1)
        #         if y < 10:
        #                 msg_y = '0' + str(y)
        #         else:
        #                 msg_y = str(y)
        #         msg = "team" + msg_x + msg_y
        #         pirate.setSignal(msg)
        #         if pirate.GetVirus() > 500:
        #                 pirate.DeployVirus(500)
        
        
        # if len(pirate.GetCurrentteamSignal()) > 0:
        #         s = pirate.GetCurrentteamSignal()[4:]
        #         sx = int(s[0:2])
        #         sy = int(s[2:4])
        #         dist = abs(sx-x) + abs(sy-y)
        #         if dist==1:
        #                 pirate.DeployVirus(pirate.GetVirus()*0.75)
        #                 return 0
        #         if x < sx:
        #                 return 2
        #         if x > sx:
        #                 return 4
        #         if y < sy :
        #                 return 3
        #         if y > sy:
        #                 return 1
        # else:
        #         return randint(1,4)
        

def ActTeam(team):
    '''
    Add your code here
    
    '''
    if team.GetElixir() > 700:
        team.create_pirate('')
    L = team.GetListOfSignals()
    for l in L:
        if len(l) > 0:
                team.SetYourSignal(l)
                return

    