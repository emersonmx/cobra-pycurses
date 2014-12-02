import curses

from cobra.gamepad import GamePad
from cobra.screen import CursesScreen
from cobra.util import sleep


class MenuScreen(CursesScreen):

    def __init__(self, application):
        CursesScreen.__init__(self, application)

    def setup_gamepad(self):
        pass

    def dispose(self):
        pass

    def update(self, delta):
        pass
