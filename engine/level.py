import pygame
import os

class Level:
    def __init__(self, tile_size, asset_path):
        self.tile_size = tile_size
        self.asset_path = asset_path
        self.tiles = []
        self.player_spawn = (0, 0)
        self.exit_position = None

    def load_level(self, level_name):
        self.tiles = []
        level_file = os.path.join(self.asset_path, "levels", f"{level_name}.txt")
        with open(level_file, "r") as file:
            rows = file.readlines()
        
        for row_index, row in enumerate(rows):
            tiles_row = []
            for col_index, tile in enumerate(row.strip().split()):
                tile = int(tile)
                if tile == 2:
                    self.player_spawn = (col_index * self.tile_size, row_index * self.tile_size)
                    tile = 0  # Clear the spawn tile
                if tile == 3:
                    self.exit_position = pygame.Rect(
                        col_index * self.tile_size, 
                        row_index * self.tile_size, 
                        self.tile_size, 
                        self.tile_size
                    )
                tiles_row.append(tile)
            self.tiles.append(tiles_row)

    def draw(self, screen):
        block_img = pygame.image.load(os.path.join(self.asset_path, "block.png"))
        block_img = pygame.transform.scale(block_img, (self.tile_size, self.tile_size))

        for row_index, row in enumerate(self.tiles):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    screen.blit(block_img, (x, y))
