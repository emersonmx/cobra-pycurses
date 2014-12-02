from cobra.screen import Screen


class CursesScreen(Screen):

    def __init__(self, application):
        self.application = application

    @property
    def gamepad(self):
        return self.application.gamepad

    @property
    def stdscr(self):
        return self.application.stdscr

    @property
    def window_size(self):
        return self.application.window_size

    def show(self):
        self.gamepad.reset_commands()
        self.setup_gamepad()

    def setup_gamepad(self):
        pass
