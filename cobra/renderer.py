import logging
logger = logging.getLogger(__name__)

from cobra.model import SnakeListener, WorldListener


class Renderer(object):

    def render(self):
        pass


class CursesUpdateContext(object):

    def __init__(self):
        self.score = None
        self.food = ()
        self.bounds = ()
        self.updated_parts = ()
        self.removed_parts = ()


class CursesRenderer(Renderer, SnakeListener, WorldListener):

    def __init__(self, stdscr):
        super(CursesRenderer, self).__init__()

        self.stdscr = stdscr

        self.context = CursesUpdateContext()

    def snake_updated_parts(self, parts):
        self.context.updated_parts = parts

    def snake_removed_parts(self, parts):
        self.context.removed_parts = parts

    def world_started(self, world):
        self.context.bounds = world.bounds
        self.context.score = world.score
        self.context.food = world.food

    def world_finished(self, world):
        self.context.bounds = world.bounds
        self.context.score = world.score
        logger.info("DEAD")

    def food_created(self, world):
        self.context.food = world.food

    def score_updated(self, world):
        self.context.score = world.score
        logger.info("Score updated to {}".format(world.score))

    def render(self):
        self._render_snake()
        self._render_bounds()
        self._render_score()
        self._render_food()

    def _render_snake(self):
        for x, y in self.context.removed_parts:
            self.stdscr.addch(y, x, ' ')

        for x, y in self.context.updated_parts:
            self.stdscr.addch(y, x, '#')

        self.context.updated_parts = ()
        self.context.removed_parts = ()

    def _render_bounds(self):
        if self.context.bounds:
            bounds = self.context.bounds
            self.stdscr.border('|', '|', ' ', '-', ' ', ' ', '+', '+')
            top_bar = "+{}+".format('-' * (bounds[2]))
            self.stdscr.addstr(bounds[1] - 1, 0, top_bar)
            self.context.bounds = ()

    def _render_score(self):
        if self.context.score != None:
            self.stdscr.addstr(0, 0, "Score: {}".format(self.context.score))
            self.context.score = 0

    def _render_food(self):
        if self.context.food:
            x, y = self.context.food
            self.stdscr.addch(y, x, '*')
            self.context.food = ()
