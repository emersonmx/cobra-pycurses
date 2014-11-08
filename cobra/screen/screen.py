class Screen(object):

    def __init__(self, game):
        super(Screen, self).__init__()

        self._game = game
        self.stdscr = game.stdscr

    @property
    def game(self):
        return self._game

    def create(self):
        pass

    def dispose(self):
        pass

    def update(self):
        pass
