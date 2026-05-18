import pygame

import pygame


def fade_in(screen, clock):

    fade_surface = pygame.Surface(screen.get_size())

    fade_surface.fill((0, 0, 0))

    for alpha in range(255, -1, -8):

        fade_surface.set_alpha(alpha)

        # desenha camada preta por cima
        screen.blit(fade_surface, (0, 0))

        pygame.display.flip()

        clock.tick(60)

def fade_out(screen, clock):

    fade_surface = pygame.Surface(screen.get_size())

    fade_surface.fill((0, 0, 0))

    for alpha in range(0, 256, 8):

        fade_surface.set_alpha(alpha)

        screen.blit(fade_surface, (0, 0))

        pygame.display.flip()

        clock.tick(60)