from cobra.model import SnakeListener


class Renderer(object):

    def draw(self):
        pass


class SnakeRenderer(Renderer, SnakeListener):

    def __init__(self, stdscr):
        super(SnakeRenderer, self).__init__()

        self.stdscr = stdscr

        self._draw_list = []
        self._dirty_list = []

    def body_updated(self, body):
        self._draw_list = list(body)

    def head_updated(self, head):
        self._draw_list.append(head)

    def tail_updated(self, tail):
        self._dirty_list.append(tail)

    def draw(self):
        for x, y in self._draw_list:
            self.stdscr.addch(y, x, '#')

        for x, y in self._dirty_list:
            self.stdscr.addch(y, x, ' ')

        self._draw_list = []
        self._dirty_list = []
