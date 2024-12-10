import pygame
import random
import os
from pygame.constants import QUIT, K_UP, K_RIGHT, K_DOWN, K_LEFT
from pygame.mask import from_surface

pygame.init()

# Display setup
HEIGHT = 800
WIDTH = 1200
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = pygame.time.Clock()
FONT = pygame.font.SysFont("Verdana", 20)
FONT_GAME_OVER = pygame.font.SysFont("Verdana", 80)
bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)


def start_screen():
    start_running = True
    while start_running:
        FPS.tick(120)
        global bg_X1, bg_X2

        # Background movement
        bg_X1 -= bg_move
        bg_X2 -= bg_move
        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))

        # Dimmed overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(COLOR_BLACK)
        main_display.blit(overlay, (0, 0))

        # "Play Game" button
        title_text = FONT.render("Play Game", True, COLOR_WHITE)
        title_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        pygame.draw.rect(main_display, COLOR_GREEN, title_rect, border_radius=10)
        main_display.blit(
            title_text,
            (title_rect.centerx - title_text.get_width() // 2, title_rect.centery - title_text.get_height() // 2),
        )

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if title_rect.collidepoint(event.pos):
                    start_running = False

        pygame.display.flip()


def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(80, HEIGHT - 80), enemy.get_width(), enemy.get_height())
    enemy_move = [random.randint(-9, -5), 0]
    enemy_mask = from_surface(enemy)
    return [enemy, enemy_rect, enemy_move, enemy_mask]


def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(random.randint(185, WIDTH - 185), -50, bonus.get_width(), bonus.get_height())
    bonus_move = [0, random.randint(3, 5)]
    bonus_mask = from_surface(bonus)
    return [bonus, bonus_rect, bonus_move, bonus_mask]


def game_over_screen():
    while True:
        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))

        game_over_text = FONT_GAME_OVER.render("GAME OVER", True, COLOR_RED)
        main_display.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

        play_again_text = FONT.render("Play Again", True, COLOR_GREEN)
        play_again_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(main_display, COLOR_WHITE, play_again_rect, border_radius=10)
        main_display.blit(
            play_again_text,
            (play_again_rect.centerx - play_again_text.get_width() // 2, play_again_rect.centery - play_again_text.get_height() // 2),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_rect.collidepoint(event.pos):
                    return True


# Game loop setup
player = pygame.image.load("player.png").convert_alpha()
player_mask = from_surface(player)
player_rect = player.get_rect(topleft=(85, HEIGHT // 3))
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)
image_index = 0

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses = []

score = 0
playing = True
start_screen()

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])).convert_alpha()
            player_mask = from_surface(player)

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom <= HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right <= WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_mask.overlap(enemy[3], (enemy[1].x - player_rect.x, enemy[1].y - player_rect.y)):
            if not game_over_screen():
                playing = False
            else:
                score = 0
                player_rect.topleft = (85, HEIGHT // 3)
                enemies.clear()
                bonuses.clear()
                break

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_mask.overlap(bonus[3], (bonus[1].x - player_rect.x, bonus[1].y - player_rect.y)):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)
    pygame.display.flip()

    enemies = [enemy for enemy in enemies if enemy[1].right > 0]
    bonuses = [bonus for bonus in bonuses if bonus[1].top < HEIGHT]

pygame.quit()