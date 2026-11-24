import pygame
from ball import Ball

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Moving Ball')
ball = Ball(*screen.get_size())
clock = pygame.time.Clock()
moves = {pygame.K_UP: (0, -20), pygame.K_DOWN: (0, 20), pygame.K_LEFT: (-20, 0), pygame.K_RIGHT: (20, 0)}
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key in moves:
            ball.move(*moves[event.key])
    screen.fill((255, 255, 255))
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
