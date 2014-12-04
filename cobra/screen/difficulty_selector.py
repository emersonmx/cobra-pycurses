import curses

from cobra.gamepad import GamePad
from cobra.screen.option import OptionScreen
from cobra.model.world import WorldConfig


class DifficultySelectorScreen(OptionScreen):

    EASY = 0
    NORMAL = 1
    HARD = 2
    VERY_HARD = 3

    def __init__(self, application, menu_screen):
        OptionScreen.__init__(self, application)

        self.menu_screen = menu_screen

        self.option = self.EASY

    def create_options(self):
        return ["Easy", "Normal", "Hard", "Very Hard"]

    def create_window(self):
        height, width = self.window_size
        padding = 2
        margin = 1
        window_width = 16
        window_height = len(self.options) + padding
        x = int(width / 2 - window_width / 2)
        y = height - len(self.options) - padding - margin
        return self.stdscr.derwin(window_height, window_width, y, x)

    def min_option(self):
        return self.EASY

    def max_option(self):
        return self.VERY_HARD

    def previous_button(self):
        return GamePad.UP

    def next_button(self):
        return GamePad.DOWN

    def enter(self):
        if self.option == self.EASY:
            self.application.screen = self.create_easy_game()
        elif self.option == self.NORMAL:
            self.application.screen = self.create_normal_game()
        elif self.option == self.HARD:
            self.application.screen = self.create_hard_game()
        elif self.option == self.VERY_HARD:
            self.application.screen = self.create_very_hard_game()

    def back(self):
        self.application.screen = self.menu_screen

    def create_easy_game(self):
        wait_screen = WaitGameScreen(self.application)
        wait_screen.game_screen.world.config = self.create_easy_world()
        return wait_screen

    def create_easy_world(self):
        world_config = WorldConfig()
        return world_config

    def create_normal_game(self):
        wait_screen = WaitGameScreen(self.application)
        wait_screen.game_screen.world.config = self.create_normal_world()
        return wait_screen

    def create_normal_world(self):
        world_config = WorldConfig()
        return world_config

    def create_hard_game(self):
        wait_screen = WaitGameScreen(self.application)
        wait_screen.game_screen.world.config = self.create_hard_world()
        return wait_screen

    def create_hard_world(self):
        world_config = WorldConfig()
        return world_config

    def create_very_hard_game(self):
        wait_screen = WaitGameScreen(self.application)
        wait_screen.game_screen.world.config = self.create_very_hard_world()
        return wait_screen

    def create_very_hard_world(self):
        world_config = WorldConfig()
        return world_config

    def render(self):
        self.stdscr.erase()
        self.menu_screen.render_logo()
        self.render_window()
        self.stdscr.refresh()

from cobra.screen.wait import WaitGameScreen
