import sys
import curses
import logging
logger = logging.getLogger(__name__)

from cobra.model import Cobra, Snake
from cobra.view import CursesView
from cobra.gamepad import GamePad


class Screen(object):

    def __init__(self, game):
        super(Screen, self).__init__()

        self.game = game
        self.stdscr = game.stdscr
        self.window_size = game.window_size

    def create(self):
        pass

    def dispose(self):
        pass

    def update(self):
        pass


class GameScreen(Screen):

    def __init__(self, game):
        super(GameScreen, self).__init__(game)

        self.cobra = None
        self.view = None
        self.gamepad = None

    def create(self):
        self.view = CursesView(self.stdscr)
        self.create_cobra()
        self.create_gamepad()

    def create_cobra(self):
        self.cobra = Cobra()
        self.cobra.snake = self.create_snake()
        self.cobra.listener = self.view
        self.cobra.create()

    def create_snake(self):
        size = 5
        x, y = self.window_size[1] / 2 - size, self.window_size[0] / 2
        snake = Snake([(x+i, y) for i in xrange(size)])
        snake.listener = self.view
        return snake

    def create_gamepad(self):
        snake = self.cobra.snake
        def snake_up(): snake.direction = Snake.UP
        def snake_right(): snake.direction = Snake.RIGHT
        def snake_down(): snake.direction = Snake.DOWN
        def snake_left(): snake.direction = Snake.LEFT
        def pause(): logger.info("PAUSE")

        self.gamepad = GamePad(self.stdscr)
        self.gamepad.bind_command(GamePad.UP, snake_up)
        self.gamepad.bind_command(GamePad.RIGHT, snake_right)
        self.gamepad.bind_command(GamePad.DOWN, snake_down)
        self.gamepad.bind_command(GamePad.LEFT, snake_left)
        self.gamepad.bind_command(GamePad.ACTION, pause)

    def update(self):
        curses.napms(self.cobra.game_speed / self.cobra.game_dificulty)

        self.gamepad.input()
        self.cobra.update()
        self.view.draw()

        self.stdscr.refresh()
