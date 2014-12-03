import curses

from cobra.screen.menu import MenuScreen
from cobra.screen import Screen as NoScreen
from cobra.gamepad import CursesGamePad
from cobra.util import *


class Application(object):

    def __init__(self):
        self.running = True
        self.error_code = 0

    def exit(self, error_code=0):
        self.error_code = error_code
        self.running = False

    def create(self):
        pass

    def dispose(self):
        pass

    def update(self):
        pass

    def run(self):
        self.create()

        while self.running:
            self.update()

        self.dispose()

        return self.error_code


class Game(Application):

    def __init__(self):
        Application.__init__(self)

        self.last_ticks = time.time()
        self.framerate = 1000 / 60.

        self._screen = NoScreen()

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        self._screen.hide()
        self._screen = screen
        self._screen.show()

    def update(self):
        delay(self.framerate)
        delta_time = self.calculate_delta_time()
        self.screen.update(delta_time)

    def calculate_delta_time(self):
        ticks = time.time()
        delta_time = ticks - self.last_ticks
        self.last_ticks = ticks
        return delta_time


class Cobra(Game):

    def __init__(self, stdscr):
        Game.__init__(self)

        self.stdscr = stdscr
        self.window_size = ()
        self.gamepad = None

    def create(self):
        self.setup_curses()
        self.create_gamepad()
        self.create_screen()

    def setup_curses(self):
        curses.resizeterm(24, 80)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)
        self.window_size = self.stdscr.getmaxyx()
        self.stdscr.nodelay(True)

    def create_gamepad(self):
        self.gamepad = CursesGamePad(self.stdscr)

    def create_screen(self):
        self.screen = MenuScreen(self)
