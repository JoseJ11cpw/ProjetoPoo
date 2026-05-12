import pygame


class Player:
    def __init__(self):
        # ---------------- SPRITE ----------------
        self.sprite = pygame.image.load("imagens/Personagem1.png").convert_alpha()

        self.FRAME_COLS = 4
        self.FRAME_ROWS = 4

        self.SPRITE_WIDTH = 408
        self.SPRITE_HEIGHT = 611

        self.frame_width = self.SPRITE_WIDTH // self.FRAME_COLS
        self.frame_height = self.SPRITE_HEIGHT // self.FRAME_ROWS

        # escala
        self.scale = 0.25
        self.scaled_width = int(self.frame_width * self.scale)
        self.scaled_height = int(self.frame_height * self.scale)

        # posição inicial
        self.x = 100
        self.y = 400
        self.speed = 2

        # direção
        self.DOWN = 0
        self.LEFT = 2
        self.RIGHT = 3
        self.UP = 1

        self.direction = self.DOWN

        # animação
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 10

        # HITBOX
        self.hitbox_offset_x = 6
        self.hitbox_offset_y = 20  #sobe/desce a hitbox
        self.hitbox_width = self.scaled_width - 12
        self.hitbox_height = 16 #altura da hitbox

    def update(self, keys, game_map):
        dx = 0
        dy = 0
        moving = False

        # -------- INPUT --------
        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = self.LEFT
            moving = True

        if keys[pygame.K_d]:
            dx = self.speed
            self.direction = self.RIGHT
            moving = True

        if keys[pygame.K_w]:
            dy = -self.speed
            self.direction = self.UP
            moving = True

        if keys[pygame.K_s]:
            dy = self.speed
            self.direction = self.DOWN
            moving = True
        # -------- NORMALIZAR DIAGONAL --------
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        # -------- COLISÃO X --------
        self.x += dx
        player_rect = self.get_rect()

        for wall in game_map.collisions:
            if player_rect.colliderect(wall):

                if dx > 0:
                    self.x = (
                        wall.left
                        - self.hitbox_width
                        - self.hitbox_offset_x
                    )

                if dx < 0:
                    self.x = wall.right - self.hitbox_offset_x

        # -------- COLISÃO Y --------
        self.y += dy
        player_rect = self.get_rect()

        for wall in game_map.collisions:
            if player_rect.colliderect(wall):

                if dy > 0:
                    self.y = (
                        wall.top
                        - self.hitbox_height
                        - (self.scaled_height - self.hitbox_offset_y)
                    )

                if dy < 0:
                    self.y = (
                        wall.bottom
                        - (self.scaled_height - self.hitbox_offset_y)
                    )

        # -------- ANIMAÇÃO --------
        if moving:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index += 1
                if self.frame_index >= self.FRAME_COLS:
                    self.frame_index = 0
        else:
            self.frame_index = 0

        # ---------------- LIMITES DO MAPA ----------------
        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

        if self.x > game_map.map_w - self.scaled_width:
            self.x = game_map.map_w - self.scaled_width

        if self.y > game_map.map_h - self.scaled_height:
            self.y = game_map.map_h - self.scaled_height


    def draw(self, surface):
        frame = self.sprite.subsurface((
            self.frame_index * self.frame_width,
            self.direction * self.frame_height,
            self.frame_width,
            self.frame_height
        ))

        frame = pygame.transform.smoothscale(
            frame,
            (self.scaled_width, self.scaled_height)
        )

        surface.blit(frame, (self.x, self.y))


    def get_rect(self):
        return pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.scaled_height - self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )

    def near_door(self, game_map):

        player_rect = self.get_rect()

        for door in game_map.doors:

            if player_rect.colliderect(door):
                return True

        return False