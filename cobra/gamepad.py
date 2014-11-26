import curses


class GamePad(object):

    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8
    ENTER = 16
    BACK = 32
    ALL_BUTTONS = 63

    @staticmethod
    def no_command():
        pass

    def __init__(self):
        self.buttons = {}
        self.commands = {}
        self.reset_commands()

    def reset_commands(self):
        self.commands = {
            self.UP: self.no_command,
            self.RIGHT: self.no_command,
            self.DOWN: self.no_command,
            self.LEFT: self.no_command,
            self.ENTER: self.no_command,
            self.BACK: self.no_command,
        }

    def process_input(self):
        pass


class CursesGamePad(GamePad):

    def __init__(self, stdscr):
        GamePad.__init__(self)

        self.stdscr = stdscr
        self.buttons = {
            self.UP: set([curses.KEY_UP, ord('k')]),
            self.RIGHT: set([curses.KEY_RIGHT, ord('l')]),
            self.DOWN: set([curses.KEY_DOWN, ord('j')]),
            self.LEFT: set([curses.KEY_LEFT, ord('h')]),
            self.ENTER: set([ord('\n'), ord(' ')]),
            self.BACK: set([ord('p')])
        }

    def input(self):
        command = GamePad.no_command

        key = self._input_key()
        if key in self.buttons[self.UP]:
            command = self.commands[self.UP]
        elif key in self.buttons[self.DOWN]:
            command = self.commands[self.DOWN]
        if key in self.buttons[self.LEFT]:
            command = self.commands[self.LEFT]
        elif key in self.buttons[self.RIGHT]:
            command = self.commands[self.RIGHT]
        if key in self.buttons[self.ENTER]:
            command = self.commands[self.ENTER]
        if key in self.buttons[self.BACK]:
            command = self.commands[self.BACK]

        command()

    def _input_key(self):
        key = self.stdscr.getch()
        return key
