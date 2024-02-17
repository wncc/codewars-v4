import pygame
from pygame.sprite import Sprite

class Collectible(Sprite):
    def __init__(self, screen, x, y, points):
        super().__init__()
        self.screen = screen
        self.initPoints = points
        self.points = points
        self.rect = (x, y, 20, 20)
        self.color = (60,60,60)
        self.setColor()
    def blitme(self):
        pygame.draw.rect(self.screen, self.color,  self.rect)

    def setColor(self):
        # if self.points <-40:
        #     self.color = (32, 0, 84)
        # elif self.points<-20:
        #     self.color = (108, 0, 171)
        # elif self.points<0:
        #     self.color = (201, 84, 255)
        # elif self.points == 0:
        #     self.color = (240, 240, 240)
        # elif self.points < 20:
        #     self.color = (252, 243, 61)
        # elif self.points<40:
        #     self.color = (200, 235, 0)
        # else:
        #     self.color = (77, 255, 0)
        if self.points == 0:
            self.color = (30, 207, 216)
        elif self.points == 1: # rum

        elif self.points == 2: # gunpowder

        elif self.points == 3: # wood
