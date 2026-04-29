import pygame
import random
import math

pygame.init()

# ======================
# SCREEN
# ======================
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# ======================
# WORLD SETTINGS
# ======================
TILE = 30  # pequeno = mais detalhe (menos “quadrado” visível)

# ======================
# NOISE (terrain base)
# ======================
def noise(x, y):
    return (math.sin(x * 127.1 + y * 311.7) * 43758.5453) % 1

def smooth_noise(x, y):
    corners = (noise(x-1,y-1)+noise(x+1,y-1)+noise(x-1,y+1)+noise(x+1,y+1))/16
    sides   = (noise(x-1,y)+noise(x+1,y)+noise(x,y-1)+noise(x,y+1))/8
    center  = noise(x,y)/4
    return corners + sides + center

def fbm(x, y):
    total = 0
    amp = 1
    freq = 0.01

    for _ in range(4):
        total += smooth_noise(x*freq, y*freq) * amp
        amp *= 0.5
        freq *= 2

    return total

# ======================
# BIOMES
# ======================
def get_biome(h):
    if h < 0.3:
        return "water"
    elif h < 0.4:
        return "sand"
    elif h < 0.65:
        return "grass"
    elif h < 0.8:
        return "forest"
    else:
        return "mountain"

# ======================
# COLORS (base terrain)
# ======================
def biome_color(b):
    return {
        "water": (40, 90, 200),
        "sand": (210, 200, 140),
        "grass": (70, 180, 90),
        "forest": (30, 120, 50),
        "mountain": (120, 120, 120)
    }[b]

# ======================
# PLAYER + CAMERA
# ======================
px, py = 0, 0
cam_x, cam_y = 0, 0

def update_camera():
    global cam_x, cam_y
    cam_x = px - W//2
    cam_y = py - H//2

# ======================
# OBJECT PLACEMENT (trees/rocks)
# ======================
def place_detail(x, y, biome):
    seed = x * 928371 + y * 1237
    random.seed(seed)

    r = random.random()

    if biome == "forest" and r < 0.25:
        return "tree"
    if biome == "mountain" and r < 0.2:
        return "rock"
    if biome == "grass" and r < 0.05:
        return "bush"

    return None

# ======================
# RIVERS (curved flow)
# ======================
def river(x, y):
    n = noise(x*0.02, y*0.02)
    return abs(n - 0.5) < 0.03

# ======================
# DRAW WORLD
# ======================
def draw_world():
    start_x = cam_x // TILE
    start_y = cam_y // TILE

    end_x = start_x + W // TILE + 2
    end_y = start_y + H // TILE + 2

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):

            h = fbm(x, y)
            biome = get_biome(h)

            sx = x*TILE - cam_x
            sy = y*TILE - cam_y

            # 🌊 river override (natural curved water)
            if river(x, y):
                color = (50, 120, 220)
            else:
                color = biome_color(biome)

            pygame.draw.rect(screen, color, (sx, sy, TILE+1, TILE+1))

            # ======================
            # DETAILS (not blocks)
            # ======================
            obj = place_detail(x, y, biome)

            if obj == "tree":
                pygame.draw.circle(screen, (20, 90, 20), (sx+5, sy+5), 4)
            elif obj == "rock":
                pygame.draw.circle(screen, (90, 90, 90), (sx+5, sy+5), 3)
            elif obj == "bush":
                pygame.draw.circle(screen, (40, 160, 60), (sx+5, sy+5), 3)

# ======================
# MOVE
# ======================
def move():
    global px, py

    keys = pygame.key.get_pressed()
    speed = 3

    if keys[pygame.K_LEFT]:
        px -= speed
    if keys[pygame.K_RIGHT]:
        px += speed
    if keys[pygame.K_UP]:
        py -= speed
    if keys[pygame.K_DOWN]:
        py += speed

# ======================
# LOOP
# ======================
running = True

while running:
    screen.fill((0,0,0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    move()
    update_camera()
    draw_world()

    # player
    pygame.draw.circle(screen, (255,255,255), (W//2, H//2), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()