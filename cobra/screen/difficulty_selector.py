import curses

from cobra.gamepad import GamePad
from cobra.screen.curses import CursesScreen
from cobra.model.world import WorldConfig


class DifficultySelectorScreen(CursesScreen):

    EASY = 0
    NORMAL = 1
    HARD = 2
    VERY_HARD = 3

    def __init__(self, application, menu_screen):
        CursesScreen.__init__(self, application)

        self.menu_screen = menu_screen

        self.options = ["Easy", "Normal", "Hard", "Very Hard"]
        self.option = self.EASY

    def setup_gamepad(self):
        def up():
            self.option -= 1
            if self.option < self.EASY:
                self.option = self.EASY
        def down():
            self.option += 1
            if self.option > self.VERY_HARD:
                self.option = self.VERY_HARD
        def enter():
            if self.option == self.EASY:
                self.application.screen = self.create_easy_game()
            elif self.option == self.NORMAL:
                self.application.screen = self.create_normal_game()
            elif self.option == self.HARD:
                self.application.screen = self.create_hard_game()
            elif self.option == self.VERY_HARD:
                self.application.screen = self.create_very_hard_game()
        def back():
            self.application.screen = self.menu_screen

        self.gamepad.commands[GamePad.UP] = up
        self.gamepad.commands[GamePad.DOWN] = down
        self.gamepad.commands[GamePad.ENTER] = enter
        self.gamepad.commands[GamePad.BACK] = back

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
        self.render_difficulty_options()
        self.stdscr.refresh()

    def render_difficulty_options(self):
        height, width = self.window_size
        padding = 2
        y = height - len(self.options) - padding
        for i, option in enumerate(self.options):
            attribute = curses.A_NORMAL
            if i == self.option:
                attribute = curses.A_BOLD
            x = int(width / 2 - len(option) / 2)
            self.stdscr.addstr(y+i, x, option, attribute)

from cobra.screen.wait import WaitGameScreen
