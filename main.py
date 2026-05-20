import pygame

from mapa import Map, Barco
from Personagens import Player, NPC, Inimigo
from camera import Camera
from menu import menu
from inventario import Inventario, Item


pygame.init()

# ---------------- Músicas/Efeitos Sonoros ----------------
pygame.mixer.music.load("musicas/musicaLoop.wav")
som_porta = pygame.mixer.Sound("musicas/Porta.mp3")

pygame.mixer.music.play(-1)
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
ilha= Map("ilha.tmx")

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

# ---------------- PLAYER ----------------
player = Player()

# ---------------- NPC ----------------
npc = NPC(800,200,"imagens/Preto.png", scale=1)
npc2 = NPC(600,200, "imagens/Npc2.png",scale=1)

enemy = Inimigo(800,600,"imagens/Polvo.png")
barco = Barco(
    600,
    400,
    "imagens/barco.png"
)

inventario = Inventario()
mochila = pygame.image.load("imagens/mochila.png").convert_alpha()
mochila = pygame.transform.scale(mochila,(48,48))
itens = [
    Item(100, 300, "imagens/moeda.png", "Moeda", 40),
    Item(100,200, "imagens/moeda.png", "Espada", 40)
]


# ---------------- FADE ----------------
fade_alpha = 255
start_fade = True

# ---------------- LOOP ----------------
running = True
while running:
    clock.tick(60)
    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # FECHAR JOGO
            if event.key == pygame.K_TAB:

                inventario.toggle()
            # INTERAÇÃO NPC
            if event.key == pygame.K_e:
                # ---------------- BARCO ----------------
                if current_map == "outside":

                    if barco.near_player(player):

                        game_map = ilha

                        current_map = "ilha"

                        player.x = 600
                        player.y = 400

                        # RESET WORLD
                        world = pygame.Surface((game_map.map_w, game_map.map_h))

                        # RESET CAMERA
                        camera = Camera(SCREEN_W,SCREEN_H,game_map.map_w,game_map.map_h)

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
                for item in itens:

                    if item.near_player(player):

                        if not item.apanhado:

                            inventario.add_item(item)

                            item.apanhado = True

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
    if current_map =="ilha":
        enemy.update(player)
        enemy.attack_player(player)

    npc.update()
    # BLOQUEIA MOVIMENTO DURANTE DIÁLOGO
    if not npc.dialogo_ativo and not inventario.aberto:
        player.update(keys, game_map)

    # UPDATE CAMERA
    if current_map != "house":
        camera.update(player)

    # ---------------- DRAW WORLD ----------------
    world.fill((0, 0, 0))

    game_map.render(world)
    player.draw(world)
    if current_map == "outside":
        npc.draw(world)
        npc2.draw(world)
        barco.draw(world)

    for item in itens:

        item.draw(world)

    if current_map=="ilha":

        enemy.draw(world)

    # ---------------- CAMERA VIEW ----------------
    view_w = int(SCREEN_W / camera.zoom)
    view_h = int(SCREEN_H / camera.zoom)

    if current_map == "house":
        cam_x = (game_map.map_w - view_w) // 2
        cam_y = (game_map.map_h - view_h) // 2
    else:
        cam_x = int(camera.offset_x)
        cam_y = int(camera.offset_y)

    # ---------------- FIX CRÍTICO ----------------
    # garantir que a "janela da câmera" não é maior que o mapa
    view_w = min(view_w, game_map.map_w)
    view_h = min(view_h, game_map.map_h)

    # clamp seguro
    max_x = max(0, game_map.map_w - view_w)
    max_y = max(0, game_map.map_h - view_h)

    cam_x = max(0, min(cam_x, max_x))
    cam_y = max(0, min(cam_y, max_y))

    camera_rect = pygame.Rect(
        cam_x,
        cam_y,
        view_w,
        view_h
    )

    # segurança extra (evita crash 100%)
    camera_rect.width = min(camera_rect.width, world.get_width())
    camera_rect.height = min(camera_rect.height, world.get_height())

    # ---------------- SUBSURFACE SAFE ----------------
    view = world.subsurface(camera_rect)
    scaled = pygame.transform.scale(
    view,
    (SCREEN_W, SCREEN_H)
)

    screen.blit(scaled, (0, 0))
    player.draw_health(screen)
    # ---------------- UI INVENTÁRIO ----------------

    bag_rect = pygame.Rect(
        SCREEN_W - 90,
        20,
        60,
        60
    )

    # FUNDO
    pygame.draw.rect(
        screen,
        (30,30,30),
        bag_rect,
        border_radius=12
    )

    # BORDA
    pygame.draw.rect(
        screen,
        (255,255,255),
        bag_rect,
        2,
        border_radius=12
    )

    # IMG
    screen.blit(
        mochila,
        (bag_rect.x + 6, bag_rect.y + 6)
    )
    tab_text = font.render("TAB",True,(255,255,255))

    screen.blit(tab_text,(bag_rect.x - 70,bag_rect.y + 20))

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
    for item in itens:
        if item.near_player(player) and not item.apanhado:

            action = "Apanhar"

            ui_rect = pygame.Rect(
                SCREEN_W // 2 - 140,
                SCREEN_H - 200,
                220,
                60
            )

            # FUNDO
            ui_surface = pygame.Surface((220, 60), pygame.SRCALPHA)

            pygame.draw.rect(
                ui_surface,
                (0, 0, 0, 180),
                (0, 0, 220, 60),
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

            # KEY BOX
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

            # LETRA E
            e_text = font.render("E", True, (0, 0, 0))

            screen.blit(
                e_text,
                (
                    key_rect.centerx - e_text.get_width() // 2,
                    key_rect.centery - e_text.get_height() // 2
                )
            )

            # TEXTO
            text = font.render(action, True, (255, 255, 255))

            screen.blit(
                text,
                (key_rect.right + 20, ui_rect.y + 12)
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
    # ---------------- UI BARCO ----------------
    if barco.near_player(player):

        action = "Viajar"
        if current_map=="outside":

            ui_rect = pygame.Rect(
                SCREEN_W // 2 - 140,
                SCREEN_H - 120,
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