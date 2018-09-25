import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Класс представляющий одного пришельца """
    def __init__(self, stngs, screen):
        super().__init__()
        self.screen = screen
        self.stngs = stngs
        self.image = pygame.transform.scale(pygame.image.load("images/alien.png"),
                                            (stngs.alien_width, stngs.alien_height))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height + stngs.status_height
        # Сохранение точной позиции пришельца.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False

    def update(self):
        self.x += self.stngs.alien_speed_factor * self.stngs.fleet_direction
        self.rect.x = self.x