import pygame
from mapa import Map
from Personagens import Player
from camera import Camera

pygame.init()

SCREEN_W, SCREEN_H = 1920, 1080
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont("arial", 32, bold=True)

# ---------------- MAPAS ----------------
outside_map = Map("mapa.tmx")
house_map = Map("casa.tmx")

current_map = "outside"
game_map = outside_map

camera = Camera(
    SCREEN_W,
    SCREEN_H,
    game_map.map_w,
    game_map.map_h
)

world = pygame.Surface((game_map.map_w, game_map.map_h))

# ---------------- PLAYER ----------------
player = Player()

running = True

while running:
    clock.tick(60)

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                if player.near_door(game_map):

                    # ENTRAR / SAIR
                    if current_map == "outside":

                        game_map = house_map
                        current_map = "house"

                        player.x = 340
                        player.y = 280

                    else:

                        game_map = outside_map
                        current_map = "outside"

                        player.x = 228
                        player.y = 70

                    # reset world
                    world = pygame.Surface((game_map.map_w, game_map.map_h))

                    # reset camera
                    camera = Camera(
                        SCREEN_W,
                        SCREEN_H,
                        game_map.map_w,
                        game_map.map_h
                    )

    # ---------------- UPDATE ----------------
    keys = pygame.key.get_pressed()
    player.update(keys, game_map)

    if current_map == "outside":
        camera.update(player)

    # ---------------- DRAW WORLD ----------------
    world.fill((0, 0, 0))

    game_map.render(world)
    player.draw(world)

    # ---------------- VIEW ----------------
    view_w = int(SCREEN_W / camera.zoom)
    view_h = int(SCREEN_H / camera.zoom)

    if current_map == "outside":

        cam_x = int(camera.offset_x)
        cam_y = int(camera.offset_y)

    else:
        # CASA CENTRADA
        cam_x = (game_map.map_w - view_w) // 2
        cam_y = (game_map.map_h - view_h) // 2

    # clamp (seguro)
    cam_x = max(0, min(cam_x, game_map.map_w - view_w))
    cam_y = max(0, min(cam_y, game_map.map_h - view_h))

    camera_rect = pygame.Rect(cam_x, cam_y, view_w, view_h)

    view = world.subsurface(camera_rect)

    scaled = pygame.transform.scale(view, (SCREEN_W, SCREEN_H))

    screen.blit(scaled, (0, 0))

    # ---------------- UI PORTA ----------------
    if player.near_door(game_map):

        action = "Entrar" if current_map == "outside" else "Sair"

        ui_rect = pygame.Rect(
            SCREEN_W // 2 - 140,
            SCREEN_H - 120,
            200,
            60
        )

        ui_surface = pygame.Surface((200, 60), pygame.SRCALPHA)

        pygame.draw.rect(
            ui_surface,
            (0, 0, 0, 180),
            (0, 0, 200, 60),
            border_radius=12
        )

        screen.blit(ui_surface, ui_rect.topleft)

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            ui_rect,
            2,
            border_radius=12
        )

        key_rect = pygame.Rect(
            ui_rect.x + 10,
            ui_rect.y + 10,
            40,
            40
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            key_rect,
            border_radius=8
        )

        e_text = font.render("E", True, (0, 0, 0))

        screen.blit(
            e_text,
            (
                key_rect.centerx - e_text.get_width() // 2,
                key_rect.centery - e_text.get_height() // 2
            )
        )

        action_text = font.render(action, True, (255, 255, 255))

        screen.blit(
            action_text,
            (key_rect.right + 20, ui_rect.y + 12)
        )

    pygame.display.flip()

pygame.quit()