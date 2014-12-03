from collections import deque


class SnakeListener(object):

    def snake_body_updated(self, body):
        pass


class Snake(object):

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    DIRECTION_SIZE = 4

    def __init__(self, body):
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
        if self.can_turn(direction):
            self._input_direction = direction

    def can_turn(self, direction):
        return ((direction + self._direction) % 2) == 1

    @property
    def listener(self):
        return self._listener

    @listener.setter
    def listener(self, listener):
        self._listener = listener
        self._listener.snake_body_updated(self.body)

    def eat(self):
        self.body.append(self.tail)

    def update(self):
        self._direction = self._input_direction
        head = self.move()
        self.body.appendleft(head)
        self.body.pop()

        self._listener.snake_body_updated(self.body)

    def move(self):
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

    def check_snake_hit_walls(self, bounds):
        if (bounds[0] <= self.head[0] <= bounds[2] and
                bounds[1] <= self.head[1] <= bounds[3]):
            return False

        return True

    def check_bitten(self):
        if self.body.count(self.head) > 1:
            return True

        return False

    def check_can_eat(self, food):
        if food == self.head:
            return True

        return False
