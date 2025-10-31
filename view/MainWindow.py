from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header
from lib.GarminRepository import GarminRepository
from ui.ActivityFilter import ActivityFilter
from ui.ActivityTable import ActivityTable
from ui.DateInput import DateInput


class MainWindow(App):
    CSS = """
        Screen { layout: vertical; }
        ActivityFilter { dock: top; }

        Header {
            height: auto;
        }

        DataTable {
            width: 100%;
            height: 100%;
        }

        Footer {
            dock: bottom;
        }
    """

    REPOSITORY = GarminRepository()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            ActivityFilter(),
            ActivityTable(),
        )
        yield Footer()

    @on(DateInput.Changed, "#start_date")
    def update_start_date(self, event: DateInput.Changed):
        if event.validation_result and event.validation_result.is_valid:
            self.notify(f"Start Date: {event.value}")

    @on(DateInput.Changed, "#end_date")
    def update_end_date(self, event: DateInput.Changed):
        if event.validation_result and event.validation_result.is_valid:
            self.notify(f"End Date: {event.value}")

    async def on_ready(self) -> None:
        await self.load_activities()

    async def load_activities(self):
        table = self.query_one(ActivityTable)
        for act in self.REPOSITORY.get_activities("2025-10-01"):
            table.add_row(
                act.start_time,
                act.id,
                act.formatted_visibility,
                act.formatted_name,
                act.formatted_distance,
                act.formatted_duration,
            )
