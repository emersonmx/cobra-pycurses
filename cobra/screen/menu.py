import curses
import logging
logger = logging.getLogger(__name__)

from cobra.gamepad import GamePad
from cobra.screen.curses import CursesScreen


class MenuScreen(CursesScreen):

    START_GAME = 0
    HOW_TO = 1
    HISCORES = 2
    QUIT = 3

    def __init__(self, application):
        CursesScreen.__init__(self, application)

        self.logo = []
        self.options = ["Start", "How-To", "High Scores", "Quit"]
        self.option = self.START_GAME

        self.create()

    def create(self):
        self.create_logo()

    def create_logo(self):
        self.logo = [
            " ##############                                                             ",
            "################                                                            ",
            "###############                                                             ",
            "####                                                                        ",
            "###                ##########   ############   ############      ########   ",
            "###               ############  ############## ##############   ##########  ",
            "###              ####      #### ###        ### ###        ###  ###      ### ",
            "###              ###        ### ###        ### ###        ### ###        ###",
            "###              ###        ### ############   ############   ###        ###",
            "###              ###        ### ###        ### ###    ###     ##############",
            "####             ###        ### ###        ### ###     ###    ##############",
            "###############  ####      #### ###        ### ###      ###   ###        ###",
            "################  ############  ############## ###       ###  ###        ###",
            " ##############    ##########   ############   ###        ### ###        ###"
        ]

    def setup_gamepad(self):
        def up():
            self.option -= 1
            if self.option < self.START_GAME:
                self.option = self.START_GAME
        def down():
            self.option += 1
            if self.option > self.QUIT:
                self.option = self.QUIT
        def back():
            self.application.exit()
        def enter():
            if self.option == self.START_GAME:
                self.application.screen = (
                    DifficultySelectorScreen(self.application, self))
                logger.info("Start game")
            elif self.option == self.HOW_TO:
                logger.info("How-To")
            elif self.option == self.HISCORES:
                logger.info("High scores")
            elif self.option == self.QUIT:
                back()

        self.gamepad.commands[GamePad.UP] = up
        self.gamepad.commands[GamePad.DOWN] = down
        self.gamepad.commands[GamePad.ENTER] = enter
        self.gamepad.commands[GamePad.BACK] = back

    def render(self):
        self.stdscr.erase()
        self.render_logo()
        self.render_menu()
        self.stdscr.refresh()

    def render_logo(self):
        width = self.window_size[1]
        y = 2
        for i, line in enumerate(self.logo):
            x = int(width / 2 - len(line) / 2)
            self.stdscr.addstr(y+i, x, line)

    def render_menu(self):
        height, width = self.window_size
        padding = 2
        y = height - len(self.options) - padding
        for i, option in enumerate(self.options):
            attribute = curses.A_NORMAL
            if i == self.option:
                attribute = curses.A_BOLD
            x = int(width / 2 - len(option) / 2)
            self.stdscr.addstr(y+i, x, option, attribute)

from cobra.screen.difficulty_selector import DifficultySelectorScreen
