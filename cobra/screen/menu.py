import curses
import logging
logger = logging.getLogger(__name__)

from cobra.gamepad import GamePad
from cobra.screen.option import OptionScreen


class MenuScreen(OptionScreen):

    START_GAME = 0
    HOW_TO = 1
    HISCORES = 2
    QUIT = 3

    def __init__(self, application):
        OptionScreen.__init__(self, application)

        self.logo = self.create_logo()
        self.option = self.START_GAME

    def create_logo(self):
        return [
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

    def create_options(self):
        return ["Start game", "How-To", "High Scores", "Quit"]

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
        return self.START_GAME

    def max_option(self):
        return self.QUIT

    def previous_button(self):
        return GamePad.UP

    def next_button(self):
        return GamePad.DOWN

    def enter(self):
        if self.option == self.START_GAME:
            self.application.screen = (
                DifficultySelectorScreen(self.application, self))
            logger.info("Start game")
        elif self.option == self.HOW_TO:
            logger.info("How-To")
        elif self.option == self.HISCORES:
            logger.info("High Scores")
        elif self.option == self.QUIT:
            self.back()

    def back(self):
        self.application.exit()

    def render(self):
        self.stdscr.erase()
        self.render_logo()
        self.render_window()
        self.stdscr.refresh()

    def render_logo(self):
        width = self.window_size[1]
        y = 2
        for i, line in enumerate(self.logo):
            x = int(width / 2 - len(line) / 2)
            self.stdscr.addstr(y+i, x, line)

from cobra.screen.difficulty_selector import DifficultySelectorScreen
