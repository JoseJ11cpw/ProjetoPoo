import pygame

def cortar_sprites(sheet, largura, altura):
    sprites = []
    for y in range(0, sheet.get_height() - altura + 1, altura):
        for x in range(0, sheet.get_width() - largura + 1, largura):
            rect = pygame.Rect(x, y, largura, altura)
            sprites.append(sheet.subsurface(rect))
    return sprites

class Jogador:
    def __init__(self, x, y):
        self.sprite_sheet = pygame.image.load("imagens/Personagem1.png").convert_alpha()
        self.frames = cortar_sprites(self.sprite_sheet, 102, 152)
        self.frame_atual = 0
        self.timer_animacao = 0

        self.x = x
        self.y = y
        self.tamanho = 40
        self.cor = (255, 0, 0)
        self.velocidade = 10
        self.vida = 100

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.velocidade
        if keys[pygame.K_s]:
            self.y += self.velocidade
        if keys[pygame.K_a]:
            self.x -= self.velocidade
        if keys[pygame.K_d]:
            self.x += self.velocidade

    def draw(self, screen):
        frame = self.frames[self.frame_atual]
        screen.blit(frame, (self.x, self.y))

    def animar(self):
        self.timer_animacao += 1

        if self.timer_animacao >= 10:
            self.frame_atual += 1
            self.timer_animacao = 0

        if self.frame_atual >= len(self.frames):
            self.frame_atual = 0



class Inimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamanho = 70
        self.cor = (0, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.cor, (self.x, self.y, self.tamanho, self.tamanho))