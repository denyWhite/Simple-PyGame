import pygame

class Ship:
    def __init__(self, stngs, screen):
        """ Инициализирует корабль и задает начальную позицию"""
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load("images/ship.png"),
                                            (stngs.ship_width, stngs.ship_height))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.stngs = stngs
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.screen_rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False

    def update_position(self):
        if self.moving_left and self.rect.left > 0:
            self.center -= self.stngs.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.stngs.ship_speed_factor
        self.rect.centerx = int(self.center)

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.screen_rect.centerx)

    def blitme(self):
            """Рисует корабль в текущей позиции."""
            self.screen.blit(self.image, self.rect)