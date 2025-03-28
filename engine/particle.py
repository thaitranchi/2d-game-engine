import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.color = color
        self.lifetime = random.randint(20, 50)
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
