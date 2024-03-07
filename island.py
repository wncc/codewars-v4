import pygame
from pirate import Pirate
from pygame.sprite import Sprite
from pygame.sprite import Group
from collectible import Collectible
from collectible import Wall

class Island(Sprite):
    def __init__(self, screen, number, game, flag, pirate_map):
        super().__init__()
        self.screen = screen
        self.coordi = []
        self.__flag = flag
        self.__red_found = False
        self.__blue_found = False
        self.__pirate_map = pirate_map
        self.__status = 0
        self.red_wall = False
        self.blue_wall = False
        self.red_present = False
        self.blue_present = False
        self.start_capture = -1
        self.capturing_team = None
        self.red_wall_frame = -1
        self.blue_wall_frame = -1
        self.rebuild_frame = -1
        self.__myTeamGame = game
        self.walls = Group()
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.coordi.append((self.__flag[0] + i, self.__flag[1] + j))
                self.__pirate_map[self.__flag[0] + j][self.__flag[1] + i] = number + 2
                self.__myTeamGame._Game__Pirates[self.__flag[0] + j][self.__flag[1] + i] = number + 2
                # self.island2.append((self.flag2[0] + i, self.flag2[1] + j))
                # self.island3.append((self.flag3[0] + i, self.flag3[1] + j))
        for coo in self.coordi:
            if coo != (self.__flag[0], self.__flag[1]):
                self.walls.add(Wall(screen, coo[0]*20, coo[1]*20))
        # this tells if being captured / is captured by red or blue
        # 0 - not captured
        # 1 - captured by red
        # -1 - captured by blue

    def check(self, frame):      
        # red enters and blue is not present  
        if self.red_present and not self.blue_present and self.start_capture == -1 and self.__status != 1:
            self.start_capture = frame
            self.capturing_team = 1
        # blue enters and red is not present
        elif self.blue_present and not self.red_present and self.start_capture == -1 and self.__status != -1:
            self.start_capture = frame
            self.capturing_team = 2
        # both are present
        elif self.red_present and self.blue_present:
            self.start_capture = -1
            self.capturing_team = None
        # no capturing team
        elif not self.red_present and not self.blue_present:
            self.start_capture = -1
            self.capturing_team = None
        # # blue was capturing, left and not red is capturing
        # elif self.red_present and not self.blue_present and self.start_capture != -1 and self.capturing_team == 2:
        #     self.start_capture = -1
        #     if self.__status != 1:
        #         self.capturing_team = 1
        #     else:
        #         self.capturing_team = None
        # # red was capturing, left and not blue is capturing
        # elif self.blue_present and not self.red_present and self.start_capture != -1 and self.capturing_team == 1:
        #     self.start_capture = -1
        #     if self.__status != -1:
        #         self.capturing_team = 2
        #     else:
        #         self.capturing_team = None
        # red captured
        if self.red_present and not self.blue_present and self.start_capture != -1 and self.capturing_team == 1:
            if frame - self.start_capture >= 150:
                self.__status = 1
                self.start_capture = -1
                self.capturing_team = None
        # blue captured
        elif self.blue_present and not self.red_present and self.start_capture != -1 and self.capturing_team == 2:
            if frame - self.start_capture >= 150:
                self.__status = -1
                self.start_capture = -1
                self.capturing_team = None
        return self.__status
    
    def checkwall(self, frame):
        if self.red_wall and not self.blue_wall:
            # if self.red_wall_frame == -1:
            #     self.red_wall_frame = frame
            if frame - self.red_wall_frame >= 50:
                self.red_wall = False
                self.rebuild_frame = frame
                self.red_wall_frame = -1
        elif self.blue_wall and not self.red_wall:
            if frame - self.blue_wall_frame >= 50:
                self.blue_wall = False
                self.rebuild_frame = frame
                self.blue_wall_frame = -1

        if self.red_wall or self.blue_wall:
        # print("HI")
            # print(self.walls)
            self.walls.draw(self.screen)