import pygame

from mapa import Map, Barco
from Personagens import Player, NPC, Inimigo
from camera import Camera
from menu import menu
from inventario import Inventario, Item
from efeitos import fade_in

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
npc = NPC(
    800,
    200,
    "imagens/Personagens e Objetos/Preto.png",
    [
        "Olá aventureiro!",
        "Tem cuidado com a ilha.",
        "Há monstros perigosos."
    ],
    scale=1
)

npcMenina = NPC(
    500,
    150,
    "imagens/Personagens e Objetos/Npc2.png",
    [
        "Olá!",
        "Perdi a minha moeda...",
        "Podes ajudar-me?"
    ],
    scale=1
)
npc_ativo = None

enemy = Inimigo(800,600,"imagens/Personagens e Objetos/Polvo.png")
barco = Barco(
    600,
    400,
    "imagens/Personagens e Objetos/barcoAfonso.png"
)

inventario = Inventario()
mochila = pygame.image.load("imagens/Personagens e Objetos/mochila.png").convert_alpha()
mochila = pygame.transform.scale(mochila,(48,48))

moeda = Item(100, 300, "imagens/Personagens e Objetos/moeda.png", "Moeda", 40)

# ---------------- FADE ----------------
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
                if current_map =="outside":

                    if barco.near_player(player):

                        game_map = ilha

                        current_map = "ilha"

                        player.x = 600
                        player.y = 400

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


                if npc.near_player(player):
                    npc.dialogo_ativo = True
                    npc_ativo = npc

                if npcMenina.near_player(player):
                    npcMenina.dialogo_ativo = True
                    npc_ativo = npcMenina

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
                if moeda.near_player(player):

                    if not moeda.apanhado:

                        inventario.add_item(moeda)

                        moeda.apanhado = True
            # AVANÇAR DIÁLOGO
            for personagem in [npc, npcMenina]:

                if personagem.dialogo_ativo:

                    if event.key == pygame.K_SPACE:

                        full_text = personagem.dialogo[personagem.dialogo_index]

                        # TERMINA TEXTO INSTANTANEAMENTE
                        if personagem.char_index < len(full_text):

                            personagem.char_index = len(full_text)
                            personagem.texto_visivel = full_text

                        # AVANÇA DIÁLOGO
                        else:

                            personagem.char_index = 0
                            personagem.texto_visivel = ""

                            personagem.dialogo_index += 1

                            if personagem.dialogo_index >= len(personagem.dialogo):

                                personagem.dialogo_ativo = False
                                personagem.dialogo_index = 0

                        if personagem.dialogo_index >= len(personagem.dialogo):

                            personagem.dialogo_ativo = False
                            personagem.dialogo_index = 0

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
    game_map.render_ground(world)  # 1. Desenha o chão

    if current_map == "outside":
        npc.draw(world)
        moeda.draw(world)
        barco.draw(world)
    if current_map == "house":
        npcMenina.draw(world)
    if current_map == "ilha":
        enemy.draw(world)

    player.draw(world)             # 2. Desenha o Jogador

    game_map.render_foreground(world) # 3. Desenha as copas por cima do jogador

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
    screen.blit(scaled, (0, 0))

    # ---------------- FADE IN ----------------
    if start_fade:

        fade_in(screen, clock, scaled)

        start_fade = False
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
    if moeda.near_player(player):

        if not moeda.apanhado:

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
    # ---------------- UI NPC preto ----------------
    if current_map == "outside":

        if npc.near_player(player) and not npc.dialogo_ativo :
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
     # npc menina       
    if current_map == "house":

        if npcMenina.near_player(player) and not npcMenina.dialogo_ativo :

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

    if npc_ativo and npc_ativo.dialogo_ativo:
        npc.update_dialogo()
        npc.draw_dialogo(screen,font,SCREEN_W,SCREEN_H)

    if npcMenina.dialogo_ativo:
        npcMenina.update_dialogo()
        npcMenina.draw_dialogo(screen,font,SCREEN_W,SCREEN_H)

    # ---------------- UI BARCO ----------------
    if current_map =="outside":

        if barco.near_player(player):

            action = "Viajar"

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

    # ---------------- UPDATE SCREEN ----------------
    pygame.display.flip()
    
pygame.quit()