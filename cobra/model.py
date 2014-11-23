from random import randint
from collections import deque


class SnakeListener(object):

    def body_updated(self, body):
        pass

    def head_updated(self, head):
        pass

    def tail_updated(self, tail):
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
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if self._can_turn(value):
            self._direction = value

    def _can_turn(self, direction):
        return ((direction + self._direction) % 2) == 1

    @property
    def listener(self):
        return self._listener

    @listener.setter
    def listener(self, value):
        self._listener = value
        self._listener.body_updated(self.body)

    def eat_food(self):
        self.body.appendleft(self.body[0])

    def update(self):
        if not self.dead:
            head = self._move(self.body[-1])
            tail = self.body.popleft()
            self.body.append(head)

            self.listener.head_updated(head)
            self.listener.tail_updated(tail)

    def _move(self, right):
        head = [right[0], right[1]]
        if self.direction == self.UP:
            head[1] -= 1
        elif self.direction == self.DOWN:
            head[1] += 1
        elif self.direction == self.LEFT:
            head[0] -= 1
        elif self.direction == self.RIGHT:
            head[0] += 1

        return head


class Food(object):

    def __init__(self, position, score_value=100):
        super(Food, self).__init__()

        self.position = position
        self.score_value = score_value


class StageListener(object):

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

        self.listener = StageListener()

    def create(self):
        self.food = self.create_food()

        self.listener.game_started(self)
        self.listener.food_created(self)
        self.listener.score_updated(self)

    def create_food(self):
        attemps = 3
        food_score = 100
        for _ in xrange(attemps):
            x = randint(self.bounds[0], self.bounds[2])
            y = randint(self.bounds[1], self.bounds[3])
            point = [x, y]
            if point not in self.snake.body:
                return Food(point, food_score * self.dificulty)

        return Food(self._find_closest_tail_position(),
                    food_score * self.dificulty)

    def _find_closest_tail_position(self):
        tail = self.snake.body[0]
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

        if self._snake_collide_wall():
            self.snake.dead = True
            self.listener.game_finished(self)
        if self._snake_collide_herself():
            self.snake.dead = True
            self.listener.game_finished(self)
        if self._snake_collide_food():
            self.snake.eat_food()

            self.score += self.food.score_value
            self.food = self.create_food()

            self.listener.food_created(self)
            self.listener.score_updated(self)

    def _snake_collide_wall(self):
        head = self.snake.body[-1]
        if head[0] < self.bounds[0]:
            return True
        if head[0] > self.bounds[2]:
            return True
        if head[1] < self.bounds[1]:
            return True
        if head[1] > self.bounds[3]:
            return True

        return False

    def _snake_collide_herself(self):
        head = self.snake.body[-1]
        if self.snake.body.count(head) > 1:
            return True

        return False

    def _snake_collide_food(self):
        head = self.snake.body[-1]
        if ((head[0] == self.food.position[0]) and
                (head[1] == self.food.position[1])):
            return True

        return False
