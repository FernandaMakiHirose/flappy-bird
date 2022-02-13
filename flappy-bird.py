# no python console digite: pip install pygame

# biblioteca para criar jogos
import pygame

# biblioteca permite integrar o código com os arquivos do computador
import os

# biblioteca que gera números aleatórios no python
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

# ygame.transform.scale2x() -> aumenta a imagem para a imagem não ficar muito pequena
# pygame.image.load() -> vai pegar uma foto
# os.path.join() -> vai entrar na pasta que tem o arquivo
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

# a imagem do pássaro vai ser uma lista de imagens porque ele vai aparecer com as asas de diferentes ângulos
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

# vai marcar a pontuação
# inicializando a fonte
pygame.font.init()

# é necessário passar a família da fonte e o tamanho
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0

        # pega a primeira imagem do IMGS
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1

        # é a fóruma so sorvetão, a única coisa que vai mudar na fórmula é o número '1.5' podendo ser substituido por outro
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento

        # se o deslocamento for maior que 16 px
        if deslocamento > 16:

            # o deslocamento vai ser 16, porque esse é o limite que o pássado pode se deslocar
            deslocamento = 16
        elif deslocamento < 0:

            # vai fazer o pássaro voar um pouco mais para cima
            deslocamento -= 2

        self.y += deslocamento

        # o ângulo do passaro

        # se a posição y tiver abaixo da altura o pássaro vai começar a ficar inclinado e a cair
        if deslocamento < 0 or self.y < (self.altura + 50):

            # se o pássaro não estiver virado para cima
            if self.angulo < self.ROTACAO_MAXIMA:

                # vai colocar ele virado pra cima
                self.angulo = self.ROTACAO_MAXIMA
        else:

            # se o ângulo do pássaro for maior que -90
            if self.angulo > -90:

                # ele vai ser rotacionado para baixo
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar

        # vai mudar a imagem quando a contagem da imagem passar do tempo de animação
        self.contagem_imagem += 1

        # se a contagem for menor que o tempo de animação
        if self.contagem_imagem < self.TEMPO_ANIMACAO:

            # vai mostrar a primeira imagem
            self.imagem = self.IMGS[0]

        # se a contagem for menor que o tempo de animação * 2
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:

            # vai mostrar a segunda imagem
            self.imagem = self.IMGS[1]

        # se a contagem for menor que o tempo de animação * 3
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:

            # vai mostrar a terceira imagem
            self.imagem = self.IMGS[2]

        # se a contagem for menor que o tempo de animação * 4
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:

            # vai mostrar a segunda imagem
            self.imagem = self.IMGS[1]

        # se a contagem for menor que o tempo de animação * 4 + 1
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:

            # vai mostrar a primeira imagem
            self.imagem = self.IMGS[0]

            # e vai zerar a contagem e começa a fazer esse processo desde o início
            self.contagem_imagem = 0


        # se o passaro tiver caindo eu não vou bater asa
        if self.angulo <= -80:

            # vai mostrar a segunda imagem
            self.imagem = self.IMGS[1]

            # a próxima batida de asa dele vai ser uma batida para baixo
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem rotacionada
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)

        # vai desenhar um retângulo em volta da imagem e vai colar na tela

        # desenhando o centro da imagem
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center

        # retângulo da imagem
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)

        # vai desenhar na tela a imagem na posição do topo a esquerda
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # vai pegar a máscara do python para futuramente ver se o pássaro colidiu em alguma superfície
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    # a distância entre um cano e outro
    DISTANCIA = 250

    # velocidade do cano
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0

        # a imagem do cano do topo é apenas a imagem do cano porém de ponta cabeça
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)

        # a imagem do cano da base é apenas a imagem do cano
        self.CANO_BASE = IMAGEM_CANO

        # se passou vai ficar True
        self.passou = False

        # essa função vai gerar o valor que vai ser a altura do cano
        self.definir_altura()

    def definir_altura(self):
        # gerando um valor aleatório para a altura com valores específicos para os canos não ficarem com uma distância muito longa
        self.altura = random.randrange(50, 450)

        # a posição topo é para cima
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()

        # a posição base é para baixo
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        # o cano se movimenta para o lado, então precisa tirar um valor da posição 'x' dele
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        # o .blit desenha o cano, desenhando o cano de cima e o cano de baixo
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        # verificando qual pássaro vai colidir
        passaro_mask = passaro.get_mask()

        # pegando a máscara do topo e da base
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        # para verificar se tem colisão é necessário pegar a distância do topo e da base
        # pegando a distância do eixo x e do eixo y e é necessário arredondar os números para serem números inteiros
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # agora é só verificar se colidiu, o overlap verifica o ponto de colisão, ele verifica se existe 2 pixels iguais
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        # se um desses for verdadeiro é porque teve colisão, caso contrário não teve colisão
        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width() # pegando a largura do chão
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        # x1 = chão 1, x2 = chão 2
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        # se sair da tela 1 vai adicionar outro chão ao lado do primeiro chão
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA

        # se sair da tela 2 vai adicionar outro chão ao lado do segundo chão
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        # vai desenhar o chão
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

