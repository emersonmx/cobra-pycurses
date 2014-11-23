import sys
import curses

from cobra.screen import GameScreen
from cobra.screen import Screen as NoScreen


class Cobra(object):

    def __init__(self):
        super(Cobra, self).__init__()

        self.stdscr = None
        self.window_size = None

        self._running = True
        self._error_code = 0

        self._screen = NoScreen()

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        self._screen.dispose()
        self._screen = screen
        self._screen.create()

    def exit(self, error_code=0):
        self._error_code = error_code
        self._running = False

    def create(self):
        self.screen.create()

    def dispose(self):
        self.screen.dispose()

    def update(self):
        self.screen.update()

    def run(self):
        curses.wrapper(self._run, sys.argv)

    def _run(self, stdscr, args):
        self._setup(stdscr, args)

        while self._running:
            self.update() # TODO: pass delta time to update().

        sys.exit(self._error_code)

    def _setup(self, stdscr, args):
        curses.resizeterm(24, 80)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)

        self.stdscr = stdscr
        self.window_size = stdscr.getmaxyx()
        self.screen = GameScreen(self)
