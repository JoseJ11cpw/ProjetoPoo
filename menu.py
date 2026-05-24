import pygame
import sys
import random
from efeitos import fade_out

pygame.init()

# ---------------- FULLSCREEN ----------------
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

SCREEN_W, SCREEN_H = screen.get_size()

clock = pygame.time.Clock()

# ---------------- FONTES ----------------
title_font = pygame.font.Font(
    "fontes/PressStart2P-Regular.ttf",
    90
)

button_font = pygame.font.Font(
    "fontes/PressStart2P-Regular.ttf",
    40
)

small_font = pygame.font.Font(
    "fontes/PressStart2P-Regular.ttf",
    20
)

# ---------------- CORES ----------------
WHITE = (255,255,255)
YELLOW = (255,220,0)
BLACK = (0,0,0)

# ---------------- FUNDO ----------------
background = pygame.image.load(
    "imagens/fundoMenu2.jpg"
).convert()

background = pygame.transform.scale(
    background,
    (SCREEN_W, SCREEN_H)
)

# ---------------- PARTÍCULAS ----------------
particles = []

for i in range(50):

    particles.append([
        random.randint(0, SCREEN_W),
        random.randint(0, SCREEN_H),
        random.randint(2,5)
    ])

# ---------------- BOTÕES ----------------
buttons = [
    "JOGAR",
    "SAIR"
]

selected = 0

# ---------------- MENU ----------------
def menu():

    global selected

    running = True

    while running:

        clock.tick(60)

        # ---------------- EVENTS ----------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:

                    selected += 1

                    if selected >= len(buttons):
                        selected = 0

                if event.key == pygame.K_UP:

                    selected -= 1

                    if selected < 0:
                        selected = len(buttons) - 1

                if event.key == pygame.K_RETURN:

                    if buttons[selected] == "JOGAR":

                        fade_out(screen, clock)

                        running = False

                    if buttons[selected] == "SAIR":
                        pygame.quit()
                        sys.exit()

        # ---------------- DRAW ----------------
        screen.blit(background, (0,0))

        # ---------------- OVERLAY ESCURO ----------------
        overlay = pygame.Surface(
            (SCREEN_W, SCREEN_H),
            pygame.SRCALPHA
        )

        overlay.fill((0,0,0,120))

        screen.blit(overlay, (0,0))

        # ---------------- PARTÍCULAS ----------------
        for particle in particles:

            pygame.draw.circle(
                screen,
                (255,255,255),
                (particle[0], particle[1]),
                particle[2]
            )

            particle[1] -= 1

            if particle[1] < 0:

                particle[0] = random.randint(0, SCREEN_W)
                particle[1] = SCREEN_H

        # ---------------- TÍTULO ----------------
        title = title_font.render(
            "ECHOES OF THE ISLAND",
            True,
            WHITE
        )

        shadow = title_font.render(
            "ECHOES OF THE ISLAND",
            True,
            BLACK
        )

        screen.blit(
            shadow,
            (
                SCREEN_W//2 - title.get_width()//2 + 4,
                140 + 4
            )
        )

        screen.blit(
            title,
            (
                SCREEN_W//2 - title.get_width()//2,
                140
            )
        )

        # ---------------- BOTÕES ----------------
        for i, button in enumerate(buttons):

            color = WHITE

            prefix = "  "

            if i == selected:

                color = YELLOW

                prefix = "> "

            text = button_font.render(
                prefix + button,
                True,
                color
            )

            screen.blit(
                text,
                (
                    SCREEN_W//2 - text.get_width()//2,
                    420 + i * 90
                )
            )

        # ---------------- TEXTO PEQUENO ----------------
        info = small_font.render(
            "ENTER para selecionar",
            True,
            WHITE
        )

        screen.blit(
            info,
            (
                SCREEN_W//2 - info.get_width()//2,
                SCREEN_H - 80
            )
        )

        pygame.display.flip()
# ---------------- MENU PAUSA ----------------
# ---------------- MENU PAUSA ----------------
def pause_menu(screen, SCREEN_W, SCREEN_H):

    mouse = pygame.mouse.get_pos()

    # OVERLAY
    overlay = pygame.Surface(
        (SCREEN_W, SCREEN_H),
        pygame.SRCALPHA
    )

    overlay.fill((0,0,0,180))

    screen.blit(overlay, (0,0))

    # ---------------- CAIXA ----------------
    rect = pygame.Rect(
        SCREEN_W//2 - 300,
        SCREEN_H//2 - 220,
        600,
        400
    )

    pygame.draw.rect(
        screen,
        (220,200,160),
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (80,50,20),
        rect,
        6,
        border_radius=12
    )

    # ---------------- FONTES ----------------
    title_font = pygame.font.Font(
        "fontes/PressStart2P-Regular.ttf",
        40
    )

    button_font = pygame.font.Font(
        "fontes/PressStart2P-Regular.ttf",
        20
    )

    # ---------------- TÍTULO ----------------
    title = title_font.render(
        "PAUSA",
        True,
        (20,20,20)
    )

    screen.blit(
        title,
        (
            rect.centerx - title.get_width()//2,
            rect.y + 50
        )
    )

    # ---------------- BOTÕES ----------------
    continue_button = pygame.Rect(
        rect.centerx - 180,
        rect.y + 150,
        360,
        70
    )

    quit_button = pygame.Rect(
        rect.centerx - 180,
        rect.y + 260,
        360,
        70
    )

    # HOVER
    continue_color = (220,200,160)

    if continue_button.collidepoint(mouse):

        continue_color = (255,230,180)

    quit_color = (220,200,160)

    if quit_button.collidepoint(mouse):

        quit_color = (255,230,180)

    # DESENHAR BOTÕES
    pygame.draw.rect(
        screen,
        continue_color,
        continue_button,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        (80,50,20),
        continue_button,
        4,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        quit_color,
        quit_button,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        (80,50,20),
        quit_button,
        4,
        border_radius=8
    )

    # ---------------- TEXTO ----------------
    continue_text = button_font.render(
        "CONTINUAR",
        True,
        (20,20,20)
    )

    quit_text = button_font.render(
        "SAIR",
        True,
        (20,20,20)
    )

    screen.blit(
        continue_text,
        (
            continue_button.centerx
            - continue_text.get_width()//2,

            continue_button.centery
            - continue_text.get_height()//2
        )
    )

    screen.blit(
        quit_text,
        (
            quit_button.centerx
            - quit_text.get_width()//2,

            quit_button.centery
            - quit_text.get_height()//2
        )
    )

    return continue_button, quit_button