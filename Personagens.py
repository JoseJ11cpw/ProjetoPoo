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
        self.x = 300
        self.y = 300
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

    def update(self, keys):
        moving = False

        if keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = self.LEFT
            moving = True

        if keys[pygame.K_d]:
            self.x += self.speed
            self.direction = self.RIGHT
            moving = True

        if keys[pygame.K_w]:
            self.y -= self.speed
            self.direction = self.UP
            moving = True

        if keys[pygame.K_s]:
            self.y += self.speed
            self.direction = self.DOWN
            moving = True

        # animação
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