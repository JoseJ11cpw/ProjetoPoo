import pygame
import sys
import random
from efeitos import fade_out


pygame.init()


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = screen.get_size()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

options = ["START", "SAIR"]
selected = 0
background = pygame.image.load("imagens/FundoMenu.jpg").convert()

background = pygame.transform.scale(background, (WIDTH, HEIGHT))
leaves = []

for i in range(30):

    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)

    speed = random.uniform(1, 3)

    leaves.append([x, y, speed])

def menu():

    global selected

    running = True

    while running:

        screen.blit(background, (0, 0))

        titulo = font.render("WHISPERWOOD", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, 120))
        screen.blit(titulo, titulo_rect)

        for i, option in enumerate(options):

            color = (255, 255, 255)

            if i == selected:
                color = (255, 255, 0)

            texto = font.render(option, True, color)
            texto_rect = texto.get_rect(center=(WIDTH // 2, 300 + i * 80))
            screen.blit(texto, texto_rect)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)

                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)

                if event.key == pygame.K_RETURN:

                    if options[selected] == "START":

                        fade_out(screen, clock)

                        return

                    if options[selected] == "SAIR":
                        pygame.quit()
                        sys.exit()
        for leaf in leaves:

            pygame.draw.rect(screen, (34,139,34), (leaf[0], leaf[1], 4, 4))

            leaf[1] += leaf[2]

            if leaf[1] > HEIGHT:
                leaf[0] = random.randint(0, WIDTH)
                leaf[1] = -10
        pygame.display.flip()
        clock.tick(60)