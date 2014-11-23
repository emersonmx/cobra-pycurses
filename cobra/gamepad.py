import curses
import curses.ascii

def no_command(): pass


class GamePad(object):

    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8
    ENTER = 16
    BACK = 32
    ALL_BUTTONS = 63

    def __init__(self, stdscr):
        super(GamePad, self).__init__()

        self.stdscr = stdscr
        self.buttons = {
            self.UP: set([curses.KEY_UP, ord('k')]),
            self.RIGHT: set([curses.KEY_RIGHT, ord('l')]),
            self.DOWN: set([curses.KEY_DOWN, ord('j')]),
            self.LEFT: set([curses.KEY_LEFT, ord('h')]),
            self.ENTER: set([ord('\n'), ord(' ')]),
            self.BACK: set([curses.ascii.ESC, ord('p')])
        }

        self.commands = {
            self.UP: no_command,
            self.RIGHT: no_command,
            self.DOWN: no_command,
            self.LEFT: no_command,
            self.ENTER: no_command,
            self.BACK: no_command,
        }

    def input(self):
        command = no_command

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
