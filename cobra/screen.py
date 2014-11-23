import sys
import curses
import logging
logger = logging.getLogger(__name__)

from cobra.model import World, Snake
from cobra.view import CursesView
from cobra.gamepad import GamePad


class Screen(object):

    def create(self):
        pass

    def dispose(self):
        pass

    def update(self):
        pass


class BaseScreen(Screen):

    def __init__(self, application):
        super(BaseScreen, self).__init__()

        self.application = application

    @property
    def stdscr(self):
        return self.application.stdscr

    @property
    def window_size(self):
        return self.application.window_size


class GameScreen(BaseScreen):

    def __init__(self, application):
        super(GameScreen, self).__init__(application)

        self.world = None
        self.view = None
        self.gamepad = None

    def create(self):
        self._setup_curses()
        self._setup_world()

    def _setup_curses(self):
        self.stdscr.nodelay(True)

    def _setup_world(self):
        self.view = CursesView(self.stdscr)
        self._create_world()
        self._create_gamepad()

    def _create_world(self):
        self.world = World()
        self.world.snake = self._create_snake()
        self.world.listener = self.view
        self.world.create()

    def _create_snake(self):
        size = 5
        x, y = self.window_size[1] / 2, self.window_size[0] / 2
        snake = Snake([(x-i, y) for i in xrange(size)])
        logger.info("Snake body {}".format(str(snake.body)))
        snake.listener = self.view
        return snake

    def _create_gamepad(self):
        snake = self.world.snake
        def snake_up(): snake.direction = Snake.UP
        def snake_right(): snake.direction = Snake.RIGHT
        def snake_down(): snake.direction = Snake.DOWN
        def snake_left(): snake.direction = Snake.LEFT
        def pause(): logger.info("Pause Menu")

        self.gamepad = GamePad(self.stdscr)
        self.gamepad.commands[GamePad.UP] = snake_up
        self.gamepad.commands[GamePad.RIGHT] = snake_right
        self.gamepad.commands[GamePad.DOWN] = snake_down
        self.gamepad.commands[GamePad.LEFT] = snake_left
        self.gamepad.commands[GamePad.BACK] = pause

    def dispose(self):
        self.stdscr.nodelay(False)

    def update(self):
        curses.napms(self.world.update_delay())

        self.gamepad.input()
        self.world.update()
        self.view.draw()

        self.stdscr.refresh()
