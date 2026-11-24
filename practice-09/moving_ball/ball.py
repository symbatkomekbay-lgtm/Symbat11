import pygame

class Ball:
    def __init__(self, width, height):
        self.x, self.y = width // 2, height // 2
        self.radius = 25
        self.width, self.height = width, height

    def move(self, dx, dy):
        x, y = self.x + dx, self.y + dy
        # Reject moves that cross any screen boundary.
        if self.radius <= x <= self.width - self.radius and self.radius <= y <= self.height - self.radius:
            self.x, self.y = x, y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
