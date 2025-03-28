import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.options = ["Resume", "Restart", "Quit"]
        self.selected = 0

    def draw(self):
        self.screen.fill((50, 50, 50))
        title = self.font.render("Paused", True, (255, 255, 255))
        self.screen.blit(title, (320, 100))
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.small_font.render(option, True, color)
            self.screen.blit(text, (360, 200 + i * 50))
        pygame.display.flip()

    def run(self):
        paused = True
        while paused:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected]
            pygame.time.delay(100)
