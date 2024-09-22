import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = false

    screen.fill("gray")
    pygame.display.flip()
    clock.tick(60)

pygame.quit
