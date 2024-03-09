import pygame
from pygame.sprite import Sprite

class Collectible(Sprite):
    def __init__(self, screen, x, y, type):
        super().__init__()
        self.screen = screen
        self.type = type
        self.rect = (x*20, y*20, 20, 20)
        self.color = (30, 207, 216)

        if self.type == -1: # rum
            self.image = pygame.image.load('images/rum.jpg')
            
        elif self.type == -2: # gunpowder
            self.image = pygame.image.load('images/gunpowder.jpg')

        elif self.type == -3: # wood
            self.image = pygame.image.load('images/wood.jpg')

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Sea(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.rect = (x, y, 20, 20)
        self.color = (30, 207, 216)

    def blitme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Wall(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.rect = (x, y, 20, 20)
        self.image = pygame.image.load('images/wall.png')