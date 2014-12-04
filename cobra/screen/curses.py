from cobra.screen.base import Screen


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

    def update(self, delta):
        self.process_input()
        self.process_logic(delta)
        self.render()

    def process_input(self):
        self.gamepad.process_input()

    def process_logic(self, delta):
        pass

    def render(self):
        pass
