import pygame
from clock import MickeyClock

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Mickey's Clock")
app = MickeyClock()
fps = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    app.draw(screen)
    pygame.display.flip()
    fps.tick(30)
pygame.quit()
