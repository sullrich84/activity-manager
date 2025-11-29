from textual.app import App
from activity_manager.ui import MainScreen


class ActivityManager(App):
    SCREENS = {
        "main": MainScreen,
    }

    BINDINGS = [
        ("m", "push_screen('main')", "ActivityScreen"),
    ]

    def on_ready(self) -> None:
        self.push_screen("main")


if __name__ == "__main__":
    ActivityManager().run()
