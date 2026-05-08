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
        self.scale = 0.7
        self.scaled_width = int(self.frame_width * self.scale)
        self.scaled_height = int(self.frame_height * self.scale)

        # posição
        self.x = 950
        self.y = 900
        self.speed = 5

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

        # -------- COLISÃO X --------
        self.x += dx
        player_rect = pygame.Rect(self.x, self.y, self.scaled_width, self.scaled_height)

        for wall in game_map.collisions:
            if player_rect.colliderect(wall):
                if dx > 0:  # indo para direita
                    self.x = wall.left - self.scaled_width
                elif dx < 0:  # indo para esquerda
                    self.x = wall.right

        # -------- COLISÃO Y --------
        self.y += dy
        player_rect = pygame.Rect(self.x, self.y, self.scaled_width, self.scaled_height)

        for wall in game_map.collisions:
            if player_rect.colliderect(wall):
                if dy > 0:  # descendo
                    self.y = wall.top - self.scaled_height
                elif dy < 0:  # subindo
                    self.y = wall.bottom

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
        


    def draw(self, screen):
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

        screen.blit(frame, (self.x, self.y))
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.scaled_width, self.scaled_height)