import pygame


class Inventario:

    def __init__(self):

        self.aberto = False

        self.itens = {} 

    # ---------------- TOGGLE ----------------
    def toggle(self):

        self.aberto = not self.aberto

    # ---------------- DRAW ----------------
    def draw(self, screen, font, SCREEN_W, SCREEN_H):

        # FUNDO
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

        # TÍTULO
        title = font.render(
            "INVENTÁRIO",
            True,
            (20,20,20)
        )

        screen.blit(
            title,
            (rect.x + 20, rect.y + 20)
        )

        # ITENS
        y = rect.y + 80

        for item, quantidade in self.itens.items():

            text = font.render(
                f"{item}  x{quantidade}",
                True,
                (20,20,20)
            )

            screen.blit(text, (rect.x + 40, y))

            y += 50

    def add_item(self, nome):

        if nome in self.itens:

             self.itens[nome] += 1

        else:

            self.itens[nome] = 1





class Item:
        
    def __init__(self, x, y, image, nome, size=30):
        self.x = x
        self.y = y

        self.nome = nome

        self.size = size

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

        self.apanhado = False

        # ---------------- DRAW ----------------
    def draw(self, screen):

        if not self.apanhado:

            screen.blit(self.image,(self.x, self.y))

        # ---------------- DISTÂNCIA ----------------
    def near_player(self, player):

        player_rect = pygame.Rect(player.x, player.y, 64, 64 )

        return self.rect.colliderect(player_rect.inflate(40, 40))