import time
import curses

from cobra.screen.menu import MenuScreen
from cobra.screen import Screen as NoScreen
from cobra.gamepad import CursesGamePad


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


class Cobra(Application):

    def __init__(self, stdscr):
        Application.__init__(self)

        self.stdscr = stdscr
        self.window_size = ()
        self.gamepad = None

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

    def create(self):
        self.setup_curses()
        self.create_gamepad()
        self.create_screen()
        self.last_ticks = time.time()

    def dispose(self):
        self.screen.dispose()

    def update(self):
        self.screen.update(self.delta_time())

    def delta_time(self):
        ticks = time.time()
        delta = ticks - self.last_ticks
        self.last_ticks = ticks

        return delta

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
