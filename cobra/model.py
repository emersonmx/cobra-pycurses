import logging
logger = logging.getLogger(__name__)

from random import choice
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

    def update(self):
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
        if food == self.head:
            return True

        return False


class WorldListener(object):

    def world_started(self, world):
        pass

    def world_finished(self, world):
        pass

    def food_created(self, world):
        pass

    def score_updated(self, world):
        pass


class World(object):

    def __init__(self):
        super(World, self).__init__()
        # TODO: Reduces attributes.

        self.bounds = (1, 2, 78, 22)
        self._screen_area = None
        self.game_over = False

        self.snake = None
        self.food = None
        self.food_score = 100
        self.score = 0

        self._tick_time = 0
        self.tick = 0.2
        self.tick_decrement_ratio = 0.1
        self.score_speed_boost = 300

        self.listener = WorldListener()

    @property
    def x(self):
        return self.bounds[0]

    @x.setter
    def x(self, x):
        self.bounds[0] = x

    @property
    def y(self):
        return self.bounds[1]

    @y.setter
    def y(self, y):
        self.bounds[1] = y

    @property
    def width(self):
        return self.bounds[2]

    @width.setter
    def width(self, width):
        self.bounds[2] = width

    @property
    def height(self):
        return self.bounds[3]

    @height.setter
    def height(self, height):
        self.bounds[3] = height

    def create(self):
        self._screen_area = self._screen_area_create()
        self.food = self._create_food()

        self.listener.world_started(self)
        self.listener.food_created(self)
        self.listener.score_updated(self)

    def _screen_area_create(self):
        area = []
        for i in xrange(self.x, self.width + 1):
            for j in xrange(self.y, self.height + 1):
                area.append((i, j))

        return frozenset(area)

    def _create_food(self):
        food_area = list(self._screen_area.difference(self.snake.body))
        if food_area:
            return choice(food_area)

        return None

    def _inside_bounds(self, point):
        x, y = point
        if self.x < x < self.width:
            return True
        if self.y < y < self.height:
            return True

        return False

    def update(self, delta):
        if not self.game_over:
            self._tick_time += delta
            while self._tick_time > self.tick:
                self._tick_time -= self.tick
                self._update_world(delta)

    def _update_world(self, delta):
        self.snake.update()

        self._check_snake_hit_bounds()
        self._check_snake_bitten()
        self._check_snake_eat_food()

        if self.game_over:
            self.listener.world_finished(self)

    def _check_snake_hit_bounds(self):
        if self.snake.check_hit_bounds(self.bounds):
            logger.info("Ouch my head! T.T")
            self.game_over = True

    def _check_snake_bitten(self):
        if self.snake.check_bitten():
            logger.info("I'm a oroboros! Yay :D")
            self.game_over = True

    def _check_snake_eat_food(self):
        if self.snake.check_can_eat(self.food):
            logger.info("I see a yummy food at {} :B".format(
                self.food))
            self.snake.eat()

            self.score += self.food_score
            self.listener.score_updated(self)

            self.food = self._create_food()
            if self.food:
                #if self.score % self.score_speed_boost == 0:
                    #self._increase_snake_speed()

                self.listener.food_created(self)
            else:
                logger.info("I'm full man... I eat {} foods by the way".format(
                    len(self.snake.body)))
                self.game_over = True

    def _bounds_area(self):
        return (self.width - self.x) * (self.height - self.y)

    def _increase_snake_speed(self):
        decrement = self.tick * self.tick_decrement_ratio
        if self.tick - decrement > 0:
            self.tick -= decrement
            logger.info("Snake speed updated to {} u/s".format(1. / self.tick))
