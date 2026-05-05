import pygame
from mapa import Map
from Personagens import Player

pygame.init()

# ---------------- SCREEN ----------------
SCREEN_W, SCREEN_H = 1920, 1080
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# ---------------- GAME STATE ----------------
state = "menu"

menu_options = ["JOGAR", "SAIR"]
menu_index = 0

# ---------------- MAP / PLAYER ----------------
game_map = None
player = None

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont(None, 140)
option_font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 40)

# ---------------- MENU DRAW ----------------
def draw_menu(screen):
    screen.fill((15, 15, 30))

    # Título
    title = title_font.render("HOT ROLL", True, (255, 200, 0))
    screen.blit(title, (650, 200))

    # Opções
    base_x = 1150
    base_y = 450
    spacing = 120

    for i, option in enumerate(menu_options):

        color = (255, 255, 255)
        offset = 0

        if i == menu_index:
            color = (255, 220, 0)
            offset = 20

        text = option_font.render(option, True, color)
        screen.blit(text, (base_x + offset, base_y + i * spacing))

    # controles
    a = small_font.render("ENTER - CONFIRMAR", True, (200, 200, 200))
    b = small_font.render("ESC - SAIR", True, (200, 200, 200))

    screen.blit(a, (50, 50))
    screen.blit(b, (50, 100))


# ---------------- MAIN LOOP ----------------
running = True

while running:
    clock.tick(60)

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if state == "menu":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    menu_index -= 1

                if event.key == pygame.K_s:
                    menu_index += 1

                if event.key == pygame.K_RETURN:

                    if menu_index == 0:
                        game_map = Map("mapa.tmx")
                        player = Player()
                        state = "jogo"

                    elif menu_index == 1:
                        running = False

                if event.key == pygame.K_ESCAPE:
                    running = False

    # limitar menu
    menu_index = max(0, min(menu_index, len(menu_options) - 1))

    # ---------------- RENDER ----------------
    if state == "menu":
        draw_menu(screen)

    elif state == "jogo":
        keys = pygame.key.get_pressed()

        player.update(keys, game_map.collisions)

        game_map.render(screen)
        player.draw(screen)

    pygame.display.flip()

pygame.quit()