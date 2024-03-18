import pygame
from pygame.sprite import Sprite


class Pirate(Sprite):
    def __init__(self, screen, x, y, type, team, signal):
        super().__init__()
        self.screen = screen
        self.type = type
        self.__myTeam = team
        if self.type == "red":
            self.image = pygame.image.load("images/pirate.png")
        else:
            self.image = pygame.image.load("images/pirateblue.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__initialSignal = signal
        self.__signal = ""

    def friend_present(self, island, type3):
        for pirate in self.__myTeam._Team__pirate_list:
            if (
                (pirate.rect.x // 20, pirate.rect.y // 20) in island.coordi
                and pirate.type == self.type
                and pirate != self
            ):
                return True
        return False
    
    def __on_death(self, islands):
        for island in islands:
            if (self.rect.x // 20, self.rect.y // 20) in island.coordi:
                if self.type == "red" and not self.friend_present(island, "red"):
                    island.red_present = False
                elif self.type == "blue" and not self.friend_present(
                    island, "blue"
                ):
                    island.blue_present = False

    def __check_move(self, island, x0, y0, x1, y1):
        if (x0 // 20, y0 // 20) not in island.coordi and ( x1 // 20, y1 // 20) in island.coordi:
            if island.red_wall or island.blue_wall:
                return True
            else:
                if self.type == "red":
                    island.red_present = True
                else:
                    island.blue_present = True

        elif (x0 // 20, y0 // 20) in island.coordi and ( x1 // 20, y1 // 20) not in island.coordi:
            if island.red_wall or island.blue_wall:
                return True
            else:
                if self.type == "red" and not self.friend_present(island, "red"):
                    island.red_present = False
                elif self.type == "blue" and not self.friend_present(
                    island, "blue"
                ):
                    island.blue_present = False

    def __place_after_move(self):
        if (
            self.rect.x // 20,
            self.rect.y // 20,
        ) in self.__myTeam._Team__myGame._Game__PositionToPirate:
            self.__myTeam._Team__myGame._Game__PositionToPirate[
                (self.rect.x // 20, self.rect.y // 20)
            ][self] = True
        else:
            self.__myTeam._Team__myGame._Game__PositionToPirate[
                (self.rect.x // 20, self.rect.y // 20)
            ] = {}
            self.__myTeam._Team__myGame._Game__PositionToPirate[
                (self.rect.x // 20, self.rect.y // 20)
            ][self] = True
        # if self.type == "red":
        #     self.__myTeam._Team__pirate_map[self.rect.x // 20][
        #         self.rect.y // 20
        #     ] |= 1
        # else:
        #     self.__myTeam._Team__pirate_map[self.rect.x // 20][
        #         self.rect.y // 20
        #     ] |= 2

    __wall_case = ("wall", "blank")

    def __investigate(self,x,y):

        who = 'blank'
        where = 'blank'
        match(self.__myTeam._Team__myGame._Game__Pirates[x][y] & 3):
            case 1:
                if self.type == "red":
                    who = "friend"
                else:
                    who = "enemy"
            case 2:
                if self.type == "red":
                    who = "enemy"
                else:
                    who = "friend"
            case 3:
                who = "both"
            
        match(self.__myTeam._Team__myGame._Game__Pirates[x][y] >> 2):
            case 1:
                where = "island1"
            case 2:
                where = "island2"
            case 3:
                where = "island3"

        return (where, who)

    def move_up(self, island1, island2, island3):
        if self.rect.y > 0:
            try:
                del self.__myTeam._Team__myGame._Game__PositionToPirate[
                    (self.rect.x // 20, self.rect.y // 20)
                ][self]
            except:
                return

            for island in (island1,island2,island3):
                if self.__check_move(island, self.rect.x, self.rect.y, self.rect.x, self.rect.y - 20):
                    self.rect.y += 20
                    break

            self.rect.y -= 20
            self.__place_after_move()

    def move_down(self, island1, island2, island3):
        if self.rect.y < (self.__myTeam._Team__myGame._Game__dim[1] - 1) * 20:
            try:
                del self.__myTeam._Team__myGame._Game__PositionToPirate[
                    (self.rect.x // 20, self.rect.y // 20)
                ][self]
            except:
                return
            
            for island in (island1,island2,island3):
                if self.__check_move(island, self.rect.x, self.rect.y, self.rect.x, self.rect.y + 20):
                    self.rect.y -= 20
                    break

            self.rect.y += 20
            self.__place_after_move()

    def move_left(self, island1, island2, island3):
        if self.rect.x > 0:
            try:
                del self.__myTeam._Team__myGame._Game__PositionToPirate[
                    (self.rect.x // 20, self.rect.y // 20)
                ][self]
            except:
                return

            for island in (island1,island2,island3):
                if self.__check_move(island, self.rect.x, self.rect.y, self.rect.x - 20, self.rect.y):
                    self.rect.x += 20
                    break

            self.rect.x -= 20
            self.__place_after_move()

    def move_right(self, island1, island2, island3):
        if self.rect.x < (self.__myTeam._Team__myGame._Game__dim[0] - 1) * 20:
            try:
                del self.__myTeam._Team__myGame._Game__PositionToPirate[
                    (self.rect.x // 20, self.rect.y // 20)
                ][self]
            except:
                return

            for island in (island1,island2,island3):
                if self.__check_move(island, self.rect.x, self.rect.y, self.rect.x + 20, self.rect.y):
                    self.rect.x -= 20
                    break

            self.rect.x += 20
            self.__place_after_move()

    # player functions start here
            
    def investigate_current(self):
        return self.__investigate(self.rect.x // 20, self.rect.y // 20)

    def investigate_up(self):
        if self.rect.y == 0:
            return self.__wall_case
        return self.__investigate(self.rect.x // 20, self.rect.y // 20 - 1)

    def investigate_down(self):
        if self.rect.y == (self.__myTeam._Team__myGame._Game__dim[1] - 1) * 20:
            return self.__wall_case
        return self.__investigate(self.rect.x // 20, self.rect.y // 20 + 1)     

    def investigate_left(self):
        if self.rect.x == 0:
            return self.__wall_case
        return self.__investigate(self.rect.x // 20 - 1, self.rect.y // 20)

    def investigate_right(self):
        if self.rect.x == (self.__myTeam._Team__myGame._Game__dim[0] - 1) * 20:
            return self.__wall_case
        return self.__investigate(self.rect.x // 20 + 1, self.rect.y // 20)

    def investigate_ne(self):
        if (
            self.rect.x == (self.__myTeam._Team__myGame._Game__dim[0] - 1) * 20
            or self.rect.y == 0
        ):
            return self.__wall_case
        return self.__investigate(self.rect.x // 20 + 1, self.rect.y // 20 - 1)

    def investigate_nw(self):
        if self.rect.x == 0 or self.rect.y == 0:
            return self.__wall_case
        return self.__investigate(self.rect.x // 20 - 1, self.rect.y // 20 - 1)

    def investigate_se(self):
        if (
            self.rect.x == (self.__myTeam._Team__myGame._Game__dim[0] - 1) * 20
            or self.rect.y == (self.__myTeam._Team__myGame._Game__dim[1] - 1) * 20
        ):
            return self.__wall_case
        return self.__investigate(self.rect.x // 20 + 1, self.rect.y // 20 + 1)

    def investigate_sw(self):
        if (
            self.rect.x == 0
            or self.rect.y == (self.__myTeam._Team__myGame._Game__dim[1] - 1) * 20
        ):
            return self.__wall_case
        return self.__investigate(self.rect.x // 20 - 1, self.rect.y // 20 + 1)

    def getTotalRum(self):
        return self.__myTeam._Team__rum

    def getTotalGunpowder(self):
        return self.__myTeam._Team__gunpowder

    def getTotalWood(self):
        return self.__myTeam._Team__wood

    def getPosition(self):
        return (self.rect.x // 20, self.rect.y // 20)
    
    def getDeployPoint(self):
        return self.__myTeam.getDeployPoint()

    def getDimensionX(self):
        return self.__myTeam._Team__myGame._Game__dim[0]

    def getDimensionY(self):
        return self.__myTeam._Team__myGame._Game__dim[0]
    
    def getID(self):
        return self.__initialSignal

    def getSignal(self):
        return self.__signal
    
    def setSignal(self, sig):
        str = "wncc"
        if type(sig) != type(str) or len(sig) > 100:
            return
        self.__signal = sig

    def getTeamSignal(self):
        return self.__myTeam._Team__signal

    def setTeamSignal(self, signal):
        return self.__myTeam.setTeamSignal(signal)
    
    def trackPlayers(self):
        return self.__myTeam.trackPlayers()
    
    def getCurrentFrame(self):
        return self.__myTeam.getCurrentFrame()