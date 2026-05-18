import pygame

class NPC:

    def __init__(self, x, y, image):

        self.x = x
        self.y = y

        # TAMANHO NPC
        self.largura = 50
        self.altura = 30

        # imagem
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (self.largura, self.altura)
        )

        # HITBOX BASE
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

        # ÁREA DE INTERAÇÃO (MAIOR)
        self.interaction_rect = self.rect.inflate(80, 80)

        # DIALOGO
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

    # ---------------- UPDATE (IMPORTANTE) ----------------
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        self.interaction_rect = self.rect.inflate(10, 10)

    # ---------------- DRAW NPC ----------------
    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))

    # ---------------- PLAYER DISTANCE ----------------
    def near_player(self, player):

        player_rect = pygame.Rect(
            player.x,
            player.y,
            64,
            64
        )

        return self.interaction_rect.colliderect(player_rect)

    # ---------------- DRAW DIALOG ----------------
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

        pygame.draw.rect(screen, (50, 30, 10), shadow_rect, border_radius=12)

        # fundo
        pygame.draw.rect(screen, (240, 220, 170), rect, border_radius=12)

        # borda
        pygame.draw.rect(screen, (120, 80, 40), rect, 5, border_radius=12)

        # texto
        rendered = font.render(
            self.texto_visivel,
            True,
            (20, 20, 20)
        )

        screen.blit(rendered, (rect.x + 30, rect.y + 40))

        # continuar
        continue_text = font.render("SPACE", True, (80, 50, 20))

        screen.blit(
            continue_text,
            (rect.right - 140, rect.bottom - 45)
        )

    # ---------------- UPDATE DIALOG ----------------
    def update_dialogo(self):

        full_text = self.dialogo[self.dialogo_index]
        now = pygame.time.get_ticks()

        if now - self.last_update > self.text_speed:
            self.last_update = now

            if self.char_index < len(full_text):
                self.char_index += 1
                self.texto_visivel = full_text[:self.char_index]