import logging
from cobra.model import SnakeListener, StageListener


class View(object):

    def draw(self):
        pass


class CursesView(View, SnakeListener, StageListener):

    def __init__(self, stdscr):
        super(CursesView, self).__init__()

        self.stdscr = stdscr

        self.stage = None
        self.update_bounds = False
        self.score = None
        self.food = None

        self.body_list = []
        self.tail = []

    def body_updated(self, body):
        self.body_list = list(body)

    def head_updated(self, head):
        self.body_list.append(head)

    def tail_updated(self, tail):
        self.tail.append(tail)

    def draw(self):
        self._draw_snake()
        self._draw_bounds()
        self._draw_score()
        self._draw_food()

    def _draw_snake(self):
        for x, y in self.body_list:
            self.stdscr.addch(y, x, '#')

        for x, y in self.tail:
            self.stdscr.addch(y, x, ' ')

        self.body_list = []
        self.tail = []

    def _draw_bounds(self):
        if self.update_bounds:
            self.stdscr.border('|', '|', ' ', '-', ' ', ' ', '+', '+')
            bounds = self.stage.bounds
            bar = "+{}+".format('-' * (bounds[2]))
            self.stdscr.addstr(bounds[1] - 1, 0, bar)
            self.update_bounds = False

    def _draw_score(self):
        if self.score != None:
            self.stdscr.addstr(0, 0, "Score: {}".format(self.score))
            self.score = None

    def _draw_food(self):
        if self.food:
            bounds = self.stage.bounds
            x, y = self.food.position
            self.stdscr.addch(y, x, '*')
            self.food = None

    def game_started(self, stage):
        self.stage = stage
        self.update_bounds = True
        self.score = stage.score
        self.food = stage.food

    def game_finished(self, stage):
        self.update_bounds = True
        self.score = stage.score
        logging.info("DEAD")

    def food_created(self, stage):
        self.food = stage.food

    def score_updated(self, stage):
        self.score = stage.score
