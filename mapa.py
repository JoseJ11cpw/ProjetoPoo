import pygame
from pytmx.util_pygame import load_pygame


class Map:
    def __init__(self, file):
        self.tmx = load_pygame(file)

        # tamanho do mundo (SEM escala)
        self.map_w = self.tmx.width * self.tmx.tilewidth
        self.map_h = self.tmx.height * self.tmx.tileheight

        # surface do mapa no tamanho real do mundo
        self.surface = pygame.Surface((self.map_w, self.map_h))

        self.draw_map()

        # ---------------- COLISÕES ----------------
        self.collisions = []

        for obj in self.tmx.objects:
            if obj.name == "wall":
                rect = pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                )
                self.collisions.append(rect)

        # ---------------- PORTAS ----------------
        self.doors = []

        for obj in self.tmx.objects:
            if obj.name == "door":
                rect = pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                )
                self.doors.append(rect)

    # ---------------- DESENHAR MAPA ----------------
    def draw_map(self):
        TILE = self.tmx.tilewidth

        for layer in self.tmx.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        self.surface.blit(tile, (x * TILE, y * TILE))

    # ---------------- RENDER (COM CAMERA) ----------------
    def render(self, surface):
        # desenha o mapa completo no mundo
        surface.blit(self.surface, (0, 0))

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