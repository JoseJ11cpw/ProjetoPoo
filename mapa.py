import pygame
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, file):
        self.tmx = load_pygame(file)

        self.map_w = self.tmx.width * self.tmx.tilewidth
        self.map_h = self.tmx.height * self.tmx.tileheight
        self.screen_w = 1920
        self.screen_h = 1080

        self.scale_x = self.screen_w / self.map_w
        self.scale_y = self.screen_h / self.map_h

        self.surface = pygame.Surface((self.map_w, self.map_h))
        self.draw_map()

        # colisões
        self.collisions = []

        for obj in self.tmx.objects:
            if obj.name == "wall":
                rect = pygame.Rect( obj.x * self.scale_x,obj.y * self.scale_y,obj.width * self.scale_x, obj.height * self.scale_y)
                self.collisions.append(rect)
        
        self.doors = []

        for obj in self.tmx.objects:

            if obj.name == "door":

                rect = pygame.Rect(
                    obj.x * self.scale_x,
                    obj.y * self.scale_y,
                    obj.width * self.scale_x,
                    obj.height * self.scale_y
                )

                self.doors.append(rect)

    def draw_map(self):
        TILE = self.tmx.tilewidth
        for layer in self.tmx.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        self.surface.blit(tile, (x * TILE, y * TILE))
    def render(self, screen):
        screen_width, screen_height = screen.get_size()
        scaled_surface = pygame.transform.scale(self.surface,(screen_width, screen_height))
        screen.blit(scaled_surface, (0, 0))

        # DEBUG DAS PORTAS
        for door in self.doors:
            pygame.draw.rect(screen, (0,255,0), door, 2)