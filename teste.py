import pygame

pygame.init()

screen=pygame.display.set_mode((800,600))
Personagem1=pygame.image.load("imagens/Personagem1.png")
arvore = pygame.image.load("imagens/arvore.png").convert_alpha()
arvore = pygame.transform.scale(arvore, (235, 254))

clock = pygame.time.Clock()

running = True
x=300
y=450

FRONT=0
BACK=152
LEFT=152*2
RIGHT=152*3

flp=True
x_sprite = 6
y_sprite = 25
direcao = FRONT
animacao=0
while running:
    key=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if key[pygame.K_a]:
        x -= 5
        direcao = LEFT
        animacao=113
    elif key[pygame.K_d]:
        x += 5
        direcao = RIGHT
    elif key[pygame.K_w]:
        y-=5
        direcao=BACK
    elif key[pygame.K_s]:
        y+=5
        direcao=FRONT
    else:
        direcao=FRONT
    screen.fill((255,255,255))
    screen.blit(Personagem1,(x,y), (x_sprite+animacao,y_sprite+direcao,89,115))
    for i in range(4):
        screen.blit(arvore, (0, 0 + i * 120))
    animacao=0
    pygame.display.flip()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()