import sys

from cobra.application import Cobra

def setup_logger():
    import logging
    logging.basicConfig(filename="cobra.log", filemode="w", level=logging.DEBUG)

def main():
    setup_logger()

    application = Cobra()
    sys.exit(application.run())

if __name__ == "__main__":
    main()
