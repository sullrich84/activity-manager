from datetime import date, timedelta
from logging import Filter
from debouncer import debounce
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Label
from src.message import FilterMessage
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
            classes="date_selector",
            placeholder=placeholder,
            value=start_date,
            compact=True,
            max_length=10,
        )

        yield Label("󱙬  End Date")
        yield DateInput(
            id="end_date",
            name="end_date",
            classes="date_selector",
            placeholder=placeholder,
            valid_empty=True,
            compact=True,
            max_length=10,
        )

        return super().compose()

    # --- Event Handler ---

    @debounce(wait=0.5)
    @on(DateInput.Changed, ".date_selector")
    def update_date_range(self):
        start_date = self.query_one("#start_date", DateInput)
        end_date = self.query_one("#end_date", DateInput)

        if not start_date.value or not start_date._valid or not end_date._valid:
            return

        if start_date:
            msg = FilterMessage(start_date.value, end_date.value or None)
            self.post_message(msg)
