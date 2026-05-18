import pygame

from mapa import Map
from Personagens import Player
from camera import Camera
from menu import menu
from npc import NPC
from inventario import Inventario, Item


pygame.init()

# ---------------- SCREEN ----------------
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_W, SCREEN_H = screen.get_size()

clock = pygame.time.Clock()

# ---------------- MENU ----------------
menu()

# ---------------- FONTES ----------------
font = pygame.font.SysFont(None, 40)

# ---------------- MAPAS ----------------
outside_map = Map("mapa.tmx")
house_map = Map("casa.tmx")

current_map = "outside"

game_map = outside_map

# ---------------- CAMERA ----------------
camera = Camera(
    SCREEN_W,
    SCREEN_H,
    game_map.map_w,
    game_map.map_h
)

world = pygame.Surface((game_map.map_w, game_map.map_h))

# ---------------- Músicas/Efeitos Sonoros ----------------
#pygame.mixer.music.load("sua_musica.mp3")
som_porta = pygame.mixer.Sound("musicas/Porta.mp3")

# ---------------- PLAYER ----------------
player = Player()

# ---------------- NPC ----------------
npc = NPC(100,400,"imagens/Npc2.png")

inventario = Inventario()
cristal = Item(100,500,"imagens/cristal.png","Cristal")
# ---------------- FADE ----------------
fade_alpha = 255
start_fade = True

# ---------------- LOOP ----------------
running = True

