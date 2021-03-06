import logging
logger = logging.getLogger(__name__)

from random import choice

from cobra.model.snake import Snake


class WorldListener(object):

    def world_started(self, world):
        pass

    def world_finished(self, world):
        pass

    def food_created(self, world):
        pass

    def score_updated(self, world):
        pass


class WorldConfig(object):

    def __init__(self):
        self.bounds = (0, 0, 77, 20)
        self.food_score = 100

        self.tick = 0.2
        self.tick_decrement_ratio = 0.1
        self.speed_boost_at_score = 300


class World(object):

    def __init__(self, config):
        self.config = config

        self.screen_area = ()
        self.game_over = False

        self.snake = None
        self.food = ()
        self.score = 0

        self.tick_time = 0

        self._listener = WorldListener()

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

    @property
    def bounds(self):
        return self.config.bounds

    @bounds.setter
    def bounds(self, bounds):
        self.config.bounds = bounds

    @property
    def listener(self):
        return self._listener

    @listener.setter
    def listener(self, listener):
        self._listener = listener
        self.listener.world_started(self)
        self.listener.score_updated(self)
        self.listener.food_created(self)

    def create(self):
        self.screen_area = self.screen_area_create()
        self.snake = self.create_snake()
        self.food = self.create_food()

    def screen_area_create(self):
        area = []
        for i in range(self.x, self.width + 1):
            for j in range(self.y, self.height + 1):
                area.append((i, j))

        return frozenset(area)

    def create_snake(self):
        size = 5
        x, y = int(self.width / 2), int(self.height / 2)
        snake = Snake([(x-i, y) for i in range(size)])
        logger.info("Snake body {}".format(str(snake.body)))
        return snake

    def create_food(self):
        food_area = list(self.screen_area.difference(self.snake.body))
        if food_area:
            return choice(food_area)

        return ()

    def update(self, delta):
        if not self.game_over:
            self.tick_time += delta
            while self.tick_time > self.config.tick:
                self.tick_time -= self.config.tick
                self.update_world(delta)

    def update_world(self, delta):
        self.snake.update()

        self.check_snake_hit_walls()
        self.check_snake_bitten()
        self.check_snake_eat_food()

        if self.game_over:
            self.listener.world_finished(self)

    def check_snake_hit_walls(self):
        if self.snake.check_snake_hit_walls(self.bounds):
            logger.info("Ouch my head! T.T")
            self.game_over = True

    def check_snake_bitten(self):
        if self.snake.check_bitten():
            logger.info("I'm a oroboros! Yay :D")
            self.game_over = True

    def check_snake_eat_food(self):
        if self.snake.check_can_eat(self.food):
            self.snake.eat()

            self.score += self.config.food_score
            self.listener.score_updated(self)

            self.food = self.create_food()
            if self.food:
                if self.score % self.config.speed_boost_at_score == 0:
                    self.increase_snake_speed()

                self.listener.food_created(self)
            else:
                logger.info("I'm full man... I eat {} foods by the way".format(
                    len(self.snake.body)))
                self.game_over = True

    def increase_snake_speed(self):
        decrement = self.config.tick * self.config.tick_decrement_ratio
        if self.config.tick - decrement > 0:
            self.config.tick -= decrement
            speed = 1. / self.config.tick
            logger.info("Snake speed updated to {} u/s".format(speed))
