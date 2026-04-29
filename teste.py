import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

sprite = pygame.image.load("imagens/Personagem1.png").convert_alpha()

# ---------------- CONFIG DO SPRITE ----------------
FRAME_COLS = 4
FRAME_ROWS = 4

SPRITE_WIDTH = 408
SPRITE_HEIGHT = 611

frame_width = SPRITE_WIDTH // FRAME_COLS
frame_height = SPRITE_HEIGHT // FRAME_ROWS

# ---------------- ESCALA DO PERSONAGEM ----------------
scale = 0.7  # 50% do tamanho original

scaled_width = int(frame_width * scale)
scaled_height = int(frame_height * scale)

# ---------------- POSIÇÃO ----------------
x = 300
y = 300

# ---------------- DIREÇÕES (LINHAS) ----------------
DOWN = 0
LEFT = 2
RIGHT = 3
UP = 1

direction = DOWN

# ---------------- ANIMAÇÃO ----------------
frame_index = 0
frame_timer = 0
frame_speed = 10

running = True

while running:
    clock.tick(60)

    moving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    if key[pygame.K_a]:
        x -= 5
        direction = LEFT
        moving = True

    elif key[pygame.K_d]:
        x += 5
        direction = RIGHT
        moving = True

    elif key[pygame.K_w]:
        y -= 5
        direction = UP
        moving = True

    elif key[pygame.K_s]:
        y += 5
        direction = DOWN
        moving = True

    # ---------------- ANIMAÇÃO ----------------
    if moving:
        frame_timer += 1
        if frame_timer >= frame_speed:
            frame_timer = 0
            frame_index += 1
            if frame_index >= FRAME_COLS:
                frame_index = 0
    else:
        frame_index = 0

    # ---------------- DESENHO ----------------
    screen.fill((255, 255, 255))

    frame = sprite.subsurface(
        (frame_index * frame_width,
         direction * frame_height,
         frame_width,
         frame_height)
    )

    # REDIMENSIONA O FRAME (sem quebrar sprites)
    frame = pygame.transform.smoothscale(frame, (scaled_width, scaled_height))

    screen.blit(frame, (x, y))

    pygame.display.flip()

pygame.quit()