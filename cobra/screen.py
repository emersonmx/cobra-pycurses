import curses
import logging
logger = logging.getLogger(__name__)

from cobra.model import WorldConfig, World, Snake
from cobra.renderer import CursesRenderer
from cobra.gamepad import GamePad


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

    @property
    def stdscr(self):
        return self.application.stdscr

    @property
    def window_size(self):
        return self.application.window_size


class GameScreen(BaseScreen):

    def __init__(self, application):
        BaseScreen.__init__(self, application)

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
        x, y = int(self.window_size[1] / 2), int(self.window_size[0] / 2)
        snake = Snake([(x-i, y) for i in range(size)])
        logger.info("Snake body {}".format(str(snake.body)))
        snake.listener = self.renderer
        return snake

    def show(self):
        self.stdscr.nodelay(True)
        self.stdscr.clear()
        self._setup_gamepad()

    def _setup_gamepad(self):
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

    def hide(self):
        self.gamepad.reset_commands()
        self.stdscr.nodelay(False)

    def update(self, delta):
        curses.napms(10)

        self.process_input()
        if not self._paused:
            self.world.update(delta)

        self.render()

    def process_input(self):
        self.gamepad.process_input()

    def render(self):
        self.renderer.render()
        self.stdscr.refresh()


class GamePauseScreen(BaseScreen):

    def __init__(self, application, game_screen):
        BaseScreen.__init__(self, application)

        self.game_screen = game_screen

    def show(self):
        pass

    def hide(self):
        pass

    def dispose(self):
        pass

    def update(self, delta):
        pass
