import pygame
import json
import os
import threading
import requests

class GameOverScreen:
    def __init__(self, screen, score, highscore_file="highscores.json"):
        self.screen = screen
        self.score = score
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.input_active = True
        self.player_name = ""
        self.highscore_file = highscore_file
        self.highscores = self.load_highscores()

    def load_highscores(self):
        if os.path.exists(self.highscore_file):
            with open(self.highscore_file, "r") as f:
                return json.load(f)
        return []

    def save_highscores(self):
        with open(self.highscore_file, "w") as f:
            json.dump(self.highscores, f, indent=4)

    def add_score(self, name, score):
        self.highscores.append({"name": name, "score": score})
        # Sort descending by score
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 10 scores
        self.highscores = self.highscores[:10]
        self.save_highscores()

    def run(self):
        clock = pygame.time.Clock()
        input_box = pygame.Rect(300, 300, 200, 50)
        active = False
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            # Finalize input
                            self.add_score(self.player_name, self.score)
                            self.input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            self.player_name += event.unicode
                    else:
                        if event.key == pygame.K_RETURN:
                            return "restart"
                        elif event.key == pygame.K_ESCAPE:
                            return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box, toggle active state.
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive

            self.screen.fill((0, 0, 0))
            # Display Game Over Text
            game_over_text = self.font_large.render("Game Over", True, (255, 0, 0))
            self.screen.blit(game_over_text, (250, 100))
            score_text = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (350, 200))

            # If still inputting name
            if self.input_active:
                prompt = self.font_small.render("Enter your name:", True, (255, 255, 255))
                self.screen.blit(prompt, (300, 260))
                txt_surface = self.font_small.render(self.player_name, True, color)
                self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                pygame.draw.rect(self.screen, color, input_box, 2)
            else:
                # Display leaderboard
                leader_text = self.font_small.render("High Scores:", True, (255, 255, 0))
                self.screen.blit(leader_text, (50, 400))
                for idx, entry in enumerate(self.highscores):
                    entry_text = self.font_small.render(f"{idx+1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
                    self.screen.blit(entry_text, (50, 450 + idx * 30))
                menu_text = self.font_small.render("Press Enter to Restart or Esc to Quit", True, (255, 255, 255))
                self.screen.blit(menu_text, (150, 350))

            pygame.display.flip()
            clock.tick(60)

    def submit_score_online(name, score, api_url="http://localhost:5000/submit_score"):
        def submit():
            try:
                response = requests.post(api_url, json={"name": name, "score": score}, timeout=5)
                if response.status_code == 200:
                    print("Score submitted successfully!")
                else:
                    print("Failed to submit score, status:", response.status_code)
            except Exception as e:
                print("Error submitting score:", e)
        threading.Thread(target=submit, daemon=True).start()

    # Inside your GameOverScreen.add_score() method:
    def add_score(self, name, score):
        self.highscores.append({"name": name, "score": score})
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        self.highscores = self.highscores[:10]
        self.save_highscores()
        # Submit score online asynchronously
        submit_score_online(name, score, "https://localhost:5000/submit_score")
