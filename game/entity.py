import pygame

class Entity:
    def __init__(self, name: str, surf: pygame.Surface, rect: pygame.Rect):
        self.name = name
        self.surf = surf
        self.rect = rect
        self.speed_x = 0
        self.speed_y = 0

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y