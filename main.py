import pygame
from mapa import Map
from Personagens import Player
from camera import Camera

pygame.init()

SCREEN_W, SCREEN_H = 1920, 1080
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)

# ---------------- MAPA ----------------
game_map = Map("mapa.tmx")
camera = Camera(SCREEN_W, SCREEN_H, game_map.map_w, game_map.map_h)

world = pygame.Surface((game_map.map_w, game_map.map_h))

# ---------------- PLAYER ----------------
player = Player()

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, game_map)

    camera.update(player)

    # ---------------- WORLD DRAW ----------------
    world.fill((0, 0, 0))

    game_map.render(world)
    player.draw(world)

    # ---------------- CAMERA VIEW ----------------
    zoom = camera.zoom

    view_w = int(SCREEN_W / zoom)
    view_h = int(SCREEN_H / zoom)

    # clamp camera para não sair do world
    cam_x = int(camera.offset_x)
    cam_y = int(camera.offset_y)

    if cam_x < 0:
        cam_x = 0
    if cam_y < 0:
        cam_y = 0
    if cam_x + view_w > game_map.map_w:
        cam_x = game_map.map_w - view_w
    if cam_y + view_h > game_map.map_h:
        cam_y = game_map.map_h - view_h

    camera_rect = pygame.Rect(cam_x, cam_y, view_w, view_h)

    view = world.subsurface(camera_rect)

    scaled = pygame.transform.scale(view, (SCREEN_W, SCREEN_H))

    screen.blit(scaled, (0, 0))

    pygame.display.flip()

pygame.quit()