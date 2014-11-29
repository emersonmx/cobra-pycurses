import curses
import logging
logger = logging.getLogger(__name__)

from cobra.model import SnakeListener, WorldListener


class Renderer(object):

    def render(self):
        pass


class CursesRenderer(Renderer, SnakeListener, WorldListener):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.game_window = None

        self.snake_body = []
        self.score = 0
        self.food = ()

    def snake_body_updated(self, body):
        self.snake_body = body

    def world_started(self, world):
        x, y, width, height = world.bounds
        self.game_window = self.stdscr.derwin(1, 0)

    def world_finished(self, world):
        logger.info("Game Over")

    def food_created(self, world):
        self.food = world.food
        logger.info("I see a yummy food at {} :B".format(self.food))

    def score_updated(self, world):
        self.score = world.score
        logger.info("Score updated to {}".format(self.score))

    def render(self):
        self.stdscr.clear()
        self._render_score()
        self._render_food()
        self._render_snake_body()
        self._render_game_window_border()
        self._update_screen()

    def _render_score(self):
        self.stdscr.addstr(0, 0, "Score: {}".format(self.score))

    def _render_food(self):
        x, y = self.food
        self.game_window.addch(y + 1, x + 1, '*')

    def _render_snake_body(self):
        for x, y in self.snake_body:
            self.game_window.addch(y + 1, x + 1, '#')

    def _render_game_window_border(self):
        self.game_window.border()

    def _update_screen(self):
        self.stdscr.noutrefresh()
        self.game_window.noutrefresh()
        curses.doupdate()
