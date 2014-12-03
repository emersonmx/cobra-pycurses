import sys
import curses

from cobra.application import Cobra

def setup_logger():
    import logging
    logging.basicConfig(filename="cobra.log", filemode="w", level=logging.DEBUG)

def run_application(stdscr):
    application = Cobra(stdscr)
    return application.run()

def main():
    setup_logger()

    sys.exit(curses.wrapper(run_application))

if __name__ == "__main__":
    main()
