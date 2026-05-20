import pygame


class Inventario:

    def __init__(self):

        self.aberto = False

        self.itens = []

    # ---------------- TOGGLE ----------------
    def toggle(self):

        self.aberto = not self.aberto

    # ---------------- ADD ITEM ----------------
    def add_item(self, item):

        self.itens.append(item)

    # ---------------- DRAW ----------------
    def draw(self, screen, font, SCREEN_W, SCREEN_H):

        # ---------------- FUNDO ----------------
        rect = pygame.Rect(
            SCREEN_W // 2 - 300,
            SCREEN_H // 2 - 200,
            600,
            400
        )

        pygame.draw.rect(
            screen,
            (220, 200, 160),
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (80, 50, 20),
            rect,
            5,
            border_radius=12
        )

        # ---------------- TÍTULO ----------------
        title = font.render(
            "INVENTÁRIO",
            True,
            (20,20,20)
        )

        screen.blit(
            title,
            (rect.x + 20, rect.y + 20)
        )

        # ---------------- ITENS ----------------
        y = rect.y + 90

        for item in self.itens:

            # IMG MAIOR SÓ NO INVENTÁRIO
            inventory_img = pygame.transform.scale(
                item.image,
                (110, 110) #mexer no tamanho das img no inventario
            )

            # DESENHAR IMG
            screen.blit(
                inventory_img,
                (rect.x + 20, y-25)
            )

            # NOME
            text = font.render(
                item.nome,
                True,
                (20,20,20)
            )

            screen.blit(
                text,
                (rect.x + 130, y + 15)
            )

            y += 80


class Item:

    def __init__(
        self,
        x,
        y,
        image,
        nome,
        size=40
    ):

        self.x = x
        self.y = y

        self.nome = nome

        self.size = size

        # ---------------- IMAGEM ORIGINAL ----------------
        original_image = pygame.image.load(
            image
        ).convert_alpha()

        # IMG DO CHÃO
        self.image = pygame.transform.scale(
            original_image,
            (self.size, self.size)
        )

        # RECT
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

        self.apanhado = False

    # ---------------- DRAW ----------------
    def draw(self, screen):

        if not self.apanhado:

            screen.blit(
                self.image,
                (self.x, self.y)
            )

    # ---------------- DISTÂNCIA ----------------
    def near_player(self, player):

        player_rect = pygame.Rect(
            player.x,
            player.y,
            64,
            64
        )

        return self.rect.colliderect(
            player_rect.inflate(40, 40)
        )