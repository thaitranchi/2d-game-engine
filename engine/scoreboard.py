import pygame
import os

class Scoreboard:
    def __init__(self, screen, font_name='Arial', font_size=30, color=(255, 255, 255)):
        self.screen = screen
        self.font = pygame.font.SysFont(font_name, font_size)
        self.color = color
        self.score = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if os.path.exists('highscore.txt'):
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        with open('highscore.txt', 'w') as file:
            file.write(str(self.high_score))

    def update_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset_score(self):
        self.score = 0

    def render(self):
        score_text = f'Score: {self.score}'
        high_score_text = f'High Score: {self.high_score}'

        score_surface = self.font.render(score_text, True, self.color)
        high_score_surface = self.font.render(high_score_text, True, self.color)

        # Draw scores on the top left corner
        self.screen.blit(score_surface, (10, 10))
        self.screen.blit(high_score_surface, (10, 50))

    def handle_event(self, event):
        # Example of handling events if needed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_score()