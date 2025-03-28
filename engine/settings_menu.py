import pygame

class SettingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.Font(None, 36)
        self.options = ["UI Scale", "Theme", "Sound Volume", "Back"]
        self.selected = 0

    def draw(self):
        self.screen.fill((40, 40, 40))
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            # Display current value for adjustable settings
            if option == "UI Scale":
                display_text = f"{option}: {self.settings['ui_scale']:.1f}"
            elif option == "Theme":
                display_text = f"{option}: {self.settings['theme']}"
            elif option == "Sound Volume":
                display_text = f"{option}: {self.settings['sound_volume']:.1f}"
            else:
                display_text = option

            text = self.font.render(display_text, True, color)
            self.screen.blit(text, (200, 150 + i * 50))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_LEFT:
                        if self.options[self.selected] == "UI Scale":
                            self.settings['ui_scale'] = max(0.5, self.settings['ui_scale'] - 0.1)
                        elif self.options[self.selected] == "Sound Volume":
                            self.settings['sound_volume'] = max(0.0, self.settings['sound_volume'] - 0.1)
                    elif event.key == pygame.K_RIGHT:
                        if self.options[self.selected] == "UI Scale":
                            self.settings['ui_scale'] = min(2.0, self.settings['ui_scale'] + 0.1)
                        elif self.options[self.selected] == "Sound Volume":
                            self.settings['sound_volume'] = min(1.0, self.settings['sound_volume'] + 0.1)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected] == "Theme":
                            # Toggle between dark and light themes
                            self.settings['theme'] = "light" if self.settings['theme'] == "dark" else "dark"
                        elif self.options[self.selected] == "Back":
                            return "Back"
            pygame.time.delay(100)
