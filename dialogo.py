import pygame


class Dialogo:

    def __init__(self):

        self.active = False

        self.index = 0

    def draw(self, screen, text, font, SCREEN_W, SCREEN_H):

        rect = pygame.Rect(
            100,
            SCREEN_H - 220,
            SCREEN_W - 200,
            140
        )

        # fundo
        pygame.draw.rect(screen, (20,20,20), rect)

        # borda
        pygame.draw.rect(screen, (255,255,255), rect, 4)

        rendered = font.render(text, True, (255,255,255))

        screen.blit(rendered, (rect.x + 20, rect.y + 30))