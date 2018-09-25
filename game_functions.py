import sys
import pygame
from bullet import Bullet
from alien import Alien
from colors import Color
from time import sleep


def exit():
    sys.exit()


def fire_bullet(stngs, screen, ship, bullets):
    if len(bullets) < stngs.bullet_max_count:
        b = Bullet(stngs, screen, ship)
        bullets.add(b)


def keydown_events(event, stngs, screen, ship, bullets, stats):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(stngs, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        exit()


def keydown_events_on_begin():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            elif event.key == pygame.K_RETURN:
                return True
    return False


def keydown_events_on_end():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            elif event.key == pygame.K_RETURN:
                return True
    return False


def keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(stngs, screen, ship, bullets, stats):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown_events(event, stngs, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:
            keyup_events(event, ship)


def update_screen(stngs, screen, ship, aliens, bullets, stats):
    screen.fill(stngs.bg_color)
    ship.blitme()
    for bullet in bullets:
        bullet.draw_bullet()
    aliens.draw(screen)
    status_line(stngs, screen, stats)
    pygame.display.flip()


def check_win_or_new_lvl(stngs, screen, ship, aliens, bullets):
    if len(aliens) == 0:
        bullets.empty()
        if stngs.next_lvl():
            win(stngs, screen)
            return True
        else:
            create_fleet(stngs, screen, aliens)
    return False


def update_bullets(stngs, screen, ship, aliens, bullets, stats):
    bullets.update()
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            if stngs.minus_if_miss:
                stats.score -= 1
                if stats.score < 0:
                    stats.score = 0
    l = len(pygame.sprite.groupcollide(bullets, aliens, stngs.bullet_destroy, True))
    if l > 0:
        stats.score += l * stngs.score_for_alien
    return check_win_or_new_lvl(stngs, screen, ship, aliens, bullets)


def check_aliens_bottom(screen, aliens):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            return True
    return False


def update_aliens(stngs, screen, ship, aliens, bullets, stats):
    check_fleet_edges(stngs, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens) or check_aliens_bottom(screen, aliens):
        stats.life -= 1
        if stats.life <= 0:
            lose(stngs, screen)
            return True
        else:
            ship_hit(stngs, stats, screen, ship, aliens, bullets)
    return False


def ship_hit(stngs, stats, screen, ship, aliens, bullets):
    aliens.empty()
    bullets.empty()
    create_fleet(stngs, screen, aliens)
    ship.center_ship()
    image = pygame.image.load("images/bam.png")
    rect = image.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery
    screen.blit(image, rect)
    pygame.display.flip()
    sleep(1)


def status_line(stngs, screen, stats):

    spaces = "     "
    text = "SCORE: {0}{3}LEVEL: {1}{3}LIFE: {2}".format(stats.score, stngs.level, stats.life, spaces)
    fontObj = pygame.font.Font('images/12191.ttf', int(stngs.status_height * .8))
    textSurfaceObj = fontObj.render(text, True, stngs.color, stngs.bg_color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screen.get_rect().width // 2, stngs.status_height // 2)
    screen.blit(textSurfaceObj, textRectObj)



def create_fleet(stngs, screen, aliens):
    aw, ah, i = stngs.alien_width, stngs.alien_height, 1
    for count in stngs.levels[stngs.level]:
        sps_x = (stngs.screen_width - (aw * (count + 1))) // (count + 2)
        for alien_number in range(count):
            alien = Alien(stngs, screen)
            alien.x = sps_x * (alien_number + 1) + aw * alien_number
            alien.rect.x = alien.x
            alien.rect.y = stngs.alien_space * i + (i - 1) * ah + stngs.status_height
            aliens.add(alien)
        i += 1


def check_fleet_edges(stngs, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(stngs, aliens)
            break


def change_fleet_direction(stngs, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += stngs.fleet_drop_speed
    stngs.fleet_direction *= -1


def start(stngs, screen):
    screen.fill(stngs.bg_color)
    fontObj = pygame.font.Font('images/12191.ttf', 200)
    textSurfaceObj = fontObj.render('Star Wars', True, stngs.color, stngs.bg_color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screen.get_rect().width // 2, screen.get_rect().height // 2)
    screen.blit(textSurfaceObj, textRectObj)
    fontObj = pygame.font.Font('images/12191.ttf', 50)
    textSurfaceObj = fontObj.render('Жми Enter для начала игры', True, stngs.color, stngs.bg_color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screen.get_rect().width // 2, screen.get_rect().height - 100)
    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()


def win(stngs, screen):
    screen.fill(Color.navy_blue)
    fontObj = pygame.font.Font('images/12191.ttf', 100)
    textSurfaceObj = fontObj.render('Победа!', True, Color.yellow, Color.navy_blue)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screen.get_rect().width // 2 , screen.get_rect().height // 2)
    screen.blit(textSurfaceObj, textRectObj)
    fontObj = pygame.font.Font('images/12191.ttf', 18)
    textSurfaceObj = fontObj.render('Жми Enter для продолжения или Esc для выхода', True, Color.yellow, Color.navy_blue)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screen.get_rect().width // 2, screen.get_rect().height - 30)
    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()


def lose(stngs, screen):
    screen.fill(Color.navy_blue)
    fontObj = pygame.font.Font('images/12191.ttf', 100)
    textSurfaceObj = fontObj.render('Проигрыш!', True, Color.yellow, Color.navy_blue)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screen.get_rect().width // 2 , screen.get_rect().height // 2)
    screen.blit(textSurfaceObj, textRectObj)
    fontObj = pygame.font.Font('images/12191.ttf', 18)
    textSurfaceObj = fontObj.render('Жми Enter для продолжения или Esc для выхода', True, Color.yellow, Color.navy_blue)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screen.get_rect().width // 2, screen.get_rect().height - 30)
    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()