while running:
    clock.tick(60)
    #pygame.mixer.music.play(-1)
    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # FECHAR JOGO
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_TAB:

                inventario.toggle()
            # INTERAÇÃO NPC
            if event.key == pygame.K_e:

                if npc.near_player(player):

                    npc.dialogo_ativo = True

                elif player.near_door(game_map):
                    som_porta.play()
                    # ENTRAR / SAIR CASA
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

                    # RESET WORLD
                    world = pygame.Surface(
                        (game_map.map_w, game_map.map_h)
                    )

                    # RESET CAMERA
                    camera = Camera(
                        SCREEN_W,
                        SCREEN_H,
                        game_map.map_w,
                        game_map.map_h
                    )
                                # APANHAR ITEM
                if cristal.near_player(player):

                    if not cristal.apanhado:

                        inventario.add_item(cristal.nome)

                        cristal.apanhado = True
            # AVANÇAR DIÁLOGO
            if npc.dialogo_ativo:

                if event.key == pygame.K_SPACE:

                    full_text = npc.dialogo[npc.dialogo_index]

                    # TERMINA TEXTO INSTANTANEAMENTE
                    if npc.char_index < len(full_text):

                        npc.char_index = len(full_text)

                        npc.texto_visivel = full_text

                    # AVANÇA DIÁLOGO
                    else:

                        npc.char_index = 0
                        npc.texto_visivel = ""

                        npc.dialogo_index += 1

                        if npc.dialogo_index >= len(npc.dialogo):

                            npc.dialogo_ativo = False
                            npc.dialogo_index = 0

                    if npc.dialogo_index >= len(npc.dialogo):

                        npc.dialogo_ativo = False
                        npc.dialogo_index = 0

    # ---------------- UPDATE ----------------
    keys = pygame.key.get_pressed()
    npc.update()
    # BLOQUEIA MOVIMENTO DURANTE DIÁLOGO
    if not npc.dialogo_ativo and not inventario.aberto:
        player.update(keys, game_map)

    # UPDATE CAMERA
    if current_map == "outside":
        camera.update(player)

    # ---------------- DRAW WORLD ----------------
    world.fill((0, 0, 0))

    game_map.render(world)
    
    if current_map == "outside":
        npc.draw(world)

    cristal.draw(world)
    player.draw(world)

    # ---------------- CAMERA VIEW ----------------
    view_w = int(SCREEN_W / camera.zoom)
    view_h = int(SCREEN_H / camera.zoom)

    if current_map == "outside":

        cam_x = int(camera.offset_x)
        cam_y = int(camera.offset_y)

    else:

        cam_x = (game_map.map_w - view_w) // 2
        cam_y = (game_map.map_h - view_h) // 2

    # CLAMP
    cam_x = max(0, min(cam_x, game_map.map_w - view_w))
    cam_y = max(0, min(cam_y, game_map.map_h - view_h))

    camera_rect = pygame.Rect(
        cam_x,
        cam_y,
        view_w,
        view_h
    )

    view = world.subsurface(camera_rect)

    scaled = pygame.transform.scale(
        view,
        (SCREEN_W, SCREEN_H)
    )

    screen.blit(scaled, (0, 0))

    # ---------------- UI PORTA ----------------
    if player.near_door(game_map):

        action = (
            "Entrar"
            if current_map == "outside"
            else "Sair"
        )

        ui_rect = pygame.Rect(
            SCREEN_W // 2 - 140,
            SCREEN_H - 120,
            200,
            60
        )

        ui_surface = pygame.Surface(
            (200, 60),
            pygame.SRCALPHA
        )

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

        e_text = font.render(
            "E",
            True,
            (0, 0, 0)
        )

        screen.blit(
            e_text,
            (
                key_rect.centerx - e_text.get_width() // 2,
                key_rect.centery - e_text.get_height() // 2
            )
        )

        action_text = font.render(
            action,
            True,
            (255, 255, 255)
        )

        screen.blit(
            action_text,
            (key_rect.right + 20, ui_rect.y + 12)
        )
    # ---------------- UI ITEM ----------------
    if cristal.near_player(player):

        if not cristal.apanhado:

            action = "Apanhar"

            ui_rect = pygame.Rect(
                SCREEN_W // 2 - 140,
                SCREEN_H - 200,
                220,
                60
            )

            ui_surface = pygame.Surface(
                (220, 60),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                ui_surface,
                (0,0,0,180),
                (0,0,220,60),
                border_radius=12
            )

            screen.blit(ui_surface, ui_rect.topleft)

            pygame.draw.rect(
                screen,
                (255,255,255),
                ui_rect,
                2,
                border_radius=12
            )

            key_text = font.render(
                "E",
                True,
                (255,255,255)
            )

            text = font.render(
                action,
                True,
                (255,255,255)
            )

            screen.blit(
                key_text,
                (ui_rect.x + 20, ui_rect.y + 12)
            )

            screen.blit(
                text,
                (ui_rect.x + 60, ui_rect.y + 12)
            )
    # ---------------- UI NPC ----------------
    if current_map == "outside":

        if npc.near_player(player) and not npc.dialogo_ativo:
            action="Falar"
            ui_rect = pygame.Rect(SCREEN_W // 2 - 140,SCREEN_H - 120,200,60)

            ui_surface = pygame.Surface(
                (200, 60),
                pygame.SRCALPHA
            )

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

            e_text = font.render(
                "E",
                True,
                (0, 0, 0)
            )
            action_text = font.render(action,True,(255, 255, 255))

            screen.blit(
                e_text,
                (
                    key_rect.centerx - e_text.get_width() // 2,
                    key_rect.centery - e_text.get_height() // 2
                )
            )
            screen.blit(
            action_text,
            (key_rect.right + 20, ui_rect.y + 12)
        )

    if inventario.aberto:

        inventario.draw(screen,font,SCREEN_W,SCREEN_H)

    if npc.dialogo_ativo:

        npc.update_dialogo()

        npc.draw_dialogo(screen,font,SCREEN_W,SCREEN_H)
    # ---------------- FADE IN ----------------
    if start_fade:

        fade_surface = pygame.Surface(
            screen.get_size()
        )

        fade_surface.fill((0, 0, 0))

        fade_surface.set_alpha(fade_alpha)

        screen.blit(fade_surface, (0, 0))

        fade_alpha -= 5

        if fade_alpha <= 0:
            start_fade = False

    # ---------------- UPDATE SCREEN ----------------
    pygame.display.flip()

pygame.quit()