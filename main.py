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


def check_movement():
    """
    se o usuário clicar em uma peça e for uma peça que pode se mover,
    começamos a rotina de preencher com 'x' as posições de movimento e
    colorir essas posições com um retângulo cinza
    """

    mouse_pos = pygame.mouse.get_pos()
    clicked_block = target_piece(pygame.mouse.get_pos())
    do_the_move = False

    # caso o tabuleiro esteja marcado com possíveis movimentos,
    # a variável "faça o movimento" se torna true
    for i in range(8):
        if "x" in board[i]:
            print(board)
            do_the_move = True
            break

    # isso significa que esse click é apenas para gerar os caminhos
    # que a peça pode percorrer e colorir eles
    if do_the_move == False:
        movements = player_moves(clicked_block)

        if movements != []:
            mark_user_move(movements)
            draw_rectangle(movements)

    # o caminho que foi clicado deve ser checado, esse bloco possui
    # um 'x' indicando que a peça pode se mover para lá?!
    else:
        pass


def mark_user_move(movements):
    """
    marca com 'x' onde o usuário pode clicar após selecionar a peça
    """

    for i in range(len(movements)):
        row = movements[i][0]
        col = movements[i][1]

        board[row][col] = "x"


# TODO: movimentos para o jogar vermelho (2)
def player_moves(block_addr):
    """
    verifica se a peça que foi clicada pelo jogador possui movimentos
    válidos, caso haja, a função retorna uma lista com as ações válidas
    """

    movements = []

    # caso o usuário clique em um espaço vazio
    pos = (block_addr[0], block_addr[1])
    if board[pos[0]][pos[1]] == 0:
        return movements

    up_r = (block_addr[0] + 1, block_addr[1] - 1)
    down_r = (block_addr[0] + 1, block_addr[1] + 1)

    # verifica se o movimento na diagonal pra cima é válido
    if (up_r[0] >= 0 and up_r[0] <= 7) and (up_r[1] >= 0 and up_r[1] <= 7):
        # esquerda -> direita
        if board[up_r[0]][up_r[1]] == 0:
            movements.append(up_r)

    # diagonal pra baixo
    if (down_r[0] >= 0 and down_r[0] <= 7) and (
        down_r[1] >= 0 and down_r[1] <= 7
    ):
        if board[down_r[0]][down_r[1]] == 0:
            movements.append(down_r)

    return movements


def draw_rectangle(valid_moves):
    """
    desenha um retângulo cinza na peça clicada e nos blocos
    para onde ela pode se mover
    """

    mouse_pos = pygame.mouse.get_pos()
    block_addr = target_piece(mouse_pos)

    center = (block_addr[0] * square_height, block_addr[1] * square_width)

    gray_rectangle = pygame.Rect(
        center[0],
        center[1],
        square_height,
        square_width,
    )

    color = (100, 100, 100)

    # desenha um retângulo cinza na peça que vai se mover
    pygame.draw.rect(screen, color, gray_rectangle, 4)

    # pega o endereço de onde as peças podem ir e as colore com
    # retângulo cinza
    for i in valid_moves:
        gray_rectangle[0] = i[0] * square_height
        gray_rectangle[1] = i[1] * square_width
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


def circle_color(i, j):
    """
    função de suporte ao draw_circle,
    ela define a cor do círculo a ser desenhado
    """

    color = ()

    if board[i][j] == 0:
        return

    if board[i][j] == 1:
        color = (255, 0, 0)

    elif board[i][j] == 2:
        color = (0, 0, 255)

    return color


def draw_circle():

    for i in range(8):
        for j in range(8):
            # como essa função fica no loop principal, quando o usuário
            # vai se mover aquela posição válida na board fica marcada
            # com 'x', isso serve para não desenhar
            if board[i][j] == "x":
                continue

            target = board[i][j]
            if target == 1 or target == 2:
                color = circle_color(i, j)
                # o círculo precisa iniciar no centro do quadrado
                center = (square_height * i, square_width * j)
                center = (
                    center[0] + (square_height / 2),
                    center[1] + (square_width / 2),
                )

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


create_board()
draw_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            check_movement()

    draw_circle()
    pygame.display.flip()

    clock.tick(60)

pygame.quit
