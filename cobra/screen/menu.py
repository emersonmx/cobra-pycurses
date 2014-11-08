import sys
import curses

from cobra.screen.screen import Screen
from cobra.screen.game import Game
from cobra.screen.high_score import HighScore


class Menu(Screen):

    START_GAME = 0
    HIGH_SCORE = 1
    QUIT = 2

    def __init__(self, game):
        super(Menu, self).__init__(game)

        self.window_size = self.game.window_size
        self.window_center = self.window_size[0] / 2, self.window_size[1] / 2

        self.game_title = None
        self.menu_entry = self.START_GAME
        self.menu_entries = None

    def create(self):
        self.game_title = [
            "########   ######   #######   #######    ######",
            "##        ##    ##  ##    ##  ##    ##  ##    ##",
            "##        ##    ##  ##    ##  ##    ##  ##    ##",
            "##        ##    ##  ######    ########  ########",
            "##        ##    ##  ##    ##  #####     ##    ##",
            "##        ##    ##  ##    ##  ##  ##    ##    ##",
            "########  ########  ########  ##   ##   ##    ##",
            "########   ######   #######   ##    ##  ##    ##"
        ]
        self.menu_entries = [
            "Start game",
            "High scores",
            "Quit"
        ]

    def handle_input(self):
        key = self.stdscr.getch()
        if key == curses.KEY_UP:
            self.menu_entry -= 1
            if self.menu_entry < self.START_GAME:
                self.menu_entry = self.START_GAME
        elif key == curses.KEY_DOWN:
            self.menu_entry += 1
            if self.menu_entry > self.QUIT:
                self.menu_entry = self.QUIT

        if key == ord('\n'):
            if self.menu_entry == self.START_GAME:
                self.game.screen = Game(self.game)
            elif self.menu_entry == self.HIGH_SCORE:
                self.game.screen = HighScore(self.game)
            elif self.menu_entry == self.QUIT:
                self.game.exit()

    def draw(self):
        for i,v in enumerate(self.game_title):
            self.stdscr.addstr(
                    self.window_center[0] - len(self.game_title) - 2 + i,
                    self.window_center[1] - len(v) / 2, v)
        for i, v in enumerate(self.menu_entries):
            if i == self.menu_entry:
                v = ">>> {} <<<".format(v)
            else:
                v = "    {}    ".format(v)

            self.stdscr.addstr(self.window_center[0] + i,
                    self.window_center[1] - len(v) / 2, v)

        self.stdscr.refresh()

    def update(self):
        self.handle_input()
        self.draw()
