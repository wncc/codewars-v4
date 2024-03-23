from pygame.sprite import Group, Sprite

from .collectible import Wall

FRAMES_TO_CAPTURE = 150


class Island(Sprite):
    def __init__(self, screen, number, game, flag, pirate_map):
        super().__init__()
        self.screen = screen
        self.coordi = []
        self.__flag = flag
        self.__progress = -1
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
        self.rebuild_frame = -100 # Otherwise, the check in teams would think this was rebuilt just 1 game before game start
        self.__myTeamGame = game
        self.walls = Group()
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.coordi.append((self.__flag[0] + i, self.__flag[1] + j))
                self.__pirate_map[self.__flag[0] + j][self.__flag[1] + i] = number << 2
                self.__myTeamGame._Game__Pirates[self.__flag[0] + j][
                    self.__flag[1] + i
                ] |= number << 2
                
        for coo in self.coordi:
            if coo != (self.__flag[0], self.__flag[1]):
                self.walls.add(Wall(screen, coo[0] * 20, coo[1] * 20))
        # this tells if being captured / is captured by red or blue
        # 0 - not captured
        # 1 - captured by red
        # -1 - captured by blue

    def progress(self):
        if self.start_capture == -1 or self.capturing_team == None:
            return None
        return f"{self.__progress}/{FRAMES_TO_CAPTURE}"

    def __reset(self):
        self.start_capture = -1
        self.__progress = -1
        self.capturing_team = None

    def check(self, frame):
        # both are present
        if self.red_present and self.blue_present:
            self.__reset()
        # no capturing team
        elif not self.red_present and not self.blue_present:
            self.__reset()

        # red enters and blue is not present
        elif self.red_present and not self.blue_present and self.__status != 1:
            if self.start_capture == -1:
                self.start_capture = frame
                self.capturing_team = 1

            self.__progress = frame - self.start_capture
            if self.__progress >= FRAMES_TO_CAPTURE:
                self.__status = 1
                self.__reset()
        # blue enters and red is not present
        elif self.blue_present and not self.red_present and self.__status != -1:
            if self.start_capture == -1:
                self.start_capture = frame
                self.capturing_team = 2

            self.__progress = frame - self.start_capture
            if self.__progress >= FRAMES_TO_CAPTURE:
                self.__status = -1
                self.__reset()

        return self.__status

    def checkwall(self, frame):
        if self.red_wall and not self.blue_wall:
            if frame - self.red_wall_frame >= 50:
                self.red_wall = False
                self.rebuild_frame = frame
                self.red_wall_frame = -1
        elif self.blue_wall and not self.red_wall:
            if frame - self.blue_wall_frame >= 50:
                self.blue_wall = False
                self.rebuild_frame = frame
                self.blue_wall_frame = -1


    def drawWalls(self):
        if self.red_wall or self.blue_wall:
            self.walls.draw(self.screen)
