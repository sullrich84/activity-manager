from datetime import date
from json.encoder import encode_basestring
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from ui.UiDateInput import UiDateInput
from ui.UiLabel import UiLabel


class UiActivityFilter(HorizontalGroup):
    DEFAULT_CSS = """
        UiActivityFilter {
            height: auto;
            align: left middle;
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

        yield UiLabel("󱙭  Start Date")
        yield UiDateInput(
            id="start_date",
            name="start_date",
            placeholder=start_value,
            value=start_value,
            compact=True,
            max_length=10,
        )

        yield UiLabel("󱙬  End Date")
        yield UiDateInput(
            id="end_date",
            name="end_date",
            placeholder=end_value,
            value=end_value,
            compact=True,
            max_length=10,
        )

        return super().compose()
