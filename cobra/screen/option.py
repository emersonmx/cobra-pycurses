import curses

from cobra.gamepad import GamePad
from cobra.screen.curses import CursesScreen


class OptionScreen(CursesScreen):

    def __init__(self, application):
        CursesScreen.__init__(self, application)

        self.last_screen = None

        self.options = self.create_options()
        self.option = 0

        self.window = self.create_window()

    def create_options(self):
        pass

    def create_window(self):
        pass

    def setup_gamepad(self):
        self.gamepad.commands[self.previous_button()] = self.previous_option
        self.gamepad.commands[self.next_button()] = self.next_option
        self.gamepad.commands[GamePad.ENTER] = self.enter
        self.gamepad.commands[GamePad.BACK] = self.back

    def previous_option(self):
        self.option -= 1
        if self.option < self.min_option():
            self.option = self.min_option()

    def min_option(self):
        pass

    def next_option(self):
        self.option += 1
        if self.option > self.max_option():
            self.option = self.max_option()

    def max_option(self):
        pass

    def previous_button(self):
        pass

    def next_button(self):
        pass

    def enter(self):
        pass

    def back(self):
        self.application.screen = self.last_screen

    def render_window(self):
        height, width = self.window.getmaxyx()
        padding = 1
        self.window.border()
        for i, option in enumerate(self.options):
            attribute = curses.A_NORMAL
            if i == self.option:
                attribute = curses.A_BOLD

            x = int(width / 2 - len(option) / 2)
            self.window.addstr(i+padding, x, option, attribute)

        self.window.noutrefresh()
