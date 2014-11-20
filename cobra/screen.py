import sys
import curses

from cobra.model import Snake
from cobra.renderer import SnakeRenderer
from cobra.gamepad import GamePad, GamePadCommand


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


class GameScreenCommand(GamePadCommand):

    def __init__(self, game_screen):
        super(GameScreenCommand, self).__init__()

        self.game_screen = game_screen
        self.snake = game_screen.snake

    def up(self):
        self.snake.direction = Snake.UP

    def right(self):
        self.snake.direction = Snake.RIGHT

    def down(self):
        self.snake.direction = Snake.DOWN

    def left(self):
        self.snake.direction = Snake.LEFT

    def action(self):
        self.game_screen.show_menu()


class GameScreen(Screen):

    def __init__(self, game):
        super(GameScreen, self).__init__(game)

        self.snake = None
        self.score_text = None

        self.gamepad = None

    def show_menu(self):
        self.stdscr.addstr(0, 0, "MENU")

    def create(self):
        size = 5
        x, y = self.window_size[1] / 2 - size, self.window_size[0] / 2
        self.snake = Snake([(x+i, y) for i in xrange(size)])
        self.snake_renderer = SnakeRenderer(self.stdscr)
        self.snake.listener = self.snake_renderer

        self.gamepad = GamePad(self.stdscr)
        self.gamepad.command = GameScreenCommand(self)

    def update(self):
        curses.napms(200)

        self.gamepad.input()

        self.snake.update()
        self.snake_renderer.draw()

        self.stdscr.refresh()
