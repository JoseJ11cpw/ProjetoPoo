import pygame


# fade out
def fade_out(screen, clock):

    screenshot = screen.copy()

    fade = pygame.Surface(screen.get_size())

    fade.fill((0,0,0))

    for alpha in range(0, 255, 4):

        screen.blit(screenshot, (0,0))

        fade.set_alpha(alpha)

        screen.blit(fade, (0,0))

        pygame.display.update()

        clock.tick(60)


# fade in
def fade_in(screen, clock, background):

    fade = pygame.Surface(screen.get_size())

    fade.fill((0,0,0))

    for alpha in range(255, 0, -4):

        screen.blit(background, (0,0))

        fade.set_alpha(alpha)

        screen.blit(fade, (0,0))

        pygame.display.update()

        clock.tick(60)