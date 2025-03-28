import json
import os

class SaveSystem:
    def __init__(self, save_file="save_data.json"):
        self.save_file = save_file

    def save_game(self, player_position, score):
        data = {
            "player_position": player_position,
            "score": score
        }
        with open(self.save_file, "w") as file:
            json.dump(data, file, indent=4)
        print("Game saved!")

    def load_game(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as file:
                data = json.load(file)
                print("Game loaded!")
                return data
        return None
