import pygame

from mapa import Map, Barco
from Personagens import Player, NPC, Inimigo
from camera import Camera
from menu import menu, pause_menu
from inventario import Inventario, Item
from efeitos import fade_in, fade_out


def draw_interaction_ui(screen, font, action, SCREEN_W, SCREEN_H):

    ui_rect = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 120, 220, 60)

    # fundo
    ui_surface = pygame.Surface((220, 60), pygame.SRCALPHA)

    pygame.draw.rect(ui_surface, (0,0,0,180), (0,0,220,60), border_radius=12)

    screen.blit(ui_surface, ui_rect.topleft)

    # borda
    pygame.draw.rect(screen, (255,255,255), ui_rect, 2, border_radius=12)

    # tecla
    key_rect = pygame.Rect(ui_rect.x + 10, ui_rect.y + 10, 40, 40)

    pygame.draw.rect(screen, (255,255,255), key_rect, border_radius=8)

    e_text = font.render("E", True, (0,0,0))

    screen.blit(e_text, (
        key_rect.centerx - e_text.get_width() // 2,
        key_rect.centery - e_text.get_height() // 2
    ))

    # texto
    action_text = font.render(action, True, (255,255,255))

    screen.blit(action_text, (
        key_rect.right + 20,
        ui_rect.y + 12
    ))


pygame.init()

# musicas e efeitos
pygame.mixer.music.load("musicas/musicaLoop.wav")
som_porta = pygame.mixer.Sound("musicas/Porta.mp3")

pygame.mixer.music.play(-1)

# screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_W, SCREEN_H = screen.get_size()

clock = pygame.time.Clock()

# menu
menu()

screen.fill((0,0,0))

pygame.display.flip()

# fontes
font = pygame.font.SysFont(None, 40)

# mapas
outside_map = Map("mapa.tmx")
house_map = Map("casa.tmx")
ilha = Map("ilha.tmx")

current_map = "outside"

game_map = outside_map

# camera
camera = Camera(
    SCREEN_W,
    SCREEN_H,
    game_map.map_w,
    game_map.map_h
)

world = pygame.Surface((game_map.map_w, game_map.map_h))

# player
player = Player()

# npc
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

# inimigo
enemy = Inimigo(
    800,
    600,
    "imagens/Personagens e Objetos/Polvo.png"
)

# barco
barco = Barco(
    600,
    400,
    "imagens/Personagens e Objetos/barco.png"
)

# inventario
inventario = Inventario()

mochila = pygame.image.load("imagens/Personagens e Objetos/mochila.png").convert_alpha()

mochila = pygame.transform.scale(mochila, (48,48))

# item
moeda = Item(
    100,
    300,
    "imagens/Personagens e Objetos/moeda.png",
    "Moeda",
    40
)

# fade
start_fade = True

# loop
paused = False
running = True

