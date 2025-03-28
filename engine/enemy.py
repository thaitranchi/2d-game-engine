import pygame

class Enemy:
    def __init__(self, x, y, width, height, speed, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        # Patrol movement
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= 800:  # Screen width boundary
            self.direction *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class AdvancedEnemy:
    def __init__(self, x, y, width, height, speed, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.state = "patrol"  # states: 'patrol', 'chase', 'attack'
    
    def update(self, player_rect):
        if self.state == "patrol":
            self.rect.x += self.speed
            # Switch to chase if player is close
            if self.rect.colliderect(player_rect.inflate(100, 100)):
                self.state = "chase"
        elif self.state == "chase":
            # Move towards player
            if self.rect.x < player_rect.x:
                self.rect.x += self.speed * 1.5
            else:
                self.rect.x -= self.speed * 1.5
            # Switch to attack if very close
            if self.rect.colliderect(player_rect.inflate(20, 20)):
                self.state = "attack"
        elif self.state == "attack":
            # Attack logic (could be a cooldown or damage infliction)
            print("Enemy attacking!")
            # After attacking, return to patrol or chase
            self.state = "patrol"
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BossEnemy:
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.max_health = 100
        self.health = self.max_health
        self.phase = 1  # Boss phases: 1, 2, etc.
    
    def update(self, player_rect):
        # Boss behavior changes based on remaining health
        if self.health < self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            print("Boss entering phase 2!")
        # Basic movement or attack logic for each phase
        if self.phase == 1:
            self.rect.x += 2  # simple movement pattern
        else:
            self.rect.x -= 2  # alternate pattern in phase 2

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Draw health bar above boss
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, int(self.rect.width * health_ratio), 5))
