from cobra.game import Game

def setup_logger():
    import logging

    logging_format = ("%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s:"
                      " %(message)s")
    logging.basicConfig(filename="cobra.log", filemode="w",
                        format=logging_format, level=logging.DEBUG)


def main():
    setup_logger()

    game = Game()
    game.run()

if __name__ == "__main__":
    main()
