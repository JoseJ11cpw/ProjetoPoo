import pygame


# ---------------- FADE OUT ----------------
def fade_out(screen, clock):

    fade = pygame.Surface(screen.get_size())

    fade.fill((0,0,0))

    for alpha in range(0,255,8):

        fade.set_alpha(alpha)

        screen.blit(fade,(0,0))

        pygame.display.update()

        clock.tick(60)


# ---------------- FADE IN ----------------
def fade_in(screen, clock, background):

    fade = pygame.Surface(screen.get_size())

    fade.fill((0,0,0))

    for alpha in range(255,0,-8):

        # REDESENHA O FRAME
        screen.blit(background,(0,0))

        fade.set_alpha(alpha)

        screen.blit(fade,(0,0))

        pygame.display.update()

        clock.tick(60)