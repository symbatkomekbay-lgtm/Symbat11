import pygame
import math
from datetime import datetime
from pathlib import Path

class MickeyClock:
    def __init__(self):
        image = pygame.image.load(str(Path(__file__).parent / 'images' / 'mickey_hand.png')).convert_alpha()
        self.minute_hand = pygame.transform.smoothscale(image, (180, 180))
        self.second_hand = pygame.transform.flip(pygame.transform.smoothscale(image, (240, 240)), True, False)
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        now = datetime.now()
        center = (250, 230)
        screen.fill((245, 240, 225))
        pygame.draw.circle(screen, (30, 30, 30), center, 190, 4)
        for i in range(60):
            a = math.radians(i * 6)
            r = 172 if i % 5 == 0 else 180
            p = lambda d: (round(center[0] + d * math.sin(a)), round(center[1] - d * math.cos(a)))
            pygame.draw.line(screen, (30, 30, 30), p(r), p(185), 3 if i % 5 == 0 else 1)
            if i % 5 == 0:
                label = self.font.render(str(i // 5 or 12), True, (30, 30, 30))
                screen.blit(label, label.get_rect(center=p(150)))
        # Images have their pivot at the center; negative angles rotate clockwise.
        for hand, angle in [(self.minute_hand, now.minute * 6), (self.second_hand, now.second * 6)]:
            rotated = pygame.transform.rotate(hand, -angle)
            screen.blit(rotated, rotated.get_rect(center=center))
        pygame.draw.circle(screen, (200, 30, 30), center, 7)
        label = self.font.render(now.strftime('%M:%S'), True, (30, 30, 30))
        screen.blit(label, label.get_rect(center=(250, 455)))
