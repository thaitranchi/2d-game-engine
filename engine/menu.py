import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            title = self.font.render("2D Game Engine", True, (255, 255, 255))
            start = self.font.render("Press ENTER to Start", True, (255, 255, 255))

            self.screen.blit(title, (200, 150))
            self.screen.blit(start, (150, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
        return False
