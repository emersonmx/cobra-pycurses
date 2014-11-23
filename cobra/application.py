import sys
import curses

from cobra.screen import GameScreen


class Cobra(object):

    def __init__(self):
        super(Cobra, self).__init__()

        self.stdscr = None
        self.window_size = []

        self._running = True
        self._error_code = 0

        self._screen = None

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        if self._screen:
            self._screen.dispose()

        self._screen = value
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

    def _setup(self, stdscr, args):
        curses.resizeterm(24, 80)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)
        stdscr.nodelay(True)
        #stdscr.border()

        self.stdscr = stdscr
        self.window_size = stdscr.getmaxyx()
        self.screen = GameScreen(self)

    def _run(self, stdscr, args):
        self._setup(stdscr, args)

        self.create()
        while self._running:
            self.update()

        self.dispose()

        sys.exit(self._error_code)

    def run(self):
        curses.wrapper(self._run, sys.argv)
