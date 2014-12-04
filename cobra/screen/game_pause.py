import curses
import logging
logger = logging.getLogger(__name__)

from cobra.gamepad import GamePad
from cobra.screen.option import OptionScreen


class GamePauseScreen(OptionScreen):

    RESUME_GAME = 0
    RETRY = 1
    BACK_TO_MENU = 2

    def __init__(self, application, game_screen):
        OptionScreen.__init__(self, application)

        self.game_screen = game_screen
        self.option = self.RESUME_GAME

    def create_options(self):
        return ["Resume game", "Retry", "Back to menu"]

    def create_window(self):
        height, width = self.window_size
        window_width = 20
        window_height = len(self.options) + 2
        x = int(width / 2 - window_width / 2)
        y = int(height / 2 - window_height / 2)
        return self.stdscr.derwin(window_height, window_width, y, x)

    def min_option(self):
        return self.RESUME_GAME

    def max_option(self):
        return self.BACK_TO_MENU

    def previous_button(self):
        return GamePad.UP

    def next_button(self):
        return GamePad.DOWN

    def enter(self):
        if self.option == self.RESUME_GAME:
            self.back()
        elif self.option == self.RETRY:
            wait_screen = WaitGameScreen(self.application)
            world_config = self.game_screen.world.config
            wait_screen.game_screen.world.config = world_config
            self.application.screen = wait_screen
        elif self.option == self.BACK_TO_MENU:
            self.application.screen = MenuScreen(self.application)

    def back(self):
        self.application.screen = self.game_screen

    def render(self):
        self.stdscr.erase()
        self.game_screen.render_screen()
        #self.render_pause_window()
        self.render_window()
        curses.doupdate()

    def render_window(self):
        self.window.erase()
        self.window.border()
        OptionScreen.render_window(self)

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
