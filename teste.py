import pygame
import pytmx

def carregar_mapa(mapa):
    tmx_data = pytmx.load_pygame(mapa)
    paredes = []
    
    # Percorre todos os objetos da camada que você criou no Tiled
    for obj in tmx_data.objects:
        if obj.name == "wall": # Ou o nome que você deu à camada/objeto
            paredes.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    return tmx_data, paredes

def desenhar_mapa(screen, tmx_data):
    # Percorre todas as camadas de tiles do mapa
    for camada in tmx_data.visible_layers:
        # Verifica se é uma camada de tiles (existem camadas de objetos também)
        if isinstance(camada, pytmx.TiledTileLayer):
            for x, y, gid in camada:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Multiplica x e y pelo tamanho do tile (ex: 32x32)
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

def desenhar_colisoes(screen, paredes):
    for parede in paredes:
        pygame.draw.rect(screen, (255, 0, 0), parede, 2) # O '2' é a espessura da linha
class Jogador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocidade = 5

    def mover(self, dx, dy, paredes):
        # Move no eixo X
        self.rect.x += dx
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dx > 0: # Indo para direita
                    self.rect.right = parede.left
                if dx < 0: # Indo para esquerda
                    self.rect.left = parede.right

        # Move no eixo Y
        self.rect.y += dy
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dy > 0: # Caindo/Indo para baixo
                    self.rect.bottom = parede.top
                if dy < 0: # Pulando/Indo para cima
                    self.rect.top = parede.bottom

# 1. SETUP
pygame.init()
screen = pygame.display.set_mode((800, 600))
mapa_data, lista_paredes = carregar_mapa("mapa.tmx")

rodando = True
while rodando:

    # 2. EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # 3. LÓGICA (Movimentação do jogador com colisão aqui)

    # 4. RENDERIZAÇÃO
    screen.fill((0, 0, 0)) # Limpa a tela
    
    desenhar_mapa(screen, mapa_data)     # Desenha o chão/paredes
    desenhar_colisoes(screen, lista_paredes) # Desenha as caixas vermelhas (opcional)
    
    # Desenhe o seu jogador aqui embaixo
    # screen.blit(jogador.image, jogador.rect)

    pygame.display.flip() # Atualiza a tela