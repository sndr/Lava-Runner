import pygame
import random
from game.entity import Entity

class Platform(Entity):
    def __init__(self, x: int, y: int = None, prev_y: int = None, speed_x: int = -5):
        try:
            surf = pygame.image.load("assets/lavaplataforma.png").convert_alpha()
            surf = pygame.transform.scale(surf, (150, 40))  # PLATFORM_WIDTH, PLATFORM_HEIGHT
        except FileNotFoundError:
            surf = pygame.Surface((150, 40))
            surf.fill((255, 0, 0))  # Vermelho como fallback
        if y is None:
            min_y = 400 - 250  # PLATFORM_MIN_Y
            max_y = 400 - 100  # PLATFORM_MAX_Y
            if prev_y is None or prev_y > (min_y + max_y) // 2:
                y = random.randint(min_y, (min_y + max_y) // 2)
            else:
                y = random.randint((min_y + max_y) // 2, max_y)
        rect = surf.get_rect(bottom=y, left=x)
        super().__init__("Platform", surf, rect)
        self.speed_x = speed_x
        print(f"Plataforma criada em x={x}, y={y}, speed_x={speed_x}")