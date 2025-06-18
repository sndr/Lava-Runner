import pygame
from game.entity import Entity

class Background(Entity):
    def __init__(self, x: int):
        try:
            surf = pygame.image.load("assets/background.jpg").convert()
            surf = pygame.transform.scale(surf, (800, 400))
        except FileNotFoundError:
            surf = pygame.Surface((800, 400))
            surf.fill((100, 149, 237))
        rect = surf.get_rect(topleft=(x, 0))
        super().__init__("Background", surf, rect)
        self.speed_x = -5