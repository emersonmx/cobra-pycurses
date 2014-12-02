import curses
import logging
logger = logging.getLogger(__name__)

from cobra.gamepad import GamePad
from cobra.screen import CursesScreen
from cobra.model import World, WorldConfig, Snake
from cobra.model import WorldListener, SnakeListener
from cobra.util import sleep


class GameScreen(CursesScreen, SnakeListener, WorldListener):

    def __init__(self, application):
        CursesScreen.__init__(self, application)

        self.world = None
        self.game_window = None

        self.snake_body = []
        self.score = 0
        self.food = ()

        self.create()

    def create(self):
        self._create_world()
        self._setup_listener()
        self._create_game_window()

    def _create_world(self):
        config = self._create_world_config()
        self.world = World(config)
        self.world.create()

    def _create_world_config(self):
        return WorldConfig()

    def _setup_listener(self):
        self.world.listener = self
        self.world.snake.listener = self

    def _create_game_window(self):
        self.game_window = self.stdscr.derwin(1, 0)

    def setup_gamepad(self):
        def snake_up():
            self.world.snake.direction = Snake.UP
        def snake_right():
            self.world.snake.direction = Snake.RIGHT
        def snake_down():
            self.world.snake.direction = Snake.DOWN
        def snake_left():
            self.world.snake.direction = Snake.LEFT
        def pause():
            self.application.screen = GamePauseScreen(self.application, self)
            logger.info("Pause Menu")

        self.gamepad.commands[GamePad.UP] = snake_up
        self.gamepad.commands[GamePad.RIGHT] = snake_right
        self.gamepad.commands[GamePad.DOWN] = snake_down
        self.gamepad.commands[GamePad.LEFT] = snake_left
        self.gamepad.commands[GamePad.BACK] = pause

    def update(self, delta):
        sleep()

        self.process_input()
        self.world.update(delta)

        self._render()

    def process_input(self):
        self.gamepad.process_input()

    def _render(self):
        self.stdscr.clear()
        self.render_screen()
        self._update_screen()

    def render_screen(self):
        self._render_score()
        self._render_food()
        self._render_snake_body()
        self._render_game_window_border()

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

    def snake_body_updated(self, body):
        self.snake_body = body

    def world_started(self, world):
        x, y, width, height = world.bounds

    def world_finished(self, world):
        logger.info("Game Over")

    def food_created(self, world):
        self.food = world.food
        logger.info("I see a yummy food at {} :B".format(self.food))

    def score_updated(self, world):
        self.score = world.score
        logger.info("Score updated to {}".format(self.score))

from cobra.screen.game_pause import GamePauseScreen
