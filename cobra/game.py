import sys
import curses

from cobra.model import Snake, SnakeListener


class SnakeRenderer(SnakeListener):

    def __init__(self):
        super(SnakeRenderer, self).__init__()

        self._draw_list = []
        self._dirty_list = []

    def body_updated(self, body):
        self._draw_list = list(body)

    def head_updated(self, head):
        self._draw_list.append(head)

    def tail_updated(self, tail):
        self._dirty_list.append(tail)

    def draw(self, stdscr):
        for x, y in self._draw_list:
            stdscr.addch(y, x, '#')

        for x, y in self._dirty_list:
            stdscr.addch(y, x, ' ')

        self._draw_list = []
        self._dirty_list = []


class Game(object):

    def __init__(self):
        super(Game, self).__init__()

        self.stdscr = None
        self._window_size = []

        self._running = True
        self._error_code = 0

        self.snake = None
        self.snake_renderer = None

    @property
    def window_size(self):
        return self._window_size

    def exit(self, error_code=0):
        self._error_code = error_code
        self._running = False

    def create(self):
        size = 5
        x, y = self.window_size[1] / 2 - size, self.window_size[0] / 2
        self.snake = Snake([(x+i, y) for i in xrange(size)])
        self.snake_renderer = SnakeRenderer()
        self.snake.listener = self.snake_renderer

    def dispose(self):
        pass

    def update(self):
        curses.napms(200)

        key = self.stdscr.getch()
        curses.flushinp()

        if key == curses.KEY_UP:
            self.snake.direction = Snake.UP
        elif key == curses.KEY_RIGHT:
            self.snake.direction = Snake.RIGHT
        elif key == curses.KEY_DOWN:
            self.snake.direction = Snake.DOWN
        elif key == curses.KEY_LEFT:
            self.snake.direction = Snake.LEFT

        self.snake.update()
        self.snake_renderer.draw(self.stdscr)

        self.stdscr.refresh()

    def _setup(self, stdscr, args):
        curses.resizeterm(24, 80)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)
        stdscr.nodelay(True)
        stdscr.border()

        self.stdscr = stdscr
        self._window_size = stdscr.getmaxyx()

    def _run(self, stdscr, args):
        self._setup(stdscr, args)

        self.create()
        while self._running:
            self.update()

        self.dispose()

        sys.exit(self._error_code)

    def run(self):
        curses.wrapper(self._run, sys.argv)
