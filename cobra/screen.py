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

    def snake_up(self):
        self.snake.direction = Snake.UP

    def snake_right(self):
        self.snake.direction = Snake.RIGHT

    def snake_down(self):
        self.snake.direction = Snake.DOWN

    def snake_left(self):
        self.snake.direction = Snake.LEFT

    def pause(self):
        self.stdscr.addstr(0, 0, "PAUSE")

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
        self.gamepad = GamePad(self.stdscr)
        self.gamepad.bind_command(GamePad.UP, self.snake_up)
        self.gamepad.bind_command(GamePad.RIGHT, self.snake_right)
        self.gamepad.bind_command(GamePad.DOWN, self.snake_down)
        self.gamepad.bind_command(GamePad.LEFT, self.snake_left)
        self.gamepad.bind_command(GamePad.ACTION, self.pause)

    def update(self):
        curses.napms(200)

        self.gamepad.input()

        self.snake.update()
        self.snake_renderer.draw()

        self.stdscr.refresh()
