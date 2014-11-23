import logging
logger = logging.getLogger(__name__)

from random import randint
from collections import deque


class SnakeListener(object):

    def snake_updated_parts(self, parts):
        pass

    def snake_removed_parts(self, parts):
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
        self._input_direction = self._direction

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
            self._input_direction = direction

    def _can_turn(self, direction):
        return ((direction + self._direction) % 2) == 1

    @property
    def listener(self):
        return self._listener

    @listener.setter
    def listener(self, listener):
        self._listener = listener
        self._listener.snake_updated_parts(list(self.body))

    def eat(self):
        self.body.append(self.tail)

    def update(self, delta):
        self._direction = self._input_direction
        head = self._move()
        self.body.appendleft(head)
        tail = self.body.pop()

        self.listener.snake_updated_parts([head, self.tail])
        self.listener.snake_removed_parts([tail])

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


class Food(object):

    def __init__(self, position, score_value=100):
        super(Food, self).__init__()

        self.position = position
        self.score_value = score_value


class WorldListener(object):

    def world_started(self, stage):
        pass

    def world_finished(self, stage):
        pass

    def food_created(self, stage):
        pass

    def score_updated(self, stage):
        pass


class World(object):

    def __init__(self):
        super(World, self).__init__()

        self.bounds = (1, 2, 78, 22)
        self.score = 0
        self.game_over = False

        self.snake = None
        self.food = None

        self.tick_time = 0
        self.tick = 0.4
        self.tick_decrement = 0

        self.listener = WorldListener()

    def create(self):
        self.food = self._create_food()

        self.listener.world_started(self)
        self.listener.food_created(self)
        self.listener.score_updated(self)

        self.tick_decrement = self.tick * 0.1

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

        return Food(self._find_closest_tail_position(), food_score)

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

    def update(self, delta):
        if not self.game_over:
            self.tick_time += delta
            while self.tick_time > self.tick:
                self.tick_time -= self.tick
                self._update_world(delta)

    def _update_world(self, delta):
        self.snake.update(delta)
        logger.info(self.snake.body)

        if self.snake.check_hit_bounds(self.bounds):
            logger.info("Ouch my head! T.T")
            self.game_over = True
            self.listener.world_finished(self)
        if self.snake.check_bitten():
            logger.info("I'm a oroboros! Yay :D")
            self.game_over = True
            self.listener.world_finished(self)
        if self.snake.check_can_eat(self.food):
            logger.info("I see a yummy food at {} :B".format(self.food.position))
            self.snake.eat()

            self.score += self.food.score_value
            self.food = self._create_food()
            self._make_game_harder()

            self.listener.food_created(self)
            self.listener.score_updated(self)

    def _make_game_harder(self):
        if self.score % 300 == 0:
            if self.tick - self.tick_decrement > 0:
                logger.info("FUUU!")
                self.tick -= self.tick_decrement
