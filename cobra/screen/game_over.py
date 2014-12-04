from cobra.gamepad import GamePad
from cobra.screen.curses import CursesScreen


class GameOverScreen(CursesScreen):

    RETRY = 0
    SUBMIT_SCORE = 1
    BACK_TO_MENU = 2

    def __init__(self, application):
        CursesScreen.__init__(self, application)

        self.options = []
        self.option = self.RETRY

from cobra.screen.game import GameScreen
from cobra.screen.menu import MenuScreen
#from cobra.screen.submit_score import SubmitScore
