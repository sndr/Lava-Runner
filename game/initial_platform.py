import pygame
from game.entity import Entity

class InitialPlatform(Entity):
    def __init__(self):
        try:
            surf = pygame.image.load("assets/chãoinicial.png").convert_alpha()
            surf = pygame.transform.scale(surf, (300, 40))  # INITIAL_PLATFORM_WIDTH, INITIAL_PLATFORM_HEIGHT
        except FileNotFoundError:
            surf = pygame.Surface((300, 40))
            surf.fill((0, 128, 255))  # Azul neon como fallback
        rect = surf.get_rect(bottom=400, left=250)  # WIN_HEIGHT, centrado
        super().__init__("InitialPlatform", surf, rect)
        self.speed_x = 0  # Fixo, sem movimento