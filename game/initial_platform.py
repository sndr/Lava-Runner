import pygame
from game.entity import Entity

class InitialPlatform(Entity):
    def __init__(self):
        try:
            surf = pygame.image.load("assets/chãoinicial.png").convert_alpha()
            surf = pygame.transform.scale(surf, (300, 40))
        except FileNotFoundError:
            surf = pygame.Surface((300, 40))
            surf.fill((0, 128, 255))
        rect = surf.get_rect(bottom=400, left=250)
        super().__init__("InitialPlatform", surf, rect)
        self.speed_x = 0