import pygame
from pygame.sprite import Sprite

from .utils import SEA_BLUE


class Collectible(Sprite):
    def __init__(self, screen, x, y, type):
        super().__init__()
        self.screen = screen
        self.type = type
        self.rect = (x*20, y*20, 20, 20)
        self.color = SEA_BLUE

        if self.type == -1: # rum
            self.image = pygame.image.load('images/rum.png')
            
        elif self.type == -2: # gunpowder
            self.image = pygame.image.load('images/gunpowder.png')

        elif self.type == -3: # wood
            self.image = pygame.image.load('images/wood.png')

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Sea(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.rect = (x, y, 20, 20)
        self.color = SEA_BLUE
        self.image = pygame.image.load('images/sea.jpg')

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        # pygame.draw.rect(self.screen, self.color, self.rect)

class Wall(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.rect = (x, y, 20, 20)
        self.image = pygame.image.load('images/wall.png')