import logging
logger = logging.getLogger(__name__)

from cobra.model import SnakeListener, WorldListener


class Renderer(object):

    def render(self):
        pass


class CursesRenderer(Renderer, SnakeListener, WorldListener):

    def __init__(self, stdscr):
        super(CursesRenderer, self).__init__()

        # TODO: Too many attributes (8/7).

        self.stdscr = stdscr

        self.world = None
        self.update_bounds = False
        self.score = None
        self.food = None

        self.first = True

        self.updated_parts = []
        self.removed_parts = []

    def snake_updated_parts(self, parts):
        self.updated_parts = parts

    def snake_removed_parts(self, parts):
        self.removed_parts = parts

    def world_started(self, world):
        self.world = world
        self.update_bounds = True
        self.score = world.score
        self.food = world.food

    def world_finished(self, world):
        self.update_bounds = True
        self.score = world.score
        logger.info("DEAD")

    def food_created(self, world):
        self.food = world.food

    def score_updated(self, world):
        self.score = world.score
        logger.info("Score updated to {}".format(self.score))

    def render(self):
        self._render_snake()
        self._render_bounds()
        self._render_score()
        self._render_food()

    def _render_snake(self):
        for x, y in self.removed_parts:
            self.stdscr.addch(y, x, ' ')

        for x, y in self.updated_parts:
            self.stdscr.addch(y, x, '#')

        self.updated_parts = []
        self.removed_parts = []

    def _render_bounds(self):
        if self.update_bounds:
            self.stdscr.border('|', '|', ' ', '-', ' ', ' ', '+', '+')
            bounds = self.world.bounds
            top_bar = "+{}+".format('-' * (bounds[2]))
            self.stdscr.addstr(bounds[1] - 1, 0, top_bar)
            self.update_bounds = False

    def _render_score(self):
        if self.score != None:
            self.stdscr.addstr(0, 0, "Score: {}".format(self.score))
            self.score = None

    def _render_food(self):
        if self.food:
            x, y = self.food
            self.stdscr.addch(y, x, '*')
            self.food = None

