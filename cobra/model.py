import logging
logger = logging.getLogger(__name__)

from random import randint
from collections import deque


class SnakeListener(object):

    def snake_updated(self, snake):
        pass


class Snake(object):

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    DIRECTION_SIZE = 4

    def __init__(self, body):
        super(Snake, self).__init__()

        self.body = deque(body)
        self._direction = self.RIGHT
        self.dead = False

        self._listener = SnakeListener()

    @property
    def head(self):
        return self.body[0]

    @property
    def tail(self):
        return self.body[-1]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if self._can_turn(direction):
            self._direction = direction

    def _can_turn(self, direction):
        return ((direction + self._direction) % 2) == 1

    @property
    def listener(self):
        return self._listener

    @listener.setter
    def listener(self, listener):
        self._listener = listener
        self._listener.snake_updated(self)

    def eat(self):
        self.body.append(self.tail)

    def check_hit_bounds(self, bounds):
        if self.head[0] < bounds[0]:
            return True
        if self.head[0] > bounds[2]:
            return True
        if self.head[1] < bounds[1]:
            return True
        if self.head[1] > bounds[3]:
            return True

        return False

    def check_bitten(self):
        if self.body.count(self.head) > 1:
            return True

        return False

    def check_can_eat(self, food):
        if food.position == self.head:
            return True

        return False

    def update(self):
        if not self.dead:
            head = self._move()
            self.body.appendleft(head)
            self.listener.snake_updated(self)
            self.body.pop()

    def _move(self):
        x, y = self.head
        if self.direction == self.UP:
            y -= 1
        elif self.direction == self.DOWN:
            y += 1
        elif self.direction == self.LEFT:
            x -= 1
        elif self.direction == self.RIGHT:
            x += 1

        return (x, y)


class Food(object):

    def __init__(self, position, score_value=100):
        super(Food, self).__init__()

        self.position = position
        self.score_value = score_value


class GameListener(object):

    def game_started(self, stage):
        pass

    def game_finished(self, stage):
        pass

    def food_created(self, stage):
        pass

    def score_updated(self, stage):
        pass


class Game(object):

    EASY = 1
    NORMAL = 2
    HARD = 4
    VERY_HARD = 5

    def __init__(self):
        super(Game, self).__init__()

        self.dificulty = self.NORMAL
        self.speed = 200

        self.bounds = (1, 2, 78, 22)
        self.score = 0

        self.snake = None
        self.food = None

        self.listener = GameListener()

    def create(self):
        self.food = self._create_food()

        self.listener.game_started(self)
        self.listener.food_created(self)
        self.listener.score_updated(self)

    def _create_food(self):
        # TODO: Move to Food class.
        attemps = 3
        food_score = 100
        for _ in xrange(attemps):
            x = randint(self.bounds[0], self.bounds[2])
            y = randint(self.bounds[1], self.bounds[3])
            point = (x, y)
            if point not in self.snake.body:
                return Food(point, food_score)

        return Food(self._find_closest_tail_position(),
                    food_score * self.dificulty)

    def _find_closest_tail_position(self):
        # TODO: Rename to a better name.
        tail = self.snake.tail
        left = (tail[0] - 1, tail[1])
        right = (tail[0] + 1, tail[1])
        up = (tail[0], tail[1] - 1)
        down = (tail[0], tail[1] + 1)

        if self._food_position_is_valid(left):
            return left
        if self._food_position_is_valid(right):
            return right
        if self._food_position_is_valid(up):
            return up
        if self._food_position_is_valid(down):
            return down

    def _food_position_is_valid(self, position):
        return position not in self.snake.body and self._inside_bounds(position)

    def _inside_bounds(self, point):
        if self.bounds[0] < point[0] < self.bounds[2]:
            return True
        if self.bounds[1] < point[1] < self.bounds[3]:
            return True

        return False

    def update_delay(self):
        return self.speed / self.dificulty

    def update(self):
        self.snake.update()

        if self.snake.check_hit_bounds(self.bounds):
            self.snake.dead = True
            self.listener.game_finished(self)
        if self.snake.check_bitten():
            self.snake.dead = True
            self.listener.game_finished(self)
        if self.snake.check_can_eat(self.food):
            self.snake.eat()

            self.score += self.food.score_value
            self.food = self._create_food()

            self.listener.food_created(self)
            self.listener.score_updated(self)
