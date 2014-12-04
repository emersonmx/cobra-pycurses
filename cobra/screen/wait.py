import curses

from cobra.gamepad import GamePad
from cobra.screen.curses import CursesScreen


class WaitGameScreen(CursesScreen):

    def __init__(self, application):
        CursesScreen.__init__(self, application)

        self.game_screen = None
        self.message_window = None
        self.message = "Press any key to start."

        self.create()

    def create(self):
        self.create_message_window()
        self.create_game_screen()

    def create_message_window(self):
        padding = 3
        width = len(self.message) + 2 * padding
        height = 3
        x = int(self.window_size[1] / 2 - width / 2)
        y = int(self.window_size[0] / 3 - height / 2)
        self.message_window = self.stdscr.derwin(height, width, y, x)

    def create_game_screen(self):
        self.game_screen = GameScreen(self.application)

    def setup_gamepad(self):
        def start_game():
            self.application.screen = self.game_screen

        number_of_buttons = bin(GamePad.ALL_BUTTONS).count('1')
        commands = [1 << i for i in range(number_of_buttons)]
        for command in commands:
            self.gamepad.commands[command] = start_game

    def render(self):
        self.stdscr.erase()
        self.game_screen.render_screen()
        self.render_message_window()
        curses.doupdate()

    def render_message_window(self):
        height, width = self.message_window.getmaxyx()
        x = int(width / 2 - len(self.message) / 2)
        y = int(height / 2)
        self.message_window.erase()
        self.message_window.border()
        self.message_window.addstr(y, x, self.message)
        self.message_window.noutrefresh()

from cobra.screen.game import GameScreen
