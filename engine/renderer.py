import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def clear(self):
        self.screen.fill((0, 0, 0))  # Black background

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.screen, color, rect)

    def display(self):
        pygame.display.flip()
