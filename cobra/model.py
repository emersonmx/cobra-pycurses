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

        self._listener = None

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

    def update(self):
        head = self._move(self.body[-1])
        self.body.append(head)

        self.listener.head_updated(head)
        self.listener.tail_updated(self.body.popleft())

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
