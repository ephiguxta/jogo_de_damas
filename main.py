#!/usr/bin/env python

import pygame

pygame.init()

height = 640
width = 480

player = 1

screen = pygame.display.set_mode((height, width))

# cada posição da mesa possui um tamanho fixo, o tabuleiro
# é composto por 8x8 posições
square_height = height / 8
square_width = width / 8

clock = pygame.time.Clock()

running = True

mouse_pos = 0

board = []


def remove_movement_junk():
    for i in range(8):
        for j in range(8):
            if board[i][j] == "x":
                board[i][j] = 0


def move_piece_to_block(piece_to_move_addr, clicked_block):
    global player

    # limpa a figura da peça que vai ser movida
    i, j = piece_to_move_addr
    # salva qual é a peça, 1 ou 2?
    tag = board[i][j]
    board[i][j] = 0

    # limpa os 'x' da board
    remove_movement_junk()

    i, j = clicked_block

    if tag == "a":
        board[i][j] = 1
    elif tag == "b":
        board[i][j] = 2

    draw_rectangle(None)

    # vai mudando a variável global para que cada player
    # tenha a sua jogada
    if player == 1:
        player = 2
    else:
        player = 1


def find_piece_addr():
    global player

    tag = 0
    if player == 1:
        tag = "a"
    else:
        tag = "b"

    for i in range(8):
        if tag in board[i]:
            return (i, board[i].index(tag))


def check_movement():
    """
    se o usuário clicar em uma peça e for uma peça que pode se mover,
    começamos a rotina de preencher com 'x' as posições de movimento e
    colorir essas posições com um retângulo cinza
    """

    global player

    mouse_pos = pygame.mouse.get_pos()
    clicked_block = target_piece(pygame.mouse.get_pos())
    do_the_move = False

    piece = board[clicked_block[0]][clicked_block[1]]
    if player == 1 and piece == 2:
        return
    elif player == 2 and piece == 1:
        return

    # caso o tabuleiro esteja marcado com possíveis movimentos,
    # a variável "faça o movimento" se torna true
    for i in range(8):
        if "x" in board[i]:
            do_the_move = True
            break

    # isso significa que esse click é apenas para gerar os caminhos
    # que a peça pode percorrer e colorir eles
    if do_the_move == False:

        # TODO: atribuir 'b' quanfor for o jogador 2
        movements = player_moves(clicked_block)

        if movements != []:
            tag = 0
            if player == 1:
                tag = "a"
            else:
                tag = "b"

            board[clicked_block[0]][clicked_block[1]] = tag
            mark_user_move(movements)
            draw_rectangle(movements)
        else:
            return

    # o caminho que foi clicado deve ser checado, esse bloco possui
    # um 'x' indicando que a peça pode se mover para lá!
    else:
        mark = board[clicked_block[0]][clicked_block[1]]
        if mark == "x":
            piece_to_move_addr = find_piece_addr()
            move_piece_to_block(piece_to_move_addr, clicked_block)


def mark_user_move(movements):
    """
    marca com 'x' onde o usuário pode clicar após selecionar a peça
    """

    for i in range(len(movements)):
        row = movements[i][0]
        col = movements[i][1]

        board[row][col] = "x"


# TODO: vários pontos dessa função ser refatoradas
# em funções suporte
def check_move_limits(up, down):
    global player

    movements = []

    # verifica se o movimento na diagonal pra cima é válido
    if (up[0] >= 0 and up[0] <= 7) and (up[1] >= 0 and up[1] <= 7):
        path = board[up[0]][up[1]]
        # if path == 0 or path == "x":
        if path == 0:
            movements.append(up)

        # se for uma peça inimiga, há como derrotá-la?
        if player != path and path != 0:
            invalid_move = False
            i, j = (0, 0)

            if player == 1:
                i, j = (up[0] + 1, up[1] - 1)
                if (i > 7 or i < 0) or (j > 7 or j < 0):
                    invalid_move = True

            else:
                i, j = (up[0] - 1, up[1] - 1)
                if (i > 7 or i < 0) or (j > 7 or j < 0):
                    invalid_move = True

            if invalid_move != True:
                valid_space = board[i][j]
                if valid_space == 0:
                    movements.append((i, j))

    # diagonal pra baixo
    if (down[0] >= 0 and down[0] <= 7) and (down[1] >= 0 and down[1] <= 7):
        path = board[down[0]][down[1]]

        # if path == 0 or path == "x":
        if path == 0:
            movements.append(down)

        if player != path and path != 0:
            invalid_move = False

            i, j = (0, 0)

            if player == 1:
                i, j = (down[0] + 1, down[1] + 1)
                if (i > 7 or i < 0) or (j > 7 or j < 0):
                    invalid_move = True

            else:
                i, j = (down[0] - 1, down[1] + 1)
                if (i > 7 or i < 0) or (j > 7 or j < 0):
                    invalid_move = True

            if invalid_move != True:
                valid_space = board[i][j]
                if valid_space == 0:
                    movements.append((i, j))

    return movements


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

    # Player 1
    if player == 1:
        up_r = (block_addr[0] + 1, block_addr[1] - 1)
        down_r = (block_addr[0] + 1, block_addr[1] + 1)

        movements = check_move_limits(up_r, down_r)

    # Player 2
    else:
        up_l = (block_addr[0] - 1, block_addr[1] - 1)
        down_l = (block_addr[0] - 1, block_addr[1] + 1)

        movements = check_move_limits(up_l, down_l)

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

    # se o parâmetro passado for None, significa que
    # uma peça foi movida para uma nova posição e a borda
    # precisa ser preta
    if valid_moves is None:
        color = (0, 0, 0)
        pygame.draw.rect(screen, color, gray_rectangle, 4)
        return

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
    addr = board[i][j]

    if addr == 0:
        return

    if addr == 1 or addr == "a":
        color = (255, 0, 0)

    elif addr == 2 or addr == "b":
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


def create_matrix_board():
    # cria as 8x8 posições do tabuleiro preenchidas com zero
    for i in range(8):
        list = [0] * 8
        board.append(list)


def create_board():
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

            if board[i][j] == 0:
                pygame.draw.rect(screen, color, actual_block)


create_matrix_board()
draw_board()
create_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(board)
            check_movement()

    draw_board()
    draw_circle()

    pygame.display.flip()

    clock.tick(60)

pygame.quit
