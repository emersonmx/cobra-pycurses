import curses
import logging
logger = logging.getLogger(__name__)

from cobra.gamepad import GamePad
from cobra.screen import CursesScreen
from cobra.util import sleep


class MenuScreen(CursesScreen):

    START_GAME = 0
    HOW_TO = 1
    HISCORES = 2
    QUIT = 3

    def __init__(self, application):
        CursesScreen.__init__(self, application)

        self.logo = []
        self.menu_options = ["Start", "How-To", "High Scores", "Quit"]
        self.option = self.START_GAME

        self.create()

    def create(self):
        self._create_logo()

    def _create_logo(self):
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
        def enter():
            if self.option == self.START_GAME:
                logger.info("Start game")
            elif self.option == self.HOW_TO:
                logger.info("How-To")
            elif self.option == self.HISCORES:
                logger.info("High scores")
            elif self.option == self.QUIT:
                self.application.exit()

        self.gamepad.commands[GamePad.UP] = up
        self.gamepad.commands[GamePad.DOWN] = down
        self.gamepad.commands[GamePad.ENTER] = enter

    def update(self, delta):
        sleep()
        self.gamepad.process_input()

        self._render()

    def _render(self):
        self.stdscr.clear()
        self.stdscr.border()
        self._render_logo()
        self._render_menu()
        self.stdscr.refresh()

    def _render_logo(self):
        height, width = self.window_size
        y = 2
        for i, line in enumerate(self.logo):
            x = int(width / 2 - len(line) / 2)
            self.stdscr.addstr(y+i, x, line)

    def _render_menu(self):
        height, width = self.window_size
        padding = 2
        y = height - len(self.menu_options) - padding
        for i, option in enumerate(self.menu_options):
            attribute = curses.A_NORMAL
            if i == self.option:
                attribute = curses.A_BOLD
            x = int(width / 2 - len(option) / 2)
            self.stdscr.addstr(y+i, x, option, attribute)
