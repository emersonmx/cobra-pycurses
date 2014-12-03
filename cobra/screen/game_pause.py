import curses
import logging
logger = logging.getLogger(__name__)

from cobra.gamepad import GamePad
from cobra.screen.curses import CursesScreen


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
        self.create_pause_window()

    def create_pause_window(self):
        width = 20
        height = len(self.options) + 2
        x = int(self.window_size[1] / 2 - width / 2)
        y = int(self.window_size[0] / 2 - height / 2)
        self.pause_window = self.stdscr.derwin(height, width, y, x)

    def setup_gamepad(self):
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
                wait_screen = WaitGameScreen(self.application)
                world_config = self.game_screen.world.config
                wait_screen.game_screen.world.config = world_config
                self.application.screen = wait_screen
            elif self.option == self.BACK_TO_MENU:
                self.application.screen = MenuScreen(self.application)

        self.gamepad.commands[GamePad.UP] = up
        self.gamepad.commands[GamePad.DOWN] = down
        self.gamepad.commands[GamePad.ENTER] = enter
        self.gamepad.commands[GamePad.BACK] = back

    def update(self, delta):
        self.gamepad.process_input()

        self.stdscr.erase()
        self.game_screen.render_screen()
        self.render_pause_window()
        curses.doupdate()

    def render_pause_window(self):
        self.pause_window.erase()
        self.pause_window.border()
        width = self.pause_window.getmaxyx()[1]
        for i, option in enumerate(self.options):
            attribute = curses.A_NORMAL
            if i == self.option:
                attribute = curses.A_BOLD
            x = int(width / 2 - len(option) / 2)
            self.pause_window.addstr(i+1, x, option, attribute)

        self.pause_window.noutrefresh()

from cobra.screen.wait import WaitGameScreen
from cobra.screen.menu import MenuScreen
