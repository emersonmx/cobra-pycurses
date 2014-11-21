import logging
from cobra.game import Game

def main():
    logging.basicConfig(filename="cobra.log", filemode="w", level=logging.DEBUG)

    game = Game()
    game.run()

if __name__ == "__main__":
    main()
