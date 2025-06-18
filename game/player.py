import pygame
from game.entity import Entity

class Player(Entity):
    def __init__(self, player_start_y: int):
        try:
            surf = pygame.image.load("assets/player.png").convert_alpha()
            surf = pygame.transform.scale(surf, (60, 80))
        except FileNotFoundError:
            surf = pygame.Surface((40, 60))
            surf.fill((0, 255, 0))  # Verde como fallback
        rect = surf.get_rect(bottom=player_start_y - 40, left=350)  # Centro do chão inicial
        super().__init__("Player", surf, rect)
        self.is_jumping = False
        self.on_platform = True
        self.jump_count = 2

    def jump(self):
        if self.jump_count > 0:
            if self.on_platform or not self.is_jumping:
                self.speed_y = -16  # JUMP_FORCE
            else:
                self.speed_y = -14  # DOUBLE_JUMP_FORCE
            self.is_jumping = True
            self.on_platform = False
            self.jump_count -= 1
            print(f"Pulo executado! Jump count: {self.jump_count}")

    def move(self):
        super().move()
        self.speed_y += 0.7  # GRAVITY
        if self.rect.bottom >= 400:  # WIN_HEIGHT
            print("Jogador tocou o chão!")
            self.rect.bottom = 400
            self.speed_y = 0
            self.is_jumping = False
            return False
        return True