# função que vai desenhar o jogo
def desenhar_tela(tela, passaros, canos, chao, pontos):

    # desenhando o fundo da tela na posição 0
    tela.blit(IMAGEM_BACKGROUND, (0, 0))

    # para cada pássaro na lista de pássaros
    for passaro in passaros:

        # vai desenhar o pássaro na tela
        passaro.desenhar(tela)

    # para cada cano em canos
    for cano in canos:

        # vai desenhar o cano na tela
        cano.desenhar(tela)

    # colocando o texto dentro da tela com um texto branco
    texto = FONTE_PONTOS.render(f"{pontos}", 1, (255, 255, 255))

    # desenhando o texto no canto superior da tela
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    # vai desenhar o chão
    chao.desenhar(tela)

    # vai atualizar a tela
    pygame.display.update()

# função que vai executar o jogo (função principal)
def main():

    # passando os valores que irão aparecer na tela
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0

    # ele vai atualizar a tela
    relogio = pygame.time.Clock()

    # o jogo é um loop infinito, enquanto o jogo estiver rodando ele vai ser executado
    rodando = True
    while rodando:

        # ele vai atualizar 30 frames por segundo
        relogio.tick(30)

        # interação com o usuário
        # vai pegar a lista de eventos
        for evento in pygame.event.get():

            # se fechar a tela vai sair do jogo
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            # se apertar a barra de espaço vai pular
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # mover o pássaro e o chão
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        # variável auxiliar por padrão sendo falsa
        adicionar_cano = False
        remover_canos = []
        # para cada cano vai verificar se o cano bateu no pássaro
        for cano in canos:
            for i, passaro in enumerate(passaros):
                # se o cano bateu com o pássaro vai retirar o pássaro da lista
                if cano.colidir(passaro):
                    passaros.pop(i)

                # se o pássaro passou do cano e se o 'x' do pássaro for maior que o 'x' do cano
                if not cano.passou and passaro.x > cano.x:

                    # significa que o pássaro passou
                    cano.passou = True
                    adicionar_cano = True

            # movimentando o cano
            cano.mover()

            # se o cano já saiu da tela
            if cano.x + cano.CANO_TOPO.get_width() < 0:

                # vai adicionar ele na lista de remover os canos
                remover_canos.append(cano)

# não removemos o cano direto, porque se for remover um cano enquanto percorre a lista de canos pode dar um problema

        # o usuário vai ganhar um ponto se adicionar_cano for verdadeiro
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        # para cada canos em remover_canos vai remover o cano
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):

            # se a posição do eixo y do pássado + altura do pássaro for maior do que a posição do chão
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:

                # vai excluir o pássaro que estiver na posição i
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

# se é um arquivo que vai ser executado manualmente vai rodar o que estiver dentro, caso contrário não vai rodar o que estiver dentro
if __name__ == '__main__':
    main()
