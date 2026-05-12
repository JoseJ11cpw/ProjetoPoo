class Camera:
    def __init__(self, screen_w, screen_h, world_w, world_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.world_w = world_w
        self.world_h = world_h

        self.offset_x = 0
        self.offset_y = 0

        self.zoom = 3.0   # 👈 AQUI tens o zoom (2 = mais perto)

    def update(self, player):
        self.offset_x = player.x + player.scaled_width // 2 - self.screen_w // (2 * self.zoom)
        self.offset_y = player.y + player.scaled_height // 2 - self.screen_h // (2 * self.zoom)

        # limitar ao mundo
        max_x = self.world_w - self.screen_w / self.zoom
        max_y = self.world_h - self.screen_h / self.zoom

        self.offset_x = max(0, min(self.offset_x, max_x))
        self.offset_y = max(0, min(self.offset_y, max_y))