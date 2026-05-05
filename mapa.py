import pygame
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, file):
        self.tmx = load_pygame(file)

        self.map_w = self.tmx.width * self.tmx.tilewidth
        self.map_h = self.tmx.height * self.tmx.tileheight

        self.surface = pygame.Surface((self.map_w, self.map_h))
        self.draw_map()

        # colisões
        self.collisions = []

        for obj in self.tmx.objects:
            if obj.name == "wall":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.collisions.append(rect)

    def draw_map(self):
        TILE = self.tmx.tilewidth

        for layer in self.tmx.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        self.surface.blit(tile, (x * TILE, y * TILE))

    def render(self, screen):
        scaled = pygame.transform.scale(self.surface,screen.get_size()  # força 1920x1080
        )

        screen.blit(scaled, (0, 0))