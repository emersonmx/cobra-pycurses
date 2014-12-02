import time
import curses

from cobra.screen.game import GameScreen
from cobra.screen.wait import WaitGameScreen
from cobra.screen import Screen as NoScreen
from cobra.gamepad import CursesGamePad


class Cobra(object):

    def __init__(self):
        self.stdscr = None
        self.window_size = ()
        self.gamepad = None

        self._running = True
        self._error_code = 0
        self._last_ticks = 0

        self._screen = NoScreen()

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        self._screen.hide()
        self._screen = screen
        self._screen.show()

    def exit(self, error_code=0):
        self._error_code = error_code
        self._running = False

    def dispose(self):
        self.screen.dispose()

    def update(self):
        self.screen.update(self._delta_time())

    def _delta_time(self):
        ticks = time.time()
        delta = ticks - self._last_ticks
        self._last_ticks = ticks

        return delta

    def run(self):
        curses.wrapper(self._run)
        return self._error_code

    def _run(self, stdscr):
        self._setup(stdscr)

        while self._running:
            self.update()

    def _setup(self, stdscr):
        self._setup_curses()
        self._setup_curses_screen(stdscr)
        self._setup_gamepad(stdscr)
        self._setup_screen()

        self._last_ticks = time.time()

    def _setup_curses(self):
        curses.resizeterm(24, 80)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)

    def _setup_curses_screen(self, stdscr):
        self.stdscr = stdscr
        self.window_size = stdscr.getmaxyx()
        self.stdscr.nodelay(True)

    def _setup_gamepad(self, stdscr):
        self.gamepad = CursesGamePad(stdscr)

    def _setup_screen(self):
        self.screen = WaitGameScreen(self)
