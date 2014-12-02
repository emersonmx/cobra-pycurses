import curses

from cobra.gamepad import GamePad
from cobra.screen import CursesScreen
from cobra.util import sleep


class DifficultySelectorScreen(CursesScreen):

    def __init__(self, application, menu_screen):
        CursesScreen.__init__(self, application)

        self.menu_screen = menu_screen

    def setup_gamepad(self):
        pass

    def update(self, delta):
        sleep()
        self.gamepad.process_input()

        self.render()

    def render(self):
        self.stdscr.clear()
        self.stdscr.refresh()
