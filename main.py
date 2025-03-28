import pygame
from engine.game import Game
from engine.menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2D Game Engine")
    
    menu = Menu(screen)
    start_game = menu.run()
    
    if start_game:
        game = Game("2D Game Engine", 800, 600)
        game.run()

if __name__ == "__main__":
    main()
