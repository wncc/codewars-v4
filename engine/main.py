import random
import sys
from random import random as rnd

import numpy as np
import pygame
from pygame.sprite import Group

from .collectible import Collectible, Sea
from .island import Island
from .team import Team
from .utils import *
import random
import tkinter
from tkinter import messagebox
import traceback

status_to_sea = [SEA_DARKBLUE, SEA_BLUE, SEA_RED]
status_to_color = [BLUE, LIGHT_GRAY, RED]
status_to_team = ["Blue", "Neutral", "Red"]

root = tkinter.Tk()
root.withdraw()

class Game:
    def __init__(self, dim, red_team, blue_team):
        pygame.init()
        self.fps_controller = pygame.time.Clock()
        self.__sea = Group()
        self.__dim = dim
        self.__frame = 0
        self.rate = 20
        self.explosion = pygame.image.load("images/explode.png")
        self.purple_pirate = pygame.image.load("images/piratepurple.png")
        self.screen = pygame.display.set_mode(
            (self.__dim[0] * 20 + 400, self.__dim[1] * 20)
        )

        [self.flag1, self.flag2, self.flag3, base_red, base_blue] = self.getPositions()

        self.__rscript = red_team
        self.__bscript = blue_team
        self.__rum = Group()
        self.__gunpowder = Group()
        self.__wood = Group()
        self.__red_pirates = Group()
        self.__blue_pirates = Group()
        self.__Pirates = np.zeros((self.__dim[0], self.__dim[1]), dtype=int)
        # 0 in self.Pirates means no Pirates
        # 1 means one Pirate of red team
        # 2 means one Pirate of blue team
        # 3 means __island1
        # 4 means __island2
        # 5 means __island3
        self.status1 = 0
        self.status2 = 0
        self.status3 = 0

        self.island_status_blue = ["", "", "", "", "", ""]
        self.island_status_red = ["", "", "", "", "", ""]
        # first 3 strings of the array give the status of the islands of the repective team
        # last 3 strings give the status of the islands of the other team
        # r1, r2, r3, b1, b2, b3

        self.__PositionToPirate = {}
        self.__red_team = Team(
            self.screen, "red", self.__red_pirates, self.__Pirates, self, base_red
        )
        self.__blue_team = Team(
            self.screen, "blue", self.__blue_pirates, self.__Pirates, self, base_blue
        )

        for pirate in self.__red_pirates:
            self.__Pirates[pirate.rect.x // 20][pirate.rect.y // 20] |= 1
        for pirate in self.__blue_pirates:
            self.__Pirates[pirate.rect.x // 20][pirate.rect.y // 20] |= 2

        self.__island1 = Island(self.screen, 1, self, self.flag1, self.__Pirates)
        self.__island2 = Island(self.screen, 2, self, self.flag2, self.__Pirates)
        self.__island3 = Island(self.screen, 3, self, self.flag3, self.__Pirates)
        self.__collectibles = self.create_map()

        self.__PositionToPirate[self.flag1] = {self.__island1: True}
        self.__PositionToPirate[self.flag2] = {self.__island2: True}
        self.__PositionToPirate[self.flag3] = {self.__island3: True}

        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Sea(self.screen, i * 20, j * 20))
            self.__sea.add(Z)

    @property
    def rname(self):
        return self.__rscript.name

    @property
    def bname(self):
        return self.__bscript.name

    def getPositions(self):
        excluded = random.randint(0, 3)

        if excluded == 0 or excluded == 3:
            base_red = (self.__dim[0] - 1, 0)
            base_blue = (0, self.__dim[1] - 1)
        else:
            base_red = (0, 0)
            base_blue = (self.__dim[0] - 1, self.__dim[1] - 1)

        l = []
        for i in range(4):
            if i == excluded:
                continue
            if i == 0:
                x = random.randint(4, self.__dim[0] // 2 - 4)
                y = random.randint(4, self.__dim[1] // 2 - 4)
                l.append((x, y))
            elif i == 1:
                x = random.randint(self.__dim[0] // 2 + 4, self.__dim[0] - 4)
                y = random.randint(4, self.__dim[1] // 2 - 4)
                l.append((x, y))
            elif i == 2:
                x = random.randint(4, self.__dim[0] // 2 - 4)
                y = random.randint(self.__dim[1] // 2 + 4, self.__dim[1] - 4)
                l.append((x, y))
            else:
                x = random.randint(self.__dim[0] // 2 + 4, self.__dim[0] - 4)
                y = random.randint(self.__dim[1] // 2 + 4, self.__dim[1] - 4)
                l.append((x, y))
        return l + [base_red, base_blue]

    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = np.zeros((self.__dim))

        size = self.__dim[0] * self.__dim[1]
        frac = size / 16

        while len(self.__rum) < frac:
            x = random.randint(0, self.__dim[0] - 1)
            y = random.randint(0, self.__dim[1] - 1)
            if (
                im[x][y] == 0
                and (x, y) not in self.__island1.coordi
                and (x, y) not in self.__island2.coordi
                and (x, y) not in self.__island3.coordi
            ):
                self.__rum.add(Collectible(self.screen, x, y, -1))
                im[x][y] = -1

        while len(self.__gunpowder) < frac:
            x = random.randint(0, self.__dim[0] - 1)
            y = random.randint(0, self.__dim[1] - 1)
            if (
                im[x][y] == 0
                and (x, y) not in self.__island1.coordi
                and (x, y) not in self.__island2.coordi
                and (x, y) not in self.__island3.coordi
            ):
                self.__gunpowder.add(Collectible(self.screen, x, y, -2))
                im[x][y] = -2

        while len(self.__wood) < frac:
            x = random.randint(0, self.__dim[0] - 1)
            y = random.randint(0, self.__dim[1] - 1)
            if (
                im[x][y] == 0
                and (x, y) not in self.__island1.coordi
                and (x, y) not in self.__island2.coordi
                and (x, y) not in self.__island3.coordi
            ):
                self.__wood.add(Collectible(self.screen, x, y, -3))
                im[x][y] = -3

        return im

    def run_game(self):
        iter = 0
        while True:
            iter += 1
            if iter <= 3000:
                self.__frame = iter
                self.screen.fill(DARK_GREY)
                moves = {}

                status1 = self.__island1.check(iter)
                status2 = self.__island2.check(iter)
                status3 = self.__island3.check(iter)

                if status1 == 1:
                    self.island_status_red[0] = "myCaptured"
                    self.island_status_blue[3] = "oppCaptured"
                    self.island_status_red[3] = ""
                    self.island_status_blue[0] = ""
                elif status1 == -1:
                    self.island_status_red[3] = "oppCaptured"
                    self.island_status_blue[0] = "myCaptured"
                    self.island_status_red[0] = ""
                    self.island_status_blue[3] = ""
                else:
                    self.island_status_red[3] = ""
                    self.island_status_blue[0] = ""
                    self.island_status_red[0] = ""
                    self.island_status_blue[3] = ""
                if status2 == 1:
                    self.island_status_red[1] = "myCaptured"
                    self.island_status_blue[4] = "oppCaptured"
                    self.island_status_red[4] = ""
                    self.island_status_blue[1] = ""
                elif status2 == -1:
                    self.island_status_red[4] = "oppCaptured"
                    self.island_status_blue[1] = "myCaptured"
                    self.island_status_red[1] = ""
                    self.island_status_blue[4] = ""
                else:
                    self.island_status_red[4] = ""
                    self.island_status_blue[1] = ""
                    self.island_status_red[1] = ""
                    self.island_status_blue[4] = ""
                if status3 == 1:
                    self.island_status_red[2] = "myCaptured"
                    self.island_status_blue[5] = "oppCaptured"
                    self.island_status_red[5] = ""
                    self.island_status_blue[2] = ""
                elif status3 == -1:
                    self.island_status_red[5] = "oppCaptured"
                    self.island_status_blue[2] = "myCaptured"
                    self.island_status_red[2] = ""
                    self.island_status_blue[5] = ""
                else:
                    self.island_status_red[5] = ""
                    self.island_status_blue[2] = ""
                    self.island_status_red[2] = ""
                    self.island_status_blue[5] = ""

                if self.__island1.capturing_team == 1:  # red
                    self.island_status_red[0] = "myCapturing"
                    self.island_status_blue[3] = "oppCapturing"
                elif self.__island1.capturing_team == 2:  # blue

                    self.island_status_red[3] = "oppCapturing"
                    self.island_status_blue[0] = "myCapturing"

                if self.__island2.capturing_team == 1:  # red

                    self.island_status_red[1] = "myCapturing"
                    self.island_status_blue[4] = "oppCapturing"
                elif self.__island2.capturing_team == 2:  # blue
                    self.island_status_red[4] = "oppCapturing"
                    self.island_status_blue[1] = "myCapturing"

                if self.__island3.capturing_team == 1:  # red
                    self.island_status_red[2] = "myCapturing"
                    self.island_status_blue[5] = "oppCapturing"

                elif self.__island3.capturing_team == 2:  # blue
                    self.island_status_red[5] = "oppCapturing"
                    self.island_status_blue[2] = "myCapturing"

                self.__red_team.status1 = status1
                self.__red_team.status2 = status2
                self.__red_team.status3 = status3

                self.status1 = status1
                self.status2 = status2
                self.status3 = status3

                self.__blue_team.status1 = status1 * -1
                self.__blue_team.status2 = status2 * -1
                self.__blue_team.status3 = status3 * -1

                self.__red_team._Team__curr_frame = iter
                self.__blue_team._Team__curr_frame = iter

                self.__sea.draw(self.screen)

                island_img = pygame.image.load("images/flag1.png")
                island_rect = island_img.get_rect()
                island_rect.center = (self.flag1[0] * 20 + 10, self.flag1[1] * 20 + 10)
                pygame.draw.rect(
                    self.screen, status_to_sea[self.status1 + 1], island_rect
                )
                self.screen.blit(island_img, island_rect)

                island_img = pygame.image.load("images/flag2.png")
                island_rect = island_img.get_rect()
                island_rect.center = (self.flag2[0] * 20 + 10, self.flag2[1] * 20 + 10)
                pygame.draw.rect(
                    self.screen, status_to_sea[self.status2 + 1], island_rect
                )
                self.screen.blit(island_img, island_rect)

                island_img = pygame.image.load("images/flag3.png")
                island_rect = island_img.get_rect()
                island_rect.center = (self.flag3[0] * 20 + 10, self.flag3[1] * 20 + 10)
                pygame.draw.rect(
                    self.screen, status_to_sea[self.status3 + 1], island_rect
                )
                self.screen.blit(island_img, island_rect)

                self.__island1.checkwall(iter)
                self.__island2.checkwall(iter)
                self.__island3.checkwall(iter)

                try:
                    current_script_name = self.rname
                    self.__rscript.ActTeam(self.__red_team)
                    current_script_name = self.bname
                    self.__bscript.ActTeam(self.__blue_team)
                    if rnd() > 0.5:
                        current_script_name = self.rname
                        for pirate_i in self.__red_pirates:
                            n = self.__rscript.ActPirate(pirate_i)
                            moves[pirate_i] = n
                        current_script_name = self.bname
                        for pirate_i in self.__blue_pirates:
                            n = self.__bscript.ActPirate(pirate_i)
                            moves[pirate_i] = n
                    else:
                        current_script_name = self.bname
                        for pirate_i in self.__blue_pirates:
                            n = self.__bscript.ActPirate(pirate_i)
                            moves[pirate_i] = n
                        current_script_name = self.rname
                        for pirate_i in self.__red_pirates:
                            n = self.__rscript.ActPirate(pirate_i)
                            moves[pirate_i] = n
                except Exception as e:
                    with open("error_log.txt", "w") as file:
                        file.write(traceback.format_exc())

                    messagebox.showerror('Script Error', f'{current_script_name} threw an error:\n{e}\n\nPlease check the error_log.txt file for more details.')
                    exit(0)

                self.__island1.drawWalls()
                self.__island2.drawWalls()
                self.__island3.drawWalls()

                for pirate_i, n in moves.items():
                    if n == 1:
                        pirate_i.move_up(self.__island1, self.__island2, self.__island3)
                    elif n == 2:
                        pirate_i.move_right(
                            self.__island1, self.__island2, self.__island3
                        )
                    elif n == 3:
                        pirate_i.move_down(
                            self.__island1, self.__island2, self.__island3
                        )
                    elif n == 4:
                        pirate_i.move_left(
                            self.__island1, self.__island2, self.__island3
                        )

                collisions, overlaps = self.check_collisions()
                self.__rum.draw(self.screen)
                self.__gunpowder.draw(self.screen)
                self.__wood.draw(self.screen)
                self.__blue_pirates.draw(self.screen)
                self.__red_pirates.draw(self.screen)
                self.discovery()
                self.__red_team.respawn()
                self.__blue_team.respawn()
                self.updatePirateMap()
                self.buttons()
                self.update_score()
                self.collect()

                for rect in overlaps:
                    self.screen.blit(self.purple_pirate, rect)

                for rect in collisions:
                    self.screen.blit(self.explosion, rect)


                if iter % 10 == 0:
                    self.replenish()

                self.check_events()
                if self.game_over():
                    # winner window
                    break

                pygame.display.flip()
                self.fps_controller.tick(self.rate)
            else:
                self.time_up()
                break
                # winner window

    def discovery(self):
        for pirate in self.__red_pirates:
            if (
                pirate.investigate_up()[0] == "island1"
                or pirate.investigate_down()[0] == "island1"
                or pirate.investigate_left()[0] == "island1"
                or pirate.investigate_right()[0] == "island1"
                or pirate.investigate_nw()[0] == "island1"
                or pirate.investigate_ne()[0] == "island1"
                or pirate.investigate_sw()[0] == "island1"
                or pirate.investigate_se()[0] == "island1"
            ):
                pirate._Pirate__myTeam._Team__flag1 = self.flag1
            elif (
                pirate.investigate_up()[0] == "island2"
                or pirate.investigate_down()[0] == "island2"
                or pirate.investigate_left()[0] == "island2"
                or pirate.investigate_right()[0] == "island2"
                or pirate.investigate_nw()[0] == "island2"
                or pirate.investigate_ne()[0] == "island2"
                or pirate.investigate_sw()[0] == "island2"
                or pirate.investigate_se()[0] == "island2"
            ):
                pirate._Pirate__myTeam._Team__flag2 = self.flag2
            elif (
                pirate.investigate_up()[0] == "island3"
                or pirate.investigate_down()[0] == "island3"
                or pirate.investigate_left()[0] == "island3"
                or pirate.investigate_right()[0] == "island3"
                or pirate.investigate_nw()[0] == "island3"
                or pirate.investigate_ne()[0] == "island3"
                or pirate.investigate_sw()[0] == "island3"
                or pirate.investigate_se()[0] == "island3"
            ):
                pirate._Pirate__myTeam._Team__flag3 = self.flag3

        for pirate in self.__blue_pirates:
            if (
                pirate.investigate_up()[0] == "island1"
                or pirate.investigate_down()[0] == "island1"
                or pirate.investigate_left()[0] == "island1"
                or pirate.investigate_right()[0] == "island1"
                or pirate.investigate_nw()[0] == "island1"
                or pirate.investigate_ne()[0] == "island1"
                or pirate.investigate_sw()[0] == "island1"
                or pirate.investigate_se()[0] == "island1"
            ):
                pirate._Pirate__myTeam._Team__flag1 = self.flag1
            elif (
                pirate.investigate_up()[0] == "island2"
                or pirate.investigate_down()[0] == "island2"
                or pirate.investigate_left()[0] == "island2"
                or pirate.investigate_right()[0] == "island2"
                or pirate.investigate_nw()[0] == "island2"
                or pirate.investigate_ne()[0] == "island2"
                or pirate.investigate_sw()[0] == "island2"
                or pirate.investigate_se()[0] == "island2"
            ):
                pirate._Pirate__myTeam._Team__flag2 = self.flag2
            elif (
                pirate.investigate_up()[0] == "island3"
                or pirate.investigate_down()[0] == "island3"
                or pirate.investigate_left()[0] == "island3"
                or pirate.investigate_right()[0] == "island3"
                or pirate.investigate_nw()[0] == "island3"
                or pirate.investigate_ne()[0] == "island3"
                or pirate.investigate_sw()[0] == "island3"
                or pirate.investigate_se()[0] == "island3"
            ):
                pirate._Pirate__myTeam._Team__flag3 = self.flag3

    def check_collisions(self):
        removals = pygame.sprite.groupcollide(
            self.__blue_pirates, self.__red_pirates, False, False
        )
        to_kill = set()
        blast_positions = []
        both_positions = []

        for b, r_list in removals.items():
            blast_added = False
            for r in r_list:
                if r in to_kill:
                    continue

                if (
                    self.__blue_team._Team__gunpowder >= 100
                    and self.__red_team._Team__gunpowder >= 100
                ):
                    to_kill.add(r)
                    to_kill.add(b)

                    self.__red_team._Team__gunpowder -= 100
                    self.__blue_team._Team__gunpowder -= 100

                    if not blast_added:
                        blast_added = True
                        blast_positions.append(b.rect)
                    break

                elif self.__blue_team._Team__gunpowder >= 100:
                    to_kill.add(r)
                    self.__blue_team._Team__gunpowder -= 100

                    if not blast_added:
                        blast_added = True
                        blast_positions.append(b.rect)

                elif self.__red_team._Team__gunpowder >= 100:
                    to_kill.add(b)
                    self.__red_team._Team__gunpowder -= 100

                    if not blast_added:
                        blast_added = True
                        blast_positions.append(b.rect)
                    break
                else:
                    both_positions.append(b.rect)
                    break

        for a in to_kill:
            del self.__PositionToPirate[(a.rect.x // 20, a.rect.y // 20)][a]
            a._Pirate__on_death((self.__island1, self.__island2, self.__island3))
            a.kill()

        return blast_positions, both_positions

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, DARK_GREY)
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = ((self.__dim[0]) * 20 + 60, self.__dim[1] * 18 + 5)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.slow_rect)
        self.screen.blit(slow_down, ((self.__dim[0]) * 20 + 30, self.__dim[1] * 18))

        speed_up = button_font.render("Faster", True, DARK_GREY)
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = ((self.__dim[0]) * 20 + 258, self.__dim[1] * 18 + 5)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.fast_rect)
        self.screen.blit(speed_up, ((self.__dim[0]) * 20 + 230, self.__dim[1] * 18))

        # ss = button_font.render("SS", True, DARK_GREY)
        # self.ss_rect = ss.get_rect()
        # self.ss_rect.center = ((self.__dim[0]) * 20 + 258, self.__dim[1] * 18 + 5 - 40)
        # self.ss_rect.width += 20
        # self.ss_rect.height += 20
        # pygame.draw.rect(self.screen, LIGHT_GRAY, self.ss_rect)
        # self.screen.blit(ss, ((self.__dim[0]) * 20 + 230, self.__dim[1] * 18 - 40))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if (
                    self.slow_rect.x
                    <= mouse[0]
                    <= self.slow_rect.x + self.slow_rect.width
                    and self.slow_rect.y
                    <= mouse[1]
                    <= self.slow_rect.y + self.slow_rect.height
                    and self.rate > 2
                ):
                    self.rate -= 2
                elif (
                    self.fast_rect.x
                    <= mouse[0]
                    <= self.fast_rect.x + self.fast_rect.width
                    and self.fast_rect.y
                    <= mouse[1]
                    <= self.fast_rect.y + self.slow_rect.height
                ):
                    self.rate += 2
                # elif (
                #     self.ss_rect.x
                #     <= mouse[0]
                #     <= self.ss_rect.x + self.ss_rect.width
                #     and self.ss_rect.y
                #     <= mouse[1]
                #     <= self.ss_rect.y + self.ss_rect.height
                # ):
                #         directory = f"{random.randint(1, 100000)}"
                #         if os.path.exists(directory):
                #             directory = f"{random.randint(1, 100000)}"
                #         os.makedirs(directory)
                #         file_name = f"{directory}/screenshot_{directory}.jpg"
                #         rect = pygame.Rect(0, 0, 800, 800)
                #         sub = self.screen.subsurface(rect)
                #         pygame.image.save(sub, file_name)
                #         number_names = np.array([
                #             "B_", "Br", "Bb", "BB", "1_", "1r", "1b", "1B", "2_", "2r", "2b", "2B", "3_", "3r", "3b", "3B"
                #         ])
                #         number_names_array = number_names[self.__Pirates.T]
                #         np.savetxt(f"C:/Users/PRANAV PRAKASH/Projects/codewars-v4/{directory}/pirates_{directory}.txt", number_names_array, fmt='%s', delimiter='|')

    def replenish(self):
        for i in range(0, self.__dim[0]):
            for j in range(0, self.__dim[1]):
                if len(self.__gunpowder) < (self.__dim[0] * self.__dim[1]) / 80:
                    i = 0
                    while i < (self.__dim[0] * self.__dim[1]) / 80:
                        x = random.randint(0, self.__dim[0] - 1)
                        y = random.randint(0, self.__dim[1] - 1)
                        if (
                            self.__collectibles[x][y] == 0
                            and (x, y) not in self.__island1.coordi
                            and (x, y) not in self.__island2.coordi
                            and (x, y) not in self.__island3.coordi
                        ):
                            self.__gunpowder.add(Collectible(self.screen, x, y, -2))
                            self.__collectibles[x][y] = -2
                            i += 1

    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("SCORE BOARD", True, GREEN)
        titlerect = title.get_rect()
        titlerect.x = self.__dim[0] * 20 + 100
        titlerect.y = 40
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render(self.bname, False, BLUE)
        self.screen.blit(blue_head, ((self.__dim[0]) * 20 + 30, self.__dim[1] * 2.5))
        blue_total = norm_font.render(
            "Rum: " + str(round(self.__blue_team._Team__rum, 2)),
            False,
            LIGHT_GRAY,
        )
        self.screen.blit(blue_total, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 3.5))
        blue_total = norm_font.render(
            "Gunpowder: " + str(round(self.__blue_team._Team__gunpowder, 2)),
            False,
            LIGHT_GRAY,
        )
        self.screen.blit(
            blue_total, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 3.5 + 20)
        )
        blue_total = norm_font.render(
            "Wood: " + str(round(self.__blue_team._Team__wood, 2)),
            False,
            LIGHT_GRAY,
        )
        self.screen.blit(
            blue_total, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 3.5 + 40)
        )
        blue_flag1coordi = norm_font.render(
            "Flag 1: " + str(self.__blue_team._Team__flag1), False, LIGHT_GRAY
        )
        self.screen.blit(
            blue_flag1coordi, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 3.5 + 80)
        )
        blue_flag2coordi = norm_font.render(
            "Flag 2: " + str(self.__blue_team._Team__flag2), False, LIGHT_GRAY
        )
        self.screen.blit(
            blue_flag2coordi, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 3.5 + 100)
        )
        blue_flag3coordi = norm_font.render(
            "Flag 3: " + str(self.__blue_team._Team__flag3), False, LIGHT_GRAY
        )
        self.screen.blit(
            blue_flag3coordi, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 3.5 + 120)
        )
        blue_Pirates = norm_font.render(
            "No. of Pirates: " + str(len(self.__blue_pirates)), False, LIGHT_GRAY
        )
        self.screen.blit(
            blue_Pirates, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 3.5 + 60)
        )
        red_flag1coordi = norm_font.render(
            "Flag 1: " + str(self.__red_team._Team__flag1), False, LIGHT_GRAY
        )
        self.screen.blit(
            red_flag1coordi, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 9 + 80)
        )
        red_flag2coordi = norm_font.render(
            "Flag 2: " + str(self.__red_team._Team__flag2), False, LIGHT_GRAY
        )
        self.screen.blit(
            red_flag2coordi, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 9 + 100)
        )
        red_flag3coordi = norm_font.render(
            "Flag 3: " + str(self.__red_team._Team__flag3), False, LIGHT_GRAY
        )
        self.screen.blit(
            red_flag3coordi, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 9 + 120)
        )

        red_head = head_font.render(self.rname, False, RED)
        self.screen.blit(red_head, ((self.__dim[0]) * 20 + 30, self.__dim[1] * 8))
        red_total = norm_font.render(
            "Rum: " + str(round(self.__red_team._Team__rum, 2)),
            False,
            LIGHT_GRAY,
        )
        self.screen.blit(red_total, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 9))
        red_total = norm_font.render(
            "Gunpowder: " + str(round(self.__red_team._Team__gunpowder, 2)),
            False,
            LIGHT_GRAY,
        )
        self.screen.blit(
            red_total, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 9 + 20)
        )

        red_total = norm_font.render(
            "Wood: " + str(round(self.__red_team._Team__wood, 2)),
            False,
            LIGHT_GRAY,
        )
        self.screen.blit(
            red_total, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 9 + 40)
        )

        red_Pirates = norm_font.render(
            "No. of Pirates: " + str(len(self.__red_pirates)), False, LIGHT_GRAY
        )
        self.screen.blit(
            red_Pirates, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 9 + 60)
        )

        s1 = head_font.render(
            status_to_team[self.status1 + 1], False, status_to_color[self.status1 + 1]
        )
        self.screen.blit(s1, ((self.__dim[0]) * 20 + 170, self.__dim[1] * 10 + 170))
        s2 = head_font.render(
            status_to_team[self.status2 + 1], False, status_to_color[self.status2 + 1]
        )
        self.screen.blit(s2, ((self.__dim[0]) * 20 + 170, self.__dim[1] * 10 + 200))
        s3 = head_font.render(
            status_to_team[self.status3 + 1], False, status_to_color[self.status3 + 1]
        )
        self.screen.blit(s3, ((self.__dim[0]) * 20 + 170, self.__dim[1] * 10 + 230))

        if self.__island1.progress():
            s1 = head_font.render(
                self.__island1.progress(),
                False,
                RED if self.__island1.capturing_team == 1 else BLUE,
            )
            self.screen.blit(s1, ((self.__dim[0]) * 20 + 280, self.__dim[1] * 10 + 170))

        if self.__island2.progress():
            s1 = head_font.render(
                self.__island2.progress(),
                False,
                RED if self.__island2.capturing_team == 1 else BLUE,
            )
            self.screen.blit(s1, ((self.__dim[0]) * 20 + 280, self.__dim[1] * 10 + 200))

        if self.__island3.progress():
            s1 = head_font.render(
                self.__island3.progress(),
                False,
                RED if self.__island3.capturing_team == 1 else BLUE,
            )
            self.screen.blit(s1, ((self.__dim[0]) * 20 + 280, self.__dim[1] * 10 + 230))

        island_head = head_font.render("Island Statuses", False, GREEN)
        self.screen.blit(island_head, ((self.__dim[0]) * 20 + 30, self.__dim[1] * 10 + 140))

        stat1 = head_font.render("Island 1: ", False, LIGHT_GRAY)
        self.screen.blit(stat1, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 10 + 170))
        stat2 = head_font.render("Island 2: ", False, LIGHT_GRAY)
        self.screen.blit(stat2, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 10 + 200))
        stat3 = head_font.render("Island 3: ", False, LIGHT_GRAY)
        self.screen.blit(stat3, ((self.__dim[0]) * 20 + 50, self.__dim[1] * 10 + 230))

    def updatePirateMap(self):
        for i in range(0, self.__dim[0]):
            for j in range(0, self.__dim[1]):
                self.__Pirates[i][j] &= ~0b11

        for key in self.__PositionToPirate.keys():
            value = self.__PositionToPirate[key]
            entr = 0
            for v in value:
                if v.__class__.__name__ != "Pirate":
                    continue
                
                if v.type == "red":
                    entr |= 1
                else:
                    entr |= 2
            self.__Pirates[key[0]][key[1]] |= entr

    def collect(self):

        for key in self.__PositionToPirate.keys():
            value = self.__PositionToPirate[key]
            if (
                self.__collectibles[key[0]][key[1]] != 0
                and self.__Pirates[key[0]][key[1]] & 0b11
            ):
                val = self.__collectibles[key[0]][key[1]]
                self.__collectibles[key[0]][key[1]] = 0

                red = 0
                blue = 0
                for v in value:
                    if v.__class__.__name__ != "Pirate":
                        continue

                    if v.type == "red":
                        red += 1
                    else:
                        blue += 1
                self.__red_team.addResource(val, key[0], key[1], red / (red + blue))
                self.__blue_team.addResource(val, key[0], key[1], blue / (red + blue))

    def game_over(self):
        # # print(":(")
        if self.status1 == self.status2 == self.status3 == 1:
            self.winner("red")
            return "red"
        elif self.status1 == self.status2 == self.status3 == -1:
            self.winner("blue")
            return "blue"
        else:
            return None

    def winner(self, team):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)

        if team == "blue":
            # print("Blue Wins")
            game_over = game_over_font.render(
                self.bname + " Wins", True, BLUE, LIGHT_GRAY
            )
            self.screen.blit(game_over, ((self.__dim[0]) * 10, (self.__dim[0]) * 10))

            # time.sleep(5)
            while True:
                pygame.display.flip()
                self.check_events()

        elif team == "red":
            # print("Red Wins")
            game_over = game_over_font.render(
                self.rname + " Wins", True, RED, LIGHT_GRAY
            )
            self.screen.blit(game_over, ((self.__dim[0]) * 10, (self.__dim[0]) * 10))
            pygame.display.flip()
            # time.sleep(5)
            while True:
                pygame.display.flip()
                self.check_events()

    def time_up(self):
        nr = 0
        nb = 0
        for i in [self.status1, self.status2, self.status3]:
            if i == 1:
                nr += 1
            elif i == -1:
                nb += 1
        if nr > nb:
            self.winner("red")
        elif nb > nr:
            self.winner("blue")
        else:
            if len(self.__blue_pirates) > len(self.__red_pirates):
                self.winner("blue")
            elif len(self.__blue_pirates) < len(self.__red_pirates):
                self.winner("red")
            else:
                if (
                    0.5 * self.__red_team._Team__rum
                    + 0.3 * self.__red_team._Team__gunpowder
                    + 0.2 * self.__red_team._Team__wood
                    > 0.5 * self.__blue_team._Team__rum
                    + 0.3 * self.__blue_team._Team__gunpowder
                    + 0.2 * self.__blue_team._Team__wood
                ):
                    self.winner("red")
                elif (
                    0.5 * self.__red_team._Team__rum
                    + 0.3 * self.__red_team._Team__gunpowder
                    + 0.2 * self.__red_team._Team__wood
                    < 0.5 * self.__blue_team._Team__rum
                    + 0.3 * self.__blue_team._Team__gunpowder
                    + 0.2 * self.__blue_team._Team__wood
                ):
                    self.winner("blue")
                else:
                    return None
