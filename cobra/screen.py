import sys
import time
import curses


class Screen(object):

    def __init__(self, game):
        super(Screen, self).__init__()

        self._game = game
        self.stdscr = game.stdscr
        self.window_size = self.game.window_size
        self.window_center = self.window_size[0] / 2, self.window_size[1] / 2

    @property
    def game(self):
        return self._game

    def create(self):
        pass

    def dispose(self):
        pass

    def update(self):
        pass


class GameScreen(Screen):

    def __init__(self, game):
        super(GameScreen, self).__init__(game)

        self.score_text = None

    def create(self):
        pass

    def _draw_score(self):
        pass

    def _draw_game_area(self):
        pass

    def draw(self):
        self._draw_score()
        self._draw_game_area()

        self.stdscr.refresh()

    def update(self):
        time.sleep(0.05)
        self.draw()


class HighScoreScreen(Screen):

    def __init__(self, game):
        super(HighScoreScreen, self).__init__(game)

    def create(self):
        pass

    def update(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "High Scores")
        self.stdscr.refresh()


class MenuScreen(Screen):

    START_GAME = 0
    HIGH_SCORE = 1
    QUIT = 2

    def __init__(self, game):
        super(MenuScreen, self).__init__(game)

        self.game_logo = None
        self.menu_entry = self.START_GAME
        self.menu_entries = None
        self.layout = None

    def create(self):
        self.game_logo = [
            "########   ######   #######   #######    ###### ",
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

        self.layout = (self.window_center[0] - 8, self.window_center[1] - 24,
            self.window_center[0] + 8, self.window_center[1] + 24)

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
                self.game.screen = GameScreen(self.game)
            elif self.menu_entry == self.HIGH_SCORE:
                self.game.screen = HighScoreScreen(self.game)
            elif self.menu_entry == self.QUIT:
                self.game.exit()

    def _draw_logo(self):
        for i, v in enumerate(self.game_logo):
            self.stdscr.addstr(self.layout[0] + i, self.layout[1], v)

    def _draw_menu(self):
        for i, v in enumerate(self.menu_entries):
            attr = curses.A_NORMAL
            if i == self.menu_entry:
                attr = curses.A_BOLD

            self.stdscr.addstr(self.layout[2] - len(self.menu_entries) + i,
                    self.window_center[1] - len(v) / 2, v, attr)

    def draw(self):
        self._draw_logo()
        self._draw_menu()

        self.stdscr.refresh()

    def update(self):
        time.sleep(0.05)

        self.handle_input()
        self.draw()
