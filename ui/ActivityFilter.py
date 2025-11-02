from datetime import date, timedelta
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Label
from ui.DateInput import DateInput


class ActivityFilter(HorizontalGroup):
    DEFAULT_CSS = """
        ActivityFilter {
            height: auto;
            align: left middle;
            background: $panel-darken-1;
            border-top: heavy $surface-lighten-3;
            border-bottom: heavy $surface-lighten-3;
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
        self.border_title = " 󰈳 [italic]Filter[/italic] "
        placeholder = date.today().strftime(self.DATE_FORMAT)
        start_date = (date.today() - timedelta(weeks=12)).strftime(self.DATE_FORMAT)

        yield Label("󱙭  Start Date")
        yield DateInput(
            id="start_date",
            name="start_date",
            placeholder=placeholder,
            value=start_date,
            compact=True,
            max_length=10,
        )

        yield Label("󱙬  End Date")
        yield DateInput(
            id="end_date",
            name="end_date",
            placeholder=placeholder,
            valid_empty=True,
            compact=True,
            max_length=10,
        )

        return super().compose()
