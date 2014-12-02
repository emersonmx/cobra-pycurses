import curses
import logging
logger = logging.getLogger(__name__)

from cobra.gamepad import GamePad
from cobra.screen import CursesScreen
from cobra.util import sleep


class GamePauseScreen(CursesScreen):

    RESUME_GAME = 0
    RETRY = 1
    BACK_TO_MENU = 2

    def __init__(self, application, game_screen):
        CursesScreen.__init__(self, application)

        self.game_screen = game_screen
        self.pause_window = None
        self.option = self.RESUME_GAME
        self.options = ["Resume game", "Retry", "Back to menu"]

        self.create()

    def create(self):
        self._create_pause_window()

    def _create_pause_window(self):
        width = 20
        height = len(self.options) + 2
        x = int(self.window_size[1] / 2 - width / 2)
        y = int(self.window_size[0] / 2 - height / 2)
        self.pause_window = self.stdscr.derwin(height, width, y, x)

    def show(self):
        self.gamepad.reset_commands()
        self._setup_gamepad()

    def _setup_gamepad(self):
        def up():
            self.option -= 1
            if self.option < self.RESUME_GAME:
                self.option = self.RESUME_GAME
        def down():
            self.option += 1
            if self.option > self.BACK_TO_MENU:
                self.option = self.BACK_TO_MENU
        def back():
            self.application.screen = self.game_screen
        def enter():
            if self.option == self.RESUME_GAME:
                back()
            elif self.option == self.RETRY:
                self.application.screen = WaitGameScreen(self.application)
            elif self.option == self.BACK_TO_MENU:
                pass

        self.gamepad.commands[GamePad.UP] = up
        self.gamepad.commands[GamePad.DOWN] = down
        self.gamepad.commands[GamePad.ENTER] = enter
        self.gamepad.commands[GamePad.BACK] = back

    def hide(self):
        pass

    def dispose(self):
        pass

    def update(self, delta):
        sleep()
        self.gamepad.process_input()

        self.stdscr.clear()
        self.game_screen.render_screen()
        self._render_pause_window()
        curses.doupdate()

    def _render_pause_window(self):
        self.pause_window.clear()
        self.pause_window.border()
        height, width = self.pause_window.getmaxyx()
        for i, option in enumerate(self.options):
            attribute = curses.A_NORMAL
            if i == self.option:
                attribute = curses.A_BOLD
            x = int(width / 2 - len(option) / 2)
            self.pause_window.addstr(i+1, x, option, attribute)

        self.pause_window.noutrefresh()

from cobra.screen.wait import WaitGameScreen
