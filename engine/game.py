import pygame
import os
from .entity import Entity
from .level import Level
from .save_system import SaveSystem
from .power_up import PowerUp
from .enemy import Enemy
from .game_over import GameOverScreen
from .network import NetworkClient

class Game:
    def __init__(self, title, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        self.asset_path = os.path.join(os.path.dirname(__file__), "../assets")
        self.sound_path = os.path.join(self.asset_path, "sounds/collision.wav")

        self.level = Level(50, self.asset_path)
        self.current_level = 1
        self.total_levels = 2
        self.load_level()

        pygame.mixer.init()
        self.collision_sound = pygame.mixer.Sound(self.sound_path)

        spawn_x, spawn_y = self.level.player_spawn
        self.player = Entity(spawn_x, spawn_y, 50, 50, f"{self.asset_path}/player.png")
        self.enemy = Enemy(200, 400, 50, 50, 2, f"{self.asset_path}/enemy.png")
        self.power_up = PowerUp(300, 300, 30, 30, f"{self.asset_path}/power_up.png")
        
        self.particles = []

        self.score = 0
        self.font = pygame.font.Font(None, 36)

        self.save_system = SaveSystem()
        self.load_game_state()

        self.network = NetworkClient()
        self.other_players = {}

    def load_level(self):
        level_name = f"level{self.current_level}"
        self.level.load_level(level_name)

    def load_game_state(self):
        data = self.save_system.load_game()
        if data:
            x, y = data["player_position"]
            self.player.rect.topleft = (x, y)
            self.score = data["score"]

    def save_game_state(self):
        position = (self.player.rect.x, self.player.rect.y)
        self.save_system.save_game(position, self.score)

    def update_particles(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game_state()
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player.move(-0.5, 0)
        if keys[pygame.K_RIGHT]:
            self.player.move(0.5, 0)

        self.player.apply_physics()
        self.player.update_invincibility()

        if self.level.exit_position and self.player.rect.colliderect(self.level.exit_position):
            self.current_level += 1
            if self.current_level > self.total_levels:
                self.running = False
            else:
                self.load_level()
                spawn_x, spawn_y = self.level.player_spawn
                self.player.rect.topleft = (spawn_x, spawn_y)

        self.enemy.update()
        if self.player.rect.colliderect(self.enemy.rect) and not self.player.invincible:
            self.player.take_damage()

        if self.power_up.collect(self.player):
            self.player.invincible = True
            self.player.invincible_timer = 300

        if self.player.health <= 0:
            game_over = GameOverScreen(self.screen, self.score)
            result = game_over.run()
            if result == "restart":
                self.restart_level()
                self.player.health = 3
                self.score = 0
            else:
                self.running = False

        position_data = {
            "id": "player1",
            "x": self.player.rect.x,
            "y": self.player.rect.y
        }
        self.network.send_data(position_data)

        while self.network.received_data:
            data = self.network.received_data.pop(0)
            player_id = data.get("id")
            if player_id != "player1":
                self.other_players[player_id] = (data.get("x"), data.get("y"))

    def render(self):
        self.screen.fill((30, 30, 30))

        self.player.draw(self.screen)
        for pos_data in self.other_players.values():
            pos = (int(pos_data[0]), int(pos_data[1]))
            pygame.draw.circle(self.screen, (0, 255, 0), pos, 20)
        self.enemy.draw(self.screen)
        self.power_up.draw(self.screen)

        for particle in self.particles:
            particle.draw(self.screen)

        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 40))
        
        # Additional UI Elements
        level_text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 70))

        pygame.display.flip()
