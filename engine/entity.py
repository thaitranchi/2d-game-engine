import pygame

class Entity:
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Physics properties
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.friction = 0.8

        # Health
        self.health = 3
        self.invincible = False
        self.invincible_timer = 0

    def apply_physics(self):
        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Apply friction
        self.vel_x *= self.friction
        self.rect.x += self.vel_x

        # Keep the entity on the ground (pseudo floor at y=500)
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0

    def move(self, dx, dy):
        self.vel_x += dx
        self.vel_y += dy

    def draw(self, screen):
        if self.invincible and (pygame.time.get_ticks() // 300) % 2 == 0:
            return  # Flicker when invincible
        screen.blit(self.image, self.rect)

    def check_collision(self, other):
        return self.rect.colliderect(other.rect)
        
    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_timer = 120  # 2 seconds at 60 FPS

    def update_invincibility(self):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False