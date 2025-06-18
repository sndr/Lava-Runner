import pygame
from game.game import Game

def main():
    pygame.init()
    pygame.display.set_caption("Lava Runner")
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()