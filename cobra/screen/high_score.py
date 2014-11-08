from cobra.screen.screen import Screen


class HighScore(Screen):

    def __init__(self, game):
        super(HighScore, self).__init__(game)

    def create(self):
        pass

    def update(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "High Scores")
        self.stdscr.refresh()
