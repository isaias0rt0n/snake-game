import pygame
from random import randint


class Snake:
    cor = (255, 255, 255)
    tamanho = (10, 10)
    velocidade = 10
    tamanho_max = 49 * 49 # tamanho maximo da cobra (faz a verificação dessa condição na funcao colisao)

    def __init__(self):
        self.textura = pygame.Surface(self.tamanho)
        self.textura.fill(self.cor)

        self.corpo = [(100, 100), (90, 100), (80, 100)]  # vai cresenco a medida q come a fruta. Melhor aplicação -> estrutura de dados lista
        self.direcao = "direita"

        self.pontos = 0
        self.nivel_vel = 10  # velocidade incial da cobrinha

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
        self.corpo.append((0, 0))  # coloca qualqer posição, ja que sera removido na lógica do corpo e acrescido na cabeça
        self.pontos += 1  # ao comer fruta, soma um ponto
        self.nivel_vel += 5  # ao comer, aumenta a velocidade da cobra
        pygame.display.set_caption("Snake | Pontos: {}".format(self.pontos))

    def colisao_parede(self):
        cabeca = self.corpo[0]
        x = cabeca[0]
        y = cabeca[1]

        return x < 0 or y < 0 or x > 490 or y > 490 or len(self.corpo) > self.tamanho_max

    def auto_colisao(self):
        return self.corpo[0] in self.corpo[1:]  # verifica se a posição da cabeça da cobra é a mesma de alguma parte do corpo

    def nivel(self):
        return self.nivel_vel


class Fruta:
    cor = (255, 0, 0)
    tamanho = (10, 10)  # tamanho da nossa frutinha

    def __init__(self, snake):  # Iniciar a fruta
        self.textura = pygame.Surface(self.tamanho)
        self.textura.fill(self.cor)

        self.posicao = Fruta.criar_posicao(snake)

    @staticmethod
    def criar_posicao(snake):
        x = randint(0, 49) * 10  # garantir que sempre seja multipla de 10
        y = randint(0, 49) * 10

        if (x, y) in snake.corpo:   # garantir a fruta de não nascer no espaço em que a cobra está
            Fruta.criar_posicao(snake)
        else:
            return x, y

    def blit(self, screen):
        screen.blit(self.textura, self.posicao)


if __name__ == "__main__":

    pygame.init()

    resolucao = (500, 500)
    screen = pygame.display.set_mode(resolucao)

    pygame.display.set_caption("Snake Gaming 🐍")

    clock = pygame.time.Clock()

    color_bg = (0, 68, 83)

    snake = Snake()
    fruta = Fruta(snake)

    while True:
        clock.tick(snake.nivel_vel)
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
            fruta = Fruta(snake)  # Ao comer, cria uma nova fruta (nova instancia do objeto)

        if snake.colisao_parede() or snake.auto_colisao():
            snake = Snake()

        snake.andar()

        screen.fill(color_bg)
        fruta.blit(screen)
        snake.blit(screen)

        pygame.display.update()