import pygame
import math

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
        self.vida=100
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


class NPC:

    def __init__(self, x, y, image, scale=1):

        self.x = x
        self.y = y

        # ---------------- IMAGEM ORIGINAL ----------------
        self.image_original = pygame.image.load(image).convert_alpha()

        # ---------------- ESCALA SEM DISTORCER ----------------
        largura_original = self.image_original.get_width()
        altura_original = self.image_original.get_height()

        self.largura = int(largura_original * scale)
        self.altura = int(altura_original * scale)

        self.image = pygame.transform.scale(
            self.image_original,
            (self.largura, self.altura)
        )

        # ---------------- HITBOX ----------------
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

        # ---------------- ÁREA DE INTERAÇÃO ----------------
        self.interaction_rect = self.rect.inflate(80, 80)

        # ---------------- DIÁLOGO ----------------
        self.dialogo = [
            "Olá aventureiro...",
            "A floresta foi corrompida.",
            "Encontra os 3 cristais."
        ]

        self.dialogo_ativo = False
        self.dialogo_index = 0

        self.texto_visivel = ""
        self.char_index = 0

        self.last_update = pygame.time.get_ticks()
        self.text_speed = 30

    # ---------------- UPDATE ----------------
    def update(self):

        self.rect.topleft = (self.x, self.y)
        self.interaction_rect = self.rect.inflate(80, 80)

    # ---------------- DESENHAR NPC ----------------
    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))

    # ---------------- VERIFICAR DISTÂNCIA PLAYER ----------------
    def near_player(self, player):

        player_rect = pygame.Rect(
            player.x,
            player.y,
            64,
            64
        )

        return self.interaction_rect.colliderect(player_rect)

    # ---------------- DESENHAR DIÁLOGO ----------------
    def draw_dialogo(self, screen, font, SCREEN_W, SCREEN_H):

        rect = pygame.Rect(
            120,
            SCREEN_H - 240,
            SCREEN_W - 240,
            160
        )

        # sombra
        shadow_rect = rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6

        pygame.draw.rect(
            screen,
            (50, 30, 10),
            shadow_rect,
            border_radius=12
        )

        # fundo
        pygame.draw.rect(
            screen,
            (240, 220, 170),
            rect,
            border_radius=12
        )

        # borda
        pygame.draw.rect(
            screen,
            (120, 80, 40),
            rect,
            5,
            border_radius=12
        )

        # texto
        rendered = font.render(
            self.texto_visivel,
            True,
            (20, 20, 20)
        )

        screen.blit(
            rendered,
            (rect.x + 30, rect.y + 40)
        )

        # continuar
        continue_text = font.render(
            "SPACE",
            True,
            (80, 50, 20)
        )

        screen.blit(
            continue_text,
            (rect.right - 140, rect.bottom - 45)
        )

    # ---------------- UPDATE TEXTO DIÁLOGO ----------------
    def update_dialogo(self):

        full_text = self.dialogo[self.dialogo_index]
        now = pygame.time.get_ticks()

        if now - self.last_update > self.text_speed:

            self.last_update = now

            if self.char_index < len(full_text):

                self.char_index += 1
                self.texto_visivel = full_text[:self.char_index]


class Inimigo:

    def __init__(self, x, y, image):

        self.x = x
        self.y = y

        self.speed = 1

        self.size = 64

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

        self.vida = 100

        self.damage = 1
        self.attack_cooldown = 0
    # ---------------- UPDATE ----------------
    def update(self, player):

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        # EVITAR BUG DIVISÃO
        if distance > 0:

            dx /= distance
            dy /= distance

            self.x += dx * self.speed
            self.y += dy * self.speed

        self.rect.x = self.x
        self.rect.y = self.y

    # ---------------- DRAW ----------------
    def draw(self, screen):

        screen.blit(
            self.image,
            (self.x, self.y)
        )

        # VIDA
        pygame.draw.rect(
            screen,
            (255,0,0),
            (self.x, self.y - 10, 50, 6)
        )

        pygame.draw.rect(
            screen,
            (0,255,0),
            (
                self.x,
                self.y - 10,
                self.vida / 2,
                6
            )
        )

    # ---------------- DANO ----------------
    def attack_player(self, player):

        player_rect = pygame.Rect(
            player.x,
            player.y,
            64,
            64
        )

        if self.attack_cooldown > 0:

            self.attack_cooldown -= 1

        if self.rect.colliderect(player_rect):

            if self.attack_cooldown == 0:

                player.vida -= self.damage

                self.attack_cooldown = 60