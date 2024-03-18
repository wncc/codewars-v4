import random

from .pirate import Pirate


class Team:
    def __init__(self, screen, type, __pirate_list, __pirate_map, game, base):
        self.__pirate_list = __pirate_list
        self.__pirate_map = __pirate_map
        self.screen = screen
        self.__myGame = game
        self.__type = type
        self.__rum = 400
        self.__gunpowder = 500
        self.__wood = 150
        self.__flag1 = None
        self.__flag2 = None
        self.__flag3 = None
        self.__base = base
        self.status1 = 0
        self.status2 = 0
        self.status3 = 0
        self.__curr_frame = -1
        self.__signal = ""
        self.__created_count = 0

        for _ in range(8):
            x = random.randint(0, 39)
            y = random.randint(0, 39)
            self.create_Pirate(base[0] * 20, base[1] * 20)

    def create_Pirate(self, x, y):
        if self.__rum >= 50:
            self.__rum -= 50
            self.__created_count += 1
            pirate_i = Pirate(self.screen, x, y, self.__type, self, str(self.__created_count))
            self.__pirate_list.add(pirate_i)

            if (x // 20, y // 20) in self.__myGame._Game__PositionToPirate:
                self.__myGame._Game__PositionToPirate[(x // 20, y // 20)][
                    pirate_i
                ] = True
            else:
                self.__myGame._Game__PositionToPirate[(x // 20, y // 20)] = {}
                self.__myGame._Game__PositionToPirate[(x // 20, y // 20)][
                    pirate_i
                ] = True

    def __buildWalls(self, island1, island2, island3, island_no):
        wood = self.__wood
        if wood < 50:
            return

        if island_no == 1:
            if (
                self.__type == "red"
                and island1.red_present
                and not island1.blue_present
                and not island1.red_wall
                and not island1.blue_wall
                and island1.rebuild_frame + 35 < self.__curr_frame
            ):
                island1.red_wall = True
                if island1.red_wall_frame == -1:
                    island1.red_wall_frame = self.__curr_frame
                self.__wood -= 50

                return
            elif (
                self.__type == "blue"
                and island1.blue_present
                and not island1.red_present
                and not island1.red_wall
                and not island1.blue_wall
                and island1.rebuild_frame + 35 < self.__curr_frame
            ):
                island1.blue_wall = True
                if island1.blue_wall_frame == -1:
                    island1.blue_wall_frame = self.__curr_frame
                self.__wood -= 50
                return

        elif island_no == 2:
            if (
                self.__type == "red"
                and island2.red_present
                and not island2.blue_present
                and not island2.red_wall
                and not island2.blue_wall
                and island2.rebuild_frame + 35 < self.__curr_frame
            ):
                island2.red_wall = True
                if island2.red_wall_frame == -1:
                    island2.red_wall_frame = self.__curr_frame
                self.__wood -= 50
                return
            elif (
                self.__type == "blue"
                and island2.blue_present
                and not island2.red_present
                and not island2.red_wall
                and not island2.blue_wall
                and island2.rebuild_frame + 35 < self.__curr_frame
            ):
                island2.blue_wall = True
                if island2.blue_wall_frame == -1:
                    island2.blue_wall_frame = self.__curr_frame
                self.__wood -= 50
                return
        # elif self.__flag3 and island_no == 3:
        elif island_no == 3:
            if (
                self.__type == "red"
                and island3.red_present
                and not island3.blue_present
                and not island3.red_wall
                and not island3.blue_wall
                and island3.rebuild_frame + 35 < self.__curr_frame
            ):
                island3.red_wall = True
                if island3.red_wall_frame == -1:
                    island3.red_wall_frame = self.__curr_frame
                self.__wood -= 50
                # # print(island3.red_wall)
                return
            elif (
                self.__type == "blue"
                and island3.blue_present
                and not island3.red_present
                and not island3.red_wall
                and not island3.blue_wall
                and island3.rebuild_frame + 35 < self.__curr_frame
            ):
                island3.blue_wall = True
                if island3.blue_wall_frame == -1:
                    island3.blue_wall_frame = self.__curr_frame
                self.__wood -= 50
                return
            
    def addResource(self, type, x, y, frac):
        x = x * 20
        y = y * 20

        if type == -1:
            self.__rum += 75 * frac

            for i in self.__myGame._Game__rum:
                if i.rect == (x, y, 20, 20):

                    self.__myGame._Game__rum.remove(i)
                    break
        elif type == -2:
            self.__gunpowder += 50 * frac
            for i in self.__myGame._Game__gunpowder:
                if i.rect == (x, y, 20, 20):
                    self.__myGame._Game__gunpowder.remove(i)
                    break
        elif type == -3:
            self.__wood += 25 * frac
            for i in self.__myGame._Game__wood:
                if i.rect == (x, y, 20, 20):
                    self.__myGame._Game__wood.remove(i)
                    break

    def respawn(self):
        for i in range(int(self.__rum // 50)):
            x, y = self.__base
            self.create_Pirate(x * 20, y * 20)

    # player functions start here

    def getTeamSignal(self):
        return self.__signal

    def setTeamSignal(self, s):
        str = "wncc"
        if type(s) != type(str) or len(s) > 100:
            return
        self.__signal = s

    def getListOfSignals(self):
        res = []
        for x in self.__pirate_list:
            res.append(x._Pirate__signal)
        return res
    
    def trackPlayers(self):
        if self.__type == "red":
            return self.__myGame.island_status_red
        else:
            return self.__myGame.island_status_blue
        
    def getTotalPirates(self):
        return len(self.__pirate_list)

    def getTotalRum(self):
        return self.__rum

    def getTotalGunpowder(self):
        return self.__gunpowder

    def getTotalWood(self):
        return self.__wood

    def getDeployPoint(self):
        return (self.__base[0], self.__base[1])

    def getDimensionX(self):
        return self.__myGame._Game__dim[0]

    def getDimensionY(self):
        return self.__myGame._Game__dim[1]        
            
    def buildWalls(self, island_no):
        return self.__buildWalls(self.__myGame._Game__island1, self.__myGame._Game__island2, self.__myGame._Game__island3, island_no)

    def getCurrentFrame(self):
        return self.__myGame._Game__frame