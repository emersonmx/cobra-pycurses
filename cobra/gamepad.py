import curses


class GamePadCommand(object):

    def up(self):
        pass

    def right(self):
        pass

    def down(self):
        pass

    def left(self):
        pass

    def action(self):
        pass


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

        self.command = None

    def input(self):
        key = self._input_key()
        if key in self.buttons[self.UP]:
            self.command.up()
        elif key in self.buttons[self.DOWN]:
            self.command.down()
        if key in self.buttons[self.LEFT]:
            self.command.left()
        elif key in self.buttons[self.RIGHT]:
            self.command.right()
        if key in self.buttons[self.ACTION]:
            self.command.action()

    def _input_key(self):
        key = self.stdscr.getch()
        curses.flushinp()
        return key
