import pygame
from pygame.sprite import Sprite

class Pirate(Sprite):
    def __init__(self, screen, x, y, type, team, signal):
        super().__init__()
        self.screen = screen
        self.type = type
        # print(team._Team__curr_frame)
        self.__myTeam = team
        if self.type == 'red':
            self.image = pygame.image.load('images/pirate.jpg')
        else:
            self.image = pygame.image.load('images/pirateblue.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__initialSignal = signal
        self.__signal = ''

    def move_up(self, island1, island2, island3):
        if self.rect.y >0:
            #self.__myBase.pirate_map[self.rect.x//20][self.rect.y//20] = 0
            # print("move up")
            
            try:
                del self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self]
            except:
                return
            # print(self.rect.x//20, self.rect.y//20)
            if (self.rect.x//20, self.rect.y//20) not in island1.coordi and (self.rect.x//20, (self.rect.y-20)//20) in island1.coordi:
                # print("here")
                if island1.red_wall or island1.blue_wall:
                    self.rect.y += 20
                else:
                    if self.type == 'red':
                        island1.red_present = True
                        # print(island1.red_present)
                    
                    else:
                        island1.blue_present = True
            if (self.rect.x//20, self.rect.y//20) not in island2.coordi and (self.rect.x//20, (self.rect.y-20)//20) in island2.coordi:
                # print("here")
                if island2.red_wall or island2.blue_wall:
                    self.rect.y += 20
                else:
                        
                    if self.type == 'red':
                        island2.red_present = True
                        # print(island2.red_present)
                    else:
                        island2.blue_present = True
            if (self.rect.x//20, self.rect.y//20) not in island3.coordi and  (self.rect.x//20, (self.rect.y-20)//20) in island3.coordi:
                # print("here")
                if island3.red_wall or island3.blue_wall:
                    self.rect.y += 20
                else:
                    if self.type == 'red':
                        island3.red_present = True
                        # print(island3.red_present)
                    else:
                        island3.blue_present = True


            if (self.rect.x//20, self.rect.y//20) in island1.coordi and (self.rect.x//20, (self.rect.y-20)//20) not in island1.coordi:
                if island1.red_wall or island1.blue_wall:
                    self.rect.y += 20
                else:

                    if self.type == "red" and not self.friend_present(island1, "red"):
                        island1.red_present = False
                    elif self.type == "blue" and not self.friend_present(island1, "blue"):
                        island1.blue_present = False

            if (self.rect.x//20, self.rect.y//20) in island2.coordi and (self.rect.x//20, (self.rect.y-20)//20) not in island2.coordi:
                if island2.red_wall or island2.blue_wall:
                    self.rect.y += 20
                else:
                    if self.type == "red" and not self.friend_present(island2, "red"):
                        island2.red_present = False
                    elif self.type == "blue" and not self.friend_present(island2, "blue"):
                        island2.blue_present = False
            
            if (self.rect.x//20, self.rect.y//20) in island3.coordi and (self.rect.x//20, (self.rect.y-20)//20) not in island3.coordi:
                if island3.red_wall or island3.blue_wall:
                    self.rect.y += 20
                else:
                    if self.type == "red" and not self.friend_present(island3, "red"):
                        island3.red_present = False
                    elif self.type == "blue" and not self.friend_present(island3, "red"):
                        island3.blue_present = False

            # print("ho")
                
                
            self.rect.y -= 20
            # print(self.rect.x//20, self.rect.y//20)
            if (self.rect.x//20, self.rect.y//20) in self.__myTeam._Team__myGame._Game__PositionToPirate:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            else:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)] = {}
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            if self.type == 'red': 
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 1
            else:
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 2

    def friend_present(self, island, type3):
        for pirate in self.__myTeam._Team__pirate_list:
            if pirate.rect in island.coordi and pirate.type == self.type and pirate != self:
                return True
        return False            

    def move_down(self, island1, island2, island3):
        if self.rect.y < (self.__myTeam._Team__myGame._Game__dim[1]-1)*20:
            #self.__myBase.pirate_map[self.rect.x//20][self.rect.y//20] = 0
            try:
                del self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self]
            except:
                return
            
            if (self.rect.x//20, self.rect.y//20) not in island1.coordi and (self.rect.x//20, (self.rect.y+20)//20) in island1.coordi:
                if island1.red_wall or island1.blue_wall:
                    self.rect.y -= 20
                else:
                    if self.type == 'red':
                        island1.red_present = True
                        # print(island1.red_present)
                    else:
                        island1.blue_present = True
            if (self.rect.x//20, self.rect.y//20) not in island2.coordi and (self.rect.x//20, (self.rect.y+20)//20) in island2.coordi:
                if island2.red_wall or island2.blue_wall:
                    self.rect.y -= 20
                else:
                    if self.type == 'red':
                        island2.red_present = True
                        # print(island2.red_present)
                    else:
                        island2.blue_present = True
            if (self.rect.x//20, self.rect.y//20) not in island3.coordi and (self.rect.x//20, (self.rect.y+20)//20) in island3.coordi:
                if island3.red_wall or island3.blue_wall:
                    self.rect.y -= 20
                else:
                    if self.type == 'red':
                        island3.red_present = True
                        # print(island3.red_present)
                    else:
                        island3.blue_present = True
            
            if (self.rect.x//20, self.rect.y//20) in island1.coordi and (self.rect.x//20, (self.rect.y+20)//20) not in island1.coordi:
                if island1.red_wall or island1.blue_wall:
                    self.rect.y -= 20
                else:
                    if self.type == "red" and not self.friend_present(island1, "red"):
                        island1.red_present = False
                    elif self.type == "blue" and not self.friend_present(island1, "blue"):
                        island1.blue_present = False
            
            if (self.rect.x//20, self.rect.y//20) in island2.coordi and (self.rect.x//20, (self.rect.y+20)//20) not in island2.coordi:
                if island2.red_wall or island2.blue_wall:
                    self.rect.y -= 20
                else:
                    if self.type == "red" and not self.friend_present(island2, "red"):
                        island2.red_present = False
                    elif self.type == "blue" and not self.friend_present(island2, "blue"):
                        island2.blue_present = False

            if (self.rect.x//20, self.rect.y//20) in island3.coordi and (self.rect.x//20, (self.rect.y+20)//20) not in island3.coordi:
                if island3.red_wall or island3.blue_wall:
                    self.rect.y -= 20
                else:
                    if self.type == "red" and not self.friend_present(island3, "red"):
                        island3.red_present = False
                    elif self.type == "blue" and not self.friend_present(island3, "red"):
                        island3.blue_present = False   
            


            self.rect.y += 20
            if (self.rect.x//20, self.rect.y//20) in self.__myTeam._Team__myGame._Game__PositionToPirate:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            else:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)] = {}
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            if self.type == 'red': 
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 1
            else:
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 2

    def move_left(self, island1, island2, island3):
        if self.rect.x > 0:
            
            try:
                del self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self]
            except:
                return
            
            if (self.rect.x//20, self.rect.y//20) not in island1.coordi and ((self.rect.x-20)//20, self.rect.y//20) in island1.coordi:
                if island1.red_wall or island1.blue_wall:
                    self.rect.x += 20
                else:
                    if self.type == 'red':
                        island1.red_present = True
                        # print(island1.red_present)
                    else:
                        island1.blue_present = True

            if (self.rect.x//20, self.rect.y//20) not in island2.coordi and ((self.rect.x-20)//20, self.rect.y//20) in island2.coordi:
                if island2.red_wall or island2.blue_wall:
                    self.rect.x += 20
                else:
                    if self.type == 'red':
                        island2.red_present = True
                        # print(island2.red_present)
                    else:
                        island2.blue_present = True
            
            if (self.rect.x//20, self.rect.y//20) not in island3.coordi and ((self.rect.x-20)//20, self.rect.y//20) in island3.coordi:
                if island3.red_wall or island3.blue_wall:
                    self.rect.x += 20
                else:
                    if self.type == 'red':
                        island3.red_present = True
                        # print(island3.red_present)
                    else:
                        island3.blue_present = True

            if (self.rect.x//20, self.rect.y//20) in island1.coordi and ((self.rect.x-20)//20, self.rect.y//20) not in island1.coordi:
                if island1.red_wall or island1.blue_wall:
                    self.rect.x += 20
                else:
                    if self.type == "red" and not self.friend_present(island1, "red"):
                        island1.red_present = False
                    elif self.type == "blue" and not self.friend_present(island1, "blue"):
                        island1.blue_present = False

            if (self.rect.x//20, self.rect.y//20) in island2.coordi and ((self.rect.x-20)//20, self.rect.y//20) not in island2.coordi:
                if island2.red_wall or island2.blue_wall:
                    self.rect.x += 20
                else:
                    if self.type == "red" and not self.friend_present(island2, "red"):
                        island2.red_present = False
                    elif self.type == "blue" and not self.friend_present(island2, "blue"):
                        island2.blue_present = False


            if (self.rect.x//20, self.rect.y//20) in island3.coordi and ((self.rect.x-20)//20, self.rect.y//20) not in island3.coordi:
                if island3.red_wall or island3.blue_wall:
                    self.rect.x += 20
                else:
                    if self.type == "red" and not self.friend_present(island3, "red"):
                        island3.red_present = False
                    elif self.type == "blue" and not self.friend_present(island3, "red"):
                        island3.blue_present = False

            self.rect.x -= 20
            if (self.rect.x//20, self.rect.y//20) in self.__myTeam._Team__myGame._Game__PositionToPirate:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            else:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)] = {}
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            if self.type == 'red': 
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 1
            else:
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 2

    def move_right(self, island1, island2, island3):
        if self.rect.x < (self.__myTeam._Team__myGame._Game__dim[0]-1)*20:
            #self.__myBase.pirate_map[self.rect.x//20][self.rect.y//20] = 0
            try: 
                del self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self]
            except:
                return
            
            if (self.rect.x//20, self.rect.y//20) not in island1.coordi and ((self.rect.x+20)//20, self.rect.y//20) in island1.coordi:
                if island1.red_wall or island1.blue_wall:
                    self.rect.x -= 20
                else:
                    if self.type == 'red':
                        island1.red_present = True
                        # print(island1.red_present)
                    else:
                        island1.blue_present = True

            if (self.rect.x//20, self.rect.y//20) not in island2.coordi and ((self.rect.x+20)//20, self.rect.y//20) in island2.coordi:
                if island2.red_wall or island2.blue_wall:
                    self.rect.x -= 20
                else:
                    if self.type == 'red':
                        island2.red_present = True
                        # print(island2.red_present)
                    else:
                        island2.blue_present = True

            if (self.rect.x//20, self.rect.y//20) not in island3.coordi and ((self.rect.x+20)//20, self.rect.y//20) in island3.coordi:
                if island3.red_wall or island3.blue_wall:
                    self.rect.x -= 20
                else:
                    if self.type == 'red':
                        island3.red_present = True
                        # print(island3.red_present)
                    else:
                        island3.blue_present = True

            if (self.rect.x//20, self.rect.y//20) in island1.coordi and ((self.rect.x+20)//20, self.rect.y//20) not in island1.coordi:
                if island1.red_wall or island1.blue_wall:
                    self.rect.x -= 20
                else:
                    if self.type == "red" and not self.friend_present(island1, "red"):
                        island1.red_present = False
                    elif self.type == "blue" and not self.friend_present(island1, "blue"):
                        island1.blue_present = False

            if (self.rect.x//20, self.rect.y//20) in island2.coordi and ((self.rect.x+20)//20, self.rect.y//20) not in island2.coordi:
                if island2.red_wall or island2.blue_wall:
                    self.rect.x -= 20
                else:
                    if self.type == "red" and not self.friend_present(island2, "red"):
                        island2.red_present = False
                    elif self.type == "blue" and not self.friend_present(island2, "blue"):
                        island2.blue_present = False

            if (self.rect.x//20, self.rect.y//20) in island3.coordi and ((self.rect.x+20)//20, self.rect.y//20) not in island3.coordi:
                if island3.red_wall or island3.blue_wall:
                    self.rect.x -= 20
                else:
                    if self.type == "red" and not self.friend_present(island3, "red"):
                        island3.red_present = False
                    elif self.type == "blue" and not self.friend_present(island3, "red"):
                        island3.blue_present = False

            self.rect.x += 20
            if (self.rect.x//20, self.rect.y//20) in self.__myTeam._Team__myGame._Game__PositionToPirate:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            else:
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)] = {}
                self.__myTeam._Team__myGame._Game__PositionToPirate[(self.rect.x//20, self.rect.y//20)][self] = True
            if self.type == 'red': 
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 1
            else:
                self.__myTeam._Team__pirate_map[self.rect.x//20][self.rect.y//20] = 2

    def investigate_up(self):
        if self.rect.y == 0:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20-1] == 1:
        # elif self.__myBase._Base__Pirate_map[self.rect.y//20  - 1][self.rect.x//20] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20-1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20-1] == 3:
            # if self.type == "red":
            return "island1"

        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20-1] == 4:  
            return "island2"
            
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20-1] == 5:  
            # if self.type == "red":
            return "island3"
        else:
            return "blank"
        
    def investigate_down(self):
        if self.rect.y == (self.__myTeam._Team__myGame._Game__dim[1]-1)*20:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20+1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20+1] == 3:
            return "island1"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20+1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20+1] == 4:
            return "island2"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20][self.rect.y//20+1] == 5:
            return "island3"
        else:
            return "blank"
        
    def investigate_left(self):
        if self.rect.x == 0:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20-1][self.rect.y//20] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20-1][self.rect.y//20] == 3:
            return "island1"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20-1][self.rect.y//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20-1][self.rect.y//20] == 4:
            return "island2"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20-1][self.rect.y//20] == 5:
            return "island3"
        else:
            return "blank"
        
    def investigate_right(self):
        if self.rect.x == (self.__myTeam._Team__myGame._Game__dim[0]-1)*20:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20+1][self.rect.y//20] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20+1][self.rect.y//20] == 3:
            return "island1"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20+1][self.rect.y//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20+1][self.rect.y//20] == 4:
            return "island2"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20+1][self.rect.y//20] == 5:
            return "island3"
        else:
            return "blank"
        
    def investigate_ne(self):
        if self.rect.x == (self.__myTeam._Team__myGame._Game__dim[0]-1)*20 or self.rect.y == 0:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 - 1] == 3:
            return "island1"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 - 1] == 4:
            return "island2"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 - 1] == 5:
            return "island3"
        else:
            return "blank"
        
    def investigate_nw(self):
        if self.rect.x == 0 or self.rect.y == 0:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 - 1] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 - 1] == 3:
            return "island1"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 - 1] == 4:
            return "island2"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 - 1] == 5:
            return "island3"
        else:
            return "blank"
        
    def investigate_se(self):
        if self.rect.x == (self.__myTeam._Team__myGame._Game__dim[0]-1)*20 or self.rect.y == (self.__myTeam._Team__myGame._Game__dim[1]-1)*20:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 + 1] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 + 1] == 3:
            return "island1"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 + 1] == 4:
            return "island2"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 + 1][self.rect.y//20 + 1] == 5:
            return "island3"
        else:
            return "blank"
        
    def investigate_sw(self):
        if self.rect.x == 0 or self.rect.y == (self.__myTeam._Team__myGame._Game__dim[1]-1)*20:
            return "wall"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 + 1] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 + 1] == 3:
            return "island1"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 + 1] == 4:
            return "island2"
        elif self.__myTeam._Team__myGame._Game__Pirates[self.rect.x//20 - 1][self.rect.y//20 + 1] == 5:
            return "island3"
        else:
            return "blank"        

    def setSignal(self, sig):
        str = 'wncc'
        if type(sig)!=type(str) or len(sig) > 20:
            return
        self.__Signal = sig
    
    def GetInitialSignal(self):
        return self.__initialSignal

    def GetYourSignal(self):
        return self.__signal
    
    def GetCurrentTeamSignal(self):
        return self.__myTeam._Team__signal
    
    def GetTotalRum(self):
        return self.__myTeam._Team__rum
    
    def GetTotalGunpowder(self):
        return self.__myTeam._Team__gunpowder
    
    def GetTotalWood(self):
        return self.__myTeam._Team__wood    
    
    def GetPosition(self):
        return (self.rect.x//20, self.rect.y//20)
    
    def GetDimensionX(self):
        return self.__myBase._Base__myGame._Game__dim[0]

    def GetDimensionY(self):
        return self.__myBase._Base__myGame._Game__dim[1]
    
    def setSignal(self, sig):
        str = 'wncc'
        if type(sig)!=type(str) or len(sig) > 20:
            return
        self.__Signal = sig

    def GetInitialSignal(self):
        return self.__initialSignal

    def GetYourSignal(self):
        return self.__signal
    
    def GetCurrentTeamSignal(self):
        return self.__myTeam._Team__signal
    
    def SetTeamSignal(self, signal):
        return self.__myTeam.SetYourSignal(signal)

    def trackPlayers(self):
        return self.__myTeam.trackPlayers()

    


