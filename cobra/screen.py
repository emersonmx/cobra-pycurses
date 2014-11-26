import curses
import logging
logger = logging.getLogger(__name__)

from cobra.model import WorldConfig, World, Snake
from cobra.renderer import CursesRenderer
from cobra.gamepad import GamePad, CursesGamePad


class Screen(object):

    def show(self):
        pass

    def hide(self):
        pass

    def dispose(self):
        pass

    def update(self, delta):
        pass


class BaseScreen(Screen):

    def __init__(self, application):
        self.application = application

    @property
    def gamepad(self):
        return self.application.gamepad


class CursesScreen(BaseScreen):

    def __init__(self, application):
        BaseScreen.__init__(self, application)

    @property
    def stdscr(self):
        return self.application.stdscr

    @property
    def window_size(self):
        return self.application.window_size


class GameScreen(CursesScreen):

    def __init__(self, application):
        CursesScreen.__init__(self, application)

        self.world = None
        self.renderer = None

        self._paused = False

        self.create()

    def create(self):
        self._create_renderer()
        self._create_world()

    def _create_renderer(self):
        self.renderer = CursesRenderer(self.stdscr)

    def _create_world(self):
        config = self._create_world_config()
        self.world = World(config)
        self.world.snake = self._create_snake()
        self.world.listener = self.renderer
        self.world.create()

    def _create_world_config(self):
        return WorldConfig()

    def _create_snake(self):
        size = 5
        x, y = self.window_size[1] / 2, self.window_size[0] / 2
        snake = Snake([(x-i, y) for i in xrange(size)])
        logger.info("Snake body {}".format(str(snake.body)))
        snake.listener = self.renderer
        return snake

    def show(self):
        self.stdscr.nodelay(True)
        self.stdscr.clear()
        self._setup_gamepad()

    def _setup_gamepad(self):
        snake = self.world.snake
        def snake_up():
            snake.direction = Snake.UP
        def snake_right():
            snake.direction = Snake.RIGHT
        def snake_down():
            snake.direction = Snake.DOWN
        def snake_left():
            snake.direction = Snake.LEFT
        def pause():
            self._paused = not self._paused
            logger.info("Pause Menu")

        self.gamepad.commands[GamePad.UP] = snake_up
        self.gamepad.commands[GamePad.RIGHT] = snake_right
        self.gamepad.commands[GamePad.DOWN] = snake_down
        self.gamepad.commands[GamePad.LEFT] = snake_left
        self.gamepad.commands[GamePad.BACK] = pause

    def hide(self):
        self.gamepad.reset_commands()
        self.stdscr.nodelay(False)

    def update(self, delta):
        curses.napms(10)

        self.gamepad.input()
        if not self._paused:
            self.world.update(delta)
        self.renderer.render()

        self.stdscr.refresh()
