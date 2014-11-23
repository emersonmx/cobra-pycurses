import logging
logger = logging.getLogger(__name__)

from cobra.model import SnakeListener, GameListener


class View(object):

    def draw(self):
        pass


class CursesView(View, SnakeListener, GameListener):

    def __init__(self, stdscr):
        super(CursesView, self).__init__()

        self.stdscr = stdscr

        self.stage = None
        self.update_bounds = False
        self.score = None
        self.food = None

        self.first_update = True
        self.body = []
        self.tail = []

    def snake_updated(self, snake):
        if self.first_update:
            self.body = list(snake.body)
            self.first_update = False
        else:
            self.body.append(snake.head)
            self.tail.append(snake.tail)

    def game_started(self, stage):
        self.stage = stage
        self.update_bounds = True
        self.score = stage.score
        self.food = stage.food

    def game_finished(self, stage):
        self.update_bounds = True
        self.score = stage.score
        logger.info("DEAD")

    def food_created(self, stage):
        self.food = stage.food
        logger.info("Snake eat food")

    def score_updated(self, stage):
        self.score = stage.score
        logger.info("Score updated to {}".format(self.score))

    def draw(self):
        self._draw_snake()
        self._draw_bounds()
        self._draw_score()
        self._draw_food()

    def _draw_snake(self):
        for x, y in self.body:
            self.stdscr.addch(y, x, '#')

        for x, y in self.tail:
            self.stdscr.addch(y, x, ' ')

        self.body = []
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

