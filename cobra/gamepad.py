import curses


class GamePad(object):

    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8
    ACTION = 16
    ALL_BUTTONS = 31

    def __init__(self, stdscr):
        super(GamePad, self).__init__()

        self.stdscr = stdscr
        self.buttons = {
            self.UP: (curses.KEY_UP, ord('k')),
            self.RIGHT: (curses.KEY_RIGHT, ord('l')),
            self.DOWN: (curses.KEY_DOWN, ord('j')),
            self.LEFT: (curses.KEY_LEFT, ord('h')),
            self.ACTION: (ord('p'), ord('m'))
        }

        self.commands = {}

    def bind_command(self, button, command):
        self.commands[button] = command

    def input(self):
        command = self._null_command

        key = self._input_key()
        if key in self.buttons[self.UP]:
            command = self.commands[self.UP]
        elif key in self.buttons[self.DOWN]:
            command = self.commands[self.DOWN]
        if key in self.buttons[self.LEFT]:
            command = self.commands[self.LEFT]
        elif key in self.buttons[self.RIGHT]:
            command = self.commands[self.RIGHT]
        if key in self.buttons[self.ACTION]:
            command = self.commands[self.ACTION]

        command()

    def _null_command(self):
        pass

    def _input_key(self):
        key = self.stdscr.getch()
        curses.flushinp()
        return key
