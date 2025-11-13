from textual.app import App
from src.ui.screens import ActivityScreen


class ActivityManager(App):
    SCREENS = {
        "main": ActivityScreen,
    }

    BINDINGS = [
        ("m", "push_screen('main')", "ActivityScreen"),
    ]

    def on_ready(self) -> None:
        self.push_screen("main")


if __name__ == "__main__":
    ActivityManager().run()
