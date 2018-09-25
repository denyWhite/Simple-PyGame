import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from stats import Stats


def run_game(sw, sh, fullscreen):
    pygame.init()
    if fullscreen:
        screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((sw, sh))

    # Настройки экрана
    stngs = Settings(screen)
    pygame.display.set_caption(stngs.capthion)
    pygame.mouse.set_visible(stngs.mouse_visible)

    clock = pygame.time.Clock()

    gf.start(stngs, screen)
    stats = Stats(stngs)

    while True:
        if stats.state == 1:  # Заставка
            if gf.keydown_events_on_begin():
                ship = Ship(stngs, screen)  # Создаем корабль
                bullets = Group()  # Группа для хранения пуль
                aliens = Group()  # Группа для хранения пришельцев
                gf.create_fleet(stngs, screen, aliens)
                stats.reset_stats()
                stats.state = 2
        elif stats.state == 2:  # Игра
            gf.check_events(stngs, screen, ship, bullets, stats)
            ship.update_position()
            if gf.update_bullets(stngs, screen, ship, aliens, bullets, stats):
                stats.state = 3
                continue
            if gf.update_aliens(stngs, screen, ship, aliens, bullets, stats):
                stats.state = 4
                continue
            gf.update_screen(stngs, screen, ship, aliens, bullets, stats)
        elif stats.state == 3:  # Выигрыш
            if gf.keydown_events_on_end():
                gf.start(stngs, screen)
                stats.state = 1
        elif stats.state == 4:  # Проигрыш
            if gf.keydown_events_on_end():
                gf.start(stngs, screen)
                stats.state = 1
        clock.tick(stngs.framerate)


fullscreen = True
sw = 1360
sh = 768
run_game(sw, sh, fullscreen)