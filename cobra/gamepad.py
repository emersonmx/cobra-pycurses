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
        self.buttons = self.create_buttons()
        self.commands = self.create_commands()

    def create_buttons(self):
        number_of_buttons = bin(self.ALL_BUTTONS).count('1')
        buttons = [1 << i for i in range(number_of_buttons)]
        return {button: set() for button in buttons}

    def create_commands(self):
        number_of_buttons = bin(self.ALL_BUTTONS).count('1')
        commands = [1 << i for i in range(number_of_buttons)]
        return {command: self.no_command for command in commands}

    def reset_commands(self):
        self.commands = self.create_commands()

    def process_input(self):
        pass


class CursesGamePad(GamePad):

    def __init__(self, stdscr):
        GamePad.__init__(self)

        self.stdscr = stdscr

    def create_buttons(self):
        return {
            self.UP: set([curses.KEY_UP, ord('k')]),
            self.RIGHT: set([curses.KEY_RIGHT, ord('l')]),
            self.DOWN: set([curses.KEY_DOWN, ord('j')]),
            self.LEFT: set([curses.KEY_LEFT, ord('h')]),
            self.ENTER: set([ord('\n'), ord(' ')]),
            self.BACK: set([ord('p')])
        }

    def process_input(self):
        command = GamePad.no_command

        key = self.input_key()
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

    def input_key(self):
        key = self.stdscr.getch()
        return key
