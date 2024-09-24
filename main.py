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

    screen.fill("gray")
    color = (0, 0, 0)

    for i in range(0, 8):
        for j in range(0, 8):
            actual_block = pygame.Rect(
                square_height * i,
                square_width * j,
                square_height,
                square_width,
            )

            # screen, color, pygame.Rect, tamanho da borda
            pygame.draw.rect(screen, color, actual_block, 2)


create_board()
draw_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = false

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

    pygame.display.flip()
    clock.tick(60)

pygame.quit
