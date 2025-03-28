import pygame

class PowerUp:
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = True

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

    def collect(self, player):
        if self.active and self.rect.colliderect(player.rect):
            self.active = False
            return True
        return False
