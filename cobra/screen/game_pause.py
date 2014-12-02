from cobra.screen import CursesScreen


class GamePauseScreen(CursesScreen):

    def __init__(self, application, game_screen):
        CursesScreen.__init__(self, application)

        self.game_screen = game_screen

    def show(self):
        pass

    def hide(self):
        pass

    def dispose(self):
        pass

    def update(self, delta):
        pass
