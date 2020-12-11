import pygame
from random import randint

pygame.init()

resolucao = (500, 500)
screen = pygame.display.set_mode(resolucao)

clock = pygame.time.Clock()

color_bg = (0, 68, 83)



class Snake:
    cor = (255, 255, 255)
    tamanho = (10, 10)
    velocidade = 10

    def __init__(self):
        self.textura = pygame.Surface(self.tamanho)
        self.textura.fill(self.cor)

        self.corpo = [(100, 100), (90, 100), (80, 100)]  # vai cresenco a medida q come a fruta. Melhor aplicação -> estrutura de dados lista
        self.direcao = "direita"

    def blit(self, screen):
        for posicao in self.corpo:
            screen.blit(self.textura, posicao)

    def andar(self):
        cabeca = self.corpo[0]
        x = cabeca[0]
        y = cabeca[1]

        if self.direcao == "direita":
            self.corpo.insert(0, (x + self.velocidade, y))  # Atualiza a posição da cabeça para a direita
        elif self.direcao == "esquerda":
            self.corpo.insert(0, (x - self.velocidade, y))  # Atualiza a posição da cabeça para a esquerda
        elif self.direcao == "cima":
            self.corpo.insert(0, (x, y - self.velocidade))  # Atualiza a posição da cabeça para a cima(y cresce de cima para baixo)
        elif self.direcao == "baixo":
            self.corpo.insert(0, (x, y + self.velocidade))  # Atualiza a posição da cabeça para a direita

        self.corpo.pop(-1)

    def cima(self):
        if self.direcao is not "baixo":
            self.direcao = "cima"

    def baixo(self):
        if self.direcao is not "cima":
            self.direcao = "baixo"

    def esquerda(self):
        if self.direcao is not "direita":
            self.direcao = "esquerda"

    def direita(self):
        if self.direcao is not "esquerda":
            self.direcao = "direita"

    def colisao_fruta(self, fruta):
        return self.corpo[0] == fruta.posicao

    def comer(self, fruta):
        self.corpo.append((0, 0))   # coloca qualqer posição, ja que sera removido na lógica do corpo e acrescido na cabeça

    def colisao_parede(self):
        cabeca = self.corpo[0]
        x = cabeca[0]
        y = cabeca[1]

        return x < 0 or y < 0 or x > 490 or y > 490


class Fruta:
    cor = (255, 0, 0)
    tamanho = (10, 10)  # tamanho da nossa frutinha

    def __init__(self):  # Iniciar a fruta
        self.textura = pygame.Surface(self.tamanho)
        self.textura.fill(self.cor)
        cordenada_x = randint(0, 49) * 10  # garantir que sempre seja multipla de 10
        cordenada_y = randint(0, 49) * 10
        self.posicao = (cordenada_x, cordenada_y)

    def blit(self, screen):
        screen.blit(self.textura, self.posicao)


fruta = Fruta()
snake = Snake()

while True:
    clock.tick(10)
    print(clock.get_fps())

    for event in pygame.event.get():  # pegas os eventos que estão ocorrendo
        if event.type == pygame.QUIT:
            exit()  # sair do jogo

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.cima()
                break
            elif event.key == pygame.K_DOWN:
                snake.baixo()
                break
            elif event.key == pygame.K_LEFT:
                snake.esquerda()
                break
            elif event.key == pygame.K_RIGHT:
                snake.direita()
                break


    if snake.colisao_fruta(fruta):
        snake.comer(fruta)
        fruta = Fruta() # Ao comer, cria uma nova fruta (nova instancia do objeto)

    if snake.colisao_parede():
        snake = Snake()

    snake.andar()

    screen.fill(color_bg)
    fruta.blit(screen)
    snake.blit(screen)


    pygame.display.update()
