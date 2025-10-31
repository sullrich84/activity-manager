from datetime import date
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Label
from ui.DateInput import DateInput


class ActivityFilter(HorizontalGroup):
    DEFAULT_CSS = """
        ActivityFilter {
            height: auto;
            align: left middle;
            background: $panel;
            border-top: heavy $surface;
            border-bottom: heavy $surface;
        }

        Label {
            padding: 0 1;
        }
    """

    BINDINGS = [
        ("s", "focus('#start_date')", "start date"),
        ("e", "focus('#end_date')", "end date"),
    ]

    DATE_FORMAT = "%Y-%m-%d"

    def compose(self) -> ComposeResult:
        today = date.today()
        start_value = today.replace(day=1).strftime(self.DATE_FORMAT)
        end_value = today.strftime(self.DATE_FORMAT)

        yield Label("󱙭  Start Date")
        yield DateInput(
            id="start_date",
            name="start_date",
            placeholder=start_value,
            value=start_value,
            compact=True,
            max_length=10,
        )

        yield Label("󱙬  End Date")
        yield DateInput(
            id="end_date",
            name="end_date",
            placeholder=end_value,
            valid_empty=True,
            compact=True,
            max_length=10,
        )

        return super().compose()
