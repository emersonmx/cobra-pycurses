import sys
import curses

from cobra.screen import MenuScreen


class Game(object):

    def __init__(self):
        super(Game, self).__init__()

        self.stdscr = None
        self._window_size = []
        self._screen = None

        self._running = True
        self._error_code = 0

    @property
    def window_size(self):
        return self._window_size

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        if self._screen:
            self._screen.dispose()

        screen.create()
        self._screen = screen

    def exit(self, error_code=0):
        self._error_code = error_code
        self._running = False

    def create(self):
        self._screen.create()

    def dispose(self):
        self._screen.dispose()

    def update(self):
        self._screen.update()

    def _setup(self, stdscr, args):
        curses.resizeterm(24, 80)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)
        stdscr.nodelay(True)

        self.stdscr = stdscr
        self._window_size = stdscr.getmaxyx()

        self.screen = MenuScreen(self)

    def _run(self, stdscr, args):
        self._setup(stdscr, args)

        self.create()
        while self._running:
            self.update()

        self.dispose()

        sys.exit(self._error_code)

    def run(self):
        curses.wrapper(self._run, sys.argv)
