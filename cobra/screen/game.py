from cobra.screen.screen import Screen


class Game(Screen):

    def __init__(self, game):
        super(Game, self).__init__(game)

    def create(self):
        pass

    def update(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Game running...")
        self.stdscr.refresh()
