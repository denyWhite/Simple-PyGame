import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, stngs,  screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, stngs.bullet_width, stngs.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(ship.rect.top)
        self.color = stngs.bullet_color
        self.speed_factor = stngs.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.top = int(self.y)

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