while running:

    clock.tick(60)

    # events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # mouse
        if event.type == pygame.MOUSEBUTTONDOWN:

            if paused:

                mouse = pygame.mouse.get_pos()

                if continue_button.collidepoint(mouse):
                    paused = False

                if quit_button.collidepoint(mouse):
                    running = False

        # teclado
        if event.type == pygame.KEYDOWN:

            # pause
            if event.key == pygame.K_ESCAPE:
                paused = not paused

            # inventario
            if event.key == pygame.K_TAB:
                inventario.toggle()

            # interacoes
            if event.key == pygame.K_e:

                # barco
                if current_map == "outside":

                    if barco.near_player(player):

                        fade_out(screen, clock)

                        game_map = ilha

                        current_map = "ilha"
                        start_fade = True
                        player.x = 600
                        player.y = 400

                # npc preto
                if npc.near_player(player):

                    npc.dialogo_ativo = True

                    npc_ativo = npc

                # npc menina
                if npcMenina.near_player(player):

                    npcMenina.dialogo_ativo = True

                    npc_ativo = npcMenina

                # porta
                elif player.near_door(game_map):

                    som_porta.play()

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

                    world = pygame.Surface((game_map.map_w, game_map.map_h))

                    camera = Camera(
                        SCREEN_W,
                        SCREEN_H,
                        game_map.map_w,
                        game_map.map_h
                    )

                # apanhar item
                if moeda.near_player(player):

                    if not moeda.apanhado:

                        inventario.add_item(moeda)

                        moeda.apanhado = True

            # dialogos
            for personagem in [npc, npcMenina]:

                if personagem.dialogo_ativo:

                    if event.key == pygame.K_SPACE:

                        full_text = personagem.dialogo[personagem.dialogo_index]

                        # termina texto
                        if personagem.char_index < len(full_text):

                            personagem.char_index = len(full_text)

                            personagem.texto_visivel = full_text

                        # avanca dialogo
                        else:

                            personagem.char_index = 0

                            personagem.texto_visivel = ""

                            personagem.dialogo_index += 1

                            if personagem.dialogo_index >= len(personagem.dialogo):

                                personagem.dialogo_ativo = False

                                personagem.dialogo_index = 0

    # update
    keys = pygame.key.get_pressed()

    # inimigo
    if current_map == "ilha":

        enemy.update(player)

        enemy.attack_player(player)

    npc.update()

    # movimento
    if not npc.dialogo_ativo and not inventario.aberto:

        if not paused:

            player.update(keys, game_map)

    # camera
    if current_map != "house":
        camera.update(player)

    # draw world
    game_map.render_ground(world)

    # draw mapa
    if current_map == "outside":

        npc.draw(world)

        moeda.draw(world)

        barco.draw(world)

    if current_map == "house":
        npcMenina.draw(world)

    if current_map == "ilha":
        enemy.draw(world)

    # player
    player.draw(world)

    # foreground
    game_map.render_foreground(world)

    # camera view
    view_w = int(SCREEN_W / camera.zoom)
    view_h = int(SCREEN_H / camera.zoom)

    if current_map == "house":

        cam_x = (game_map.map_w - view_w) // 2
        cam_y = (game_map.map_h - view_h) // 2

    else:

        cam_x = int(camera.offset_x)
        cam_y = int(camera.offset_y)

    # limitar camera
    view_w = min(view_w, game_map.map_w)
    view_h = min(view_h, game_map.map_h)

    max_x = max(0, game_map.map_w - view_w)
    max_y = max(0, game_map.map_h - view_h)

    cam_x = max(0, min(cam_x, max_x))
    cam_y = max(0, min(cam_y, max_y))

    camera_rect = pygame.Rect(cam_x, cam_y, view_w, view_h)

    camera_rect.width = min(camera_rect.width, world.get_width())
    camera_rect.height = min(camera_rect.height, world.get_height())

    # subsurface
    view = world.subsurface(camera_rect)

    scaled = pygame.transform.scale(view, (SCREEN_W, SCREEN_H))

    screen.blit(scaled, (0, 0))

    # fade
    if start_fade:

        fade_in(screen, clock, scaled)

        start_fade = False

    # vida
    player.draw_health(screen)

    # ui inventario
    bag_rect = pygame.Rect(SCREEN_W - 90, 20, 60, 60)

    pygame.draw.rect(screen, (30,30,30), bag_rect, border_radius=12)

    pygame.draw.rect(screen, (255,255,255), bag_rect, 2, border_radius=12)

    screen.blit(mochila, (bag_rect.x + 6, bag_rect.y + 6))

    tab_text = font.render("TAB", True, (255,255,255))

    screen.blit(tab_text, (bag_rect.x - 70, bag_rect.y + 20))

    # ui porta
    if player.near_door(game_map):

        action = "Entrar" if current_map == "outside" else "Sair"

        draw_interaction_ui(
            screen,
            font,
            action,
            SCREEN_W,
            SCREEN_H
        )

    # ui item
    if moeda.near_player(player):

        if current_map == "outside":

            if not moeda.apanhado:

                draw_interaction_ui(
                    screen,
                    font,
                    "Apanhar",
                    SCREEN_W,
                    SCREEN_H
                )

    # ui npc preto
    if npc.near_player(player):

        if current_map == "outside":

            draw_interaction_ui(
                screen,
                font,
                "Falar",
                SCREEN_W,
                SCREEN_H
            )

    # ui npc menina
    if npcMenina.near_player(player):

        if current_map == "house":

            draw_interaction_ui(
                screen,
                font,
                "Falar",
                SCREEN_W,
                SCREEN_H
            )

    # ui barco
    if barco.near_player(player):

        if current_map == "outside":

            draw_interaction_ui(
                screen,
                font,
                "Viajar",
                SCREEN_W,
                SCREEN_H
            )

    # inventario
    if inventario.aberto:

        inventario.draw(
            screen,
            font,
            SCREEN_W,
            SCREEN_H
        )

    # dialogo
    if npc_ativo and npc_ativo.dialogo_ativo:

        npc_ativo.update_dialogo()

        npc_ativo.draw_dialogo(
            screen,
            font,
            SCREEN_W,
            SCREEN_H
        )

    # pause menu
    if paused:

        continue_button, quit_button = pause_menu(
            screen,
            SCREEN_W,
            SCREEN_H
        )

    # update screen
    pygame.display.flip()

pygame.quit()