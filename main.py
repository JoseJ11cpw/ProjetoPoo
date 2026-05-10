import pygame
from mapa import Map
from Personagens import Player

pygame.init()

font = pygame.font.SysFont(None, 40)

# ---------------- SCREEN ----------------
SCREEN_W, SCREEN_H = 1920, 1080
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# ---------------- MAPA ----------------
game_map=Map("mapa.tmx")

# ---------------- PLAYER ----------------
player = Player()

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                if player.near_door(game_map):

                    print("Entrou na casa!")

    keys = pygame.key.get_pressed()

    # UPDATE PLAYER
    player.update(keys, game_map)

    # ---------------- LIMITES DO MAPA ----------------
    if player.x < 0:
        player.x = 0
    if player.y < 0:
        player.y = 0

    if player.x > 1920 - player.scaled_width:
        player.x = 1920 - player.scaled_width

    if player.y > 1080 - player.scaled_height:
        player.y = 1080 - player.scaled_height

    # ---------------- DESENHO ----------------

    game_map.render(screen)
    scale_x = SCREEN_W / game_map.map_w
    scale_y = SCREEN_H / game_map.map_h
    if player.near_door(game_map):

        pygame.draw.rect(
            screen,
            (0,0,0),
            (player.x + 10, player.y - 45, 40, 40)
        )

        text = font.render("E", True, (255,255,255))

        screen.blit(text, (player.x + 20, player.y - 40))


    for wall in game_map.collisions:

        scaled_rect = pygame.Rect(wall.x * scale_x,wall.y * scale_y,wall.width * scale_x,wall.height * scale_y)

    player.draw(screen)

    pygame.display.flip()

pygame.quit()