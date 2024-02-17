import pygame
from Pirate import Pirate
from pygame.sprite import Sprite

class Base(Sprite):
    def __init__(self, screen, x, y, type, __Pirate_list, __Pirate_map, game):
        super().__init__()
        self.screen = screen
        self.type = type
        self.__Pirate_map = __Pirate_map
        self.__Pirate_list = __Pirate_list
        self.__myGame = game
        self.__SelfElixir = 3000
        self.__TotalTeamElixir = 3000
        self.__TotalVirus = 0
        self.__MovingAverage = 3000
        self.__Signal = ''
        
        if type == "red":
            self.image = pygame.image.load("redbase.png")
        else:
            self.image = pygame.image.load("bluebase.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def actVirus(self, v, pos):
        g = self.__myGame
        if pos[0] < 0 or pos[0] >= g._Game__dim[0]:
            return
        if pos[1] < 0 or pos[1] >= g._Game__dim[1]:
            return
        if self.__Pirate_map[pos[1]][pos[0]]==0:
            g._Game__resources[pos[1]][pos[0]]-= v
            return
        if self.__Pirate_map[pos[1]][pos[0]]==1 and self ==g._Game__redbase:
            self.__TotalVirus += v
            return
        if self.__Pirate_map[pos[1]][pos[0]]==1 and self==g._Game__bluebase:
            g._Game__redbase.VirusOnPirate(pos, v)
            return
        if self.__Pirate_map[pos[1]][pos[0]]==2 and self==g._Game__bluebase:
            self.__TotalVirus += v
            return
        if self.__Pirate_map[pos[1]][pos[0]]==2 and self==g._Game__redbase:
            g._Game__bluebase.VirusOnPirate(pos, v)
            return
        if self.__Pirate_map[pos[1]][pos[0]]==3 and self==g._Game__bluebase:
            if v <= g._Game__redbase.__SelfElixir:
                g._Game__redbase.__SelfElixir -= v
                g._Game__redbase.__TotalTeamElixir -= v
            else:
                g._Game__redbase.__SelfElixir  = 0
                g._Game__redbase.__TotalTeamElixir = 0
            return
        if self.__Pirate_map[pos[1]][pos[0]]==3 and self==g._Game__redbase:
            self.__TotalVirus += v
            return
        if self.__Pirate_map[pos[1]][pos[0]]==4 and self==g._Game__redbase:
            if v <= g._Game__bluebase.__SelfElixir:
                g._Game__bluebase.__SelfElixir -= v
                g._Game__bluebase.__TotalTeamElixir -= v
            else:
                g._Game__bluebase.__SelfElixir = 0
                g._Game__bluebase.__TotalTeamElixir = 0
            return
        if self.__Pirate_map[pos[1]][pos[0]]==4 and self==g._Game__bluebase:
            self.__TotalVirus += v
            return

    def GetListOfSignals(self):
        res = []
        for x in self.__Pirate_list:
            res.append(x._Pirate__Signal)
        return res

    def addResource(self, v):
        if v < 0:
            self.__TotalVirus -= v
        else:
            self.__SelfElixir += v
            self.__TotalTeamElixir += v
        
    def VirusOnPirate(self, pos,virus):
        Pirates = self.__myGame._Game__PositionToPirate[pos]
        if len(Pirates)==0:
            self.__myGame._Game__resources[pos[1]][pos[0]]-= virus
            return
        virus /= len(Pirates)
        delete = []
        for Pirate in Pirates:
            if Pirate._Pirate__selfElixir <= virus:
                e = virus - Pirate._Pirate__selfElixir
                self.__TotalTeamElixir -= Pirate._Pirate__selfElixir
                delete.append(Pirate)
                Pirate.kill()
                self.__Pirate_map[pos[1]][pos[0]] = 0
                self.__myGame._Game__resources[pos[1]][pos[0]]-=e
            else:
                self.__TotalTeamElixir -= virus
                Pirate._Pirate__selfElixir-=virus
        for d in delete:
            del self.__myGame._Game__PositionToPirate[pos][d]
    def create_Pirate(self, signal):
        if self.__SelfElixir >= 50:
            str = 'wncc'
            if type(signal)!=type(str) or len(signal) > 20:
                signal = ''
            self.__SelfElixir -= 50
            #self.GlobalPirateCount += 1
            robo = Pirate(self.screen, self.rect.x, self.rect.y, self.type, signal, self)
            self.__Pirate_list.add(robo)
            if (self.rect.x//20, self.rect.y//20) in self.__myGame._Game__PositionToPirate:
                self.__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][robo] = True
            else:
                self.__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)] = {}
                self.__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][robo] = True
            if self.type == 'red':
                self.__Pirate_map[self.rect.y//20][self.rect.x//20] = 3
            else:
                self.__Pirate_map[self.rect.y//20][self.rect.x//20] = 4

    def investigate_up(self):
        if self.rect.y == 0:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20  - 1][self.rect.x//20] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20  - 1][self.rect.x//20] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20  - 1][self.rect.x//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20  - 1][self.rect.x//20] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"
    

    def investigate_down(self):
        if self.rect.y == 780:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20  + 1][self.rect.x//20] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20  + 1][self.rect.x//20] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20  + 1][self.rect.x//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20  + 1][self.rect.x//20] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"
    
    def investigate_left(self):
        if self.rect.x == 0:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    def investigate_right(self):
        if self.rect.x == 780:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    def investigate_ne(self):
        if self.rect.x == 780 or self.rect.y == 0:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_nw(self):
        if self.rect.x == 0 or self.rect.y == 0:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_se(self):
        if self.rect.x == 780 or self.rect.y == 780:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_sw(self):
        if self.rect.x == 0 or self.rect.y==780:
            return "wall"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__Pirate_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    
    def GetYourSignal(self):
        return self.__Signal
    
    def SetYourSignal(self, s):
        str = 'wncc'
        if type(s)!=type(str) or len(s) > 20:
            return
        self.__Signal = s
    def GetTotalElixir(self):
        return self.__TotalTeamElixir
    def GetElixir(self):
        return self.__SelfElixir
    def GetVirus(self):
        return self.__TotalVirus
    
    def GetPosition(self):
        return (self.rect.x//20,self.rect.y//20)
    
    def GetDimensionX(self):
        return self.__myGame._Game__dim[0]

    def GetDimensionY(self):
        return self.__myGame._Game__dim[1]

    def DeployVirus(self, v):
        if v > self.__TotalVirus or v <= 0:
            return
        self.__TotalVirus -= v
        self.actVirus(v/8,(self.rect.x-1,self.rect.y))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y))
        self.actVirus(v/8,(self.rect.x-1,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x-1,self.rect.y-1))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y-1))
        self.actVirus(v/8,(self.rect.x,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x,self.rect.y-1))

    def blitme(self):
        self.screen.blit(self.image, self.rect)
