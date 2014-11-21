import sys
import curses

from cobra.model import Snake
from cobra.renderer import SnakeRenderer
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

        self.snake = None
        self.score_text = None

        self.gamepad = None

    def create(self):
        self.create_snake()
        self.create_gamepad()

    def create_snake(self):
        size = 5
        x, y = self.window_size[1] / 2 - size, self.window_size[0] / 2
        self.snake = Snake([(x+i, y) for i in xrange(size)])
        self.snake_renderer = SnakeRenderer(self.stdscr)
        self.snake.listener = self.snake_renderer

    def create_gamepad(self):
        def snake_up(): self.snake.direction = Snake.UP
        def snake_right(): self.snake.direction = Snake.RIGHT
        def snake_down(): self.snake.direction = Snake.DOWN
        def snake_left(): self.snake.direction = Snake.LEFT
        def pause(): self.stdscr.addstr(0, 0, "PAUSE")

        self.gamepad = GamePad(self.stdscr)
        self.gamepad.bind_command(GamePad.UP, snake_up)
        self.gamepad.bind_command(GamePad.RIGHT, snake_right)
        self.gamepad.bind_command(GamePad.DOWN, snake_down)
        self.gamepad.bind_command(GamePad.LEFT, snake_left)
        self.gamepad.bind_command(GamePad.ACTION, pause)

    def update(self):
        curses.napms(200)

        self.gamepad.input()

        self.snake.update()
        self.snake_renderer.draw()

        self.stdscr.refresh()
