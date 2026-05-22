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