import pygame


class Barco:

    def __init__(self, x, y, image):

        self.x = x
        self.y = y

        self.size = 128

        self.image = pygame.image.load(image).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (self.size, self.size)
        )

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

        self.interaction_distance = 70

    # ---------------- DRAW ----------------
    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))

    # ---------------- INTERAÇÃO ----------------
    def near_player(self, player):

        player_rect = pygame.Rect(
            player.x,
            player.y,
            64,
            64
        )

        interaction_rect = self.rect.inflate(
            self.interaction_distance,
            self.interaction_distance
        )

        return interaction_rect.colliderect(player_rect)