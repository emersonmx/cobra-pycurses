from cobra.game import Game

def setup_logger():
    import logging
    logging.basicConfig(filename="cobra.log", filemode="w", level=logging.DEBUG)

def main():
    setup_logger()

    game = Game()
    game.run()

if __name__ == "__main__":
    main()
