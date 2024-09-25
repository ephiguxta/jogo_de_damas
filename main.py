#!/usr/bin/env python

import pygame

pygame.init()

height = 640
width = 480

screen = pygame.display.set_mode((height, width))

# cada posição da mesa possui um tamanho fixo, o tabuleiro
# é composto por 8x8 posições
square_height = height / 8
square_width = width / 8

clock = pygame.time.Clock()

running = True

mouse_pos = 0

board = []


def draw_rectangle():
    """
    após o evento do clique acontecer, checa se o usuário clicou em
    uma peça válida
    """

    mouse_pos = pygame.mouse.get_pos()
    block_addr = target_piece(mouse_pos)

    # pega o valor referente a aquela posição do tabuleiro, é 0, 1 ou 2?
    addr = board[block_addr[0]][block_addr[1]]
    if addr != 0:
        center = (block_addr[0] * square_height, block_addr[1] * square_width)

        gray_rectangle = pygame.Rect(
                center[0],
                center[1],
                square_height,
                square_width,
        )

        color = (100, 100, 100)
        pygame.draw.rect(screen, color, gray_rectangle, 4)

def target_piece(mouse_pos):
    """
    pega o quadrado do tabuleiro que o usuário clicou
    e retorna em formato de tupla
    """

    # os valores vão de 1 a 8
    for i in range(1, 9):
        for j in range(1, 9):
            last_x = i * square_height
            last_y = j * square_width

            # verifica o intervalo do tamanho de square_* e "decodifica" onde o
            # usuário clicou
            if (
                mouse_pos[0] <= last_x
                and mouse_pos[0] >= last_x - square_height
            ) and (
                mouse_pos[1] <= last_y
                and mouse_pos[1] >= last_y - square_height
            ):
                # o -1 serve para mostrar o valor real, pois o índice começa
                # em zero
                block = (i - 1, j - 1)
                return block

    return None


def draw_circle(i, j, center):
    color = 0

    if board[i][j] == 0:
        return

    if board[i][j] == 1:
        color = (255, 0, 0)

    elif board[i][j] == 2:
        color = (0, 0, 255)

    # o círculo precisa iniciar no centro do quadrado
    center = (center[0] + (square_height / 2), center[1] + (square_width / 2))

    pygame.draw.circle(screen, color, center, 20)


def block_color(i, j):
    """
    retorna a cor do bloco correspondente a seu endereço,
    por exemplo se ele for um block de posição de movimento
    válido, ele colore de verde.
    """

    color = 0
    if ((i + j) % 2) == 0:
        color = (255, 255, 255)
        return color

    color = (0, 0, 0)
    return color


def create_board():
    # cria as 8x8 posições do tabuleiro preenchidas com zero
    for i in range(8):
        list = [0] * 8
        board.append(list)

    # armazena o endereço da primeira peça da linha
    first_piece_addr = 0

    # as peças vermelhas começam pela linha 6 e 7
    red_pos = 6
    # posição das peças azuis e vermelhas
    for i in range(2):
        if i == 0:
            first_piece_addr = 1
        elif i == 1:
            first_piece_addr = 0
            red_pos += 1

        # o jogador 1 vai possuir valor 1 de representação
        # na matriz
        for j in range(first_piece_addr, 8, 2):
            board[i][j] = 1
            board[red_pos][j] = 2


def draw_board():
    # desenha todas os 64 quadrados que representam
    # as posições da mesa

    for i in range(0, 8):
        for j in range(0, 8):
            color = block_color(i, j)

            # FIXME: esse trecho até o pygame.draw.rect() pode ser
            # transformado em uma função
            center = (square_height * i, square_width * j)

            actual_block = pygame.Rect(
                center[0],
                center[1],
                square_height,
                square_width,
            )

            pygame.draw.rect(screen, color, actual_block)
            draw_circle(i, j, center)


create_board()
draw_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_rectangle()

    pygame.display.flip()
    clock.tick(60)

pygame.quit
