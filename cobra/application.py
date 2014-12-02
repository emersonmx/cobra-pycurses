import time
import curses

from cobra.screen.menu import MenuScreen
from cobra.screen.base import Screen as NoScreen
from cobra.gamepad import CursesGamePad


class Cobra(object):

    def __init__(self):
        self.stdscr = None
        self.window_size = ()
        self.gamepad = None

        self.running = True
        self.error_code = 0
        self.last_ticks = 0

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
        self.error_code = error_code
        self.running = False

    def dispose(self):
        self.screen.dispose()

    def update(self):
        self.screen.update(self.delta_time())

    def delta_time(self):
        ticks = time.time()
        delta = ticks - self.last_ticks
        self.last_ticks = ticks

        return delta

    def run(self):
        curses.wrapper(self._run)
        return self.error_code

    def _run(self, stdscr):
        self.setup(stdscr)

        while self.running:
            self.update()

    def setup(self, stdscr):
        self.setup_curses()
        self.setup_curses_screen(stdscr)
        self.setup_gamepad(stdscr)
        self.setup_screen()

        self.last_ticks = time.time()

    def setup_curses(self):
        curses.resizeterm(24, 80)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)

    def setup_curses_screen(self, stdscr):
        self.stdscr = stdscr
        self.window_size = stdscr.getmaxyx()
        self.stdscr.nodelay(True)

    def setup_gamepad(self, stdscr):
        self.gamepad = CursesGamePad(stdscr)

    def setup_screen(self):
        self.screen = MenuScreen(self)
