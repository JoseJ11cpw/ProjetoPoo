import pygame
from Personagens import Jogador,Inimigo

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

Personagem1 = Jogador(100, 100)
Inimigo1 = Inimigo(300,300)

sprite_arvore = pygame.image.load("imagens/arvore.png").convert_alpha()
sprite_arvore = pygame.transform.scale(sprite_arvore, (235, 254))

running = True

while running:
    screen.fill((255,255,255))

    keys = pygame.key.get_pressed()
    Personagem1.move(keys)
    Personagem1.animar()
    Personagem1.draw(screen)
    Inimigo1.draw(screen)
    screen.blit(sprite_arvore, (500, 200))
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20))  # fundo vermelho
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, Personagem1.vida * 2, 20))  # vida verde

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if abs(Personagem1.x - Inimigo1.x) < 40 and abs(Personagem1.y - Inimigo1.y) < 40:
            Personagem1.vida -= 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()