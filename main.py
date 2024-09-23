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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = false

    screen.fill("gray")

    color = (0, 0, 0)

    # desenha todas os 64 quadrados que representam
    # as posições da mesa
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

    pygame.display.flip()
    clock.tick(60)

pygame.quit
