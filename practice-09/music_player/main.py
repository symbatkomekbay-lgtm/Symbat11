import pygame
from player import Player

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 320))
pygame.display.set_caption('Music Player')
player = Player()
font = pygame.font.Font(None, 30)
fps = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == player.end_event and player.playing:
            player.change(1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: player.play()
            elif event.key == pygame.K_s: player.stop()
            elif event.key == pygame.K_n: player.change(1)
            elif event.key == pygame.K_b: player.change(-1)
            elif event.key == pygame.K_q: running = False
    screen.fill((25, 32, 48))
    pos = player.position()
    lines = ['Music Player', player.name, 'Playing' if player.playing else 'Stopped', f'Position: {pos // 60:02}:{pos % 60:02}', 'P: Play   S: Stop   N: Next', 'B: Previous   Q: Quit']
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, (240, 240, 240)), (25, 25 + i * 44))
    pygame.display.flip()
    fps.tick(30)
pygame.quit()
