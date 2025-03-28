import pygame

class InputHandler:
    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
