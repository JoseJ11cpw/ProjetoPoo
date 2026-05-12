import pygame

pygame.init()

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def follow(self, target):
        # centraliza a câmera no jogador
        self.offset.x = target.rect.centerx - self.width // 2
        self.offset.y = target.rect.centery - self.height // 2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
screen=pygame.display.set_mode((1920,1080))
running=True
camera = Camera(800, 600)
player = Player(100, 100)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        camera.follow(player)

        screen.fill((30, 30, 30))

        # desenha o player com offset da câmera
        screen.blit(player.image, player.rect.topleft - camera.offset)

        pygame.display.update()