from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Center, Middle
from textual.widgets import Footer, Header, LoadingIndicator
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

        LoadingIndicator {
            width: 20;
            height: 5;
            layer: 10;
            align: center middle;
        }

        Center {
            layer: 10;
            margin: 0 40;
        }

        # This doesn't work when set in ActivityFilter
        DateInput {
            width: 14;
            padding: 0 1 0 2;
        }
    """

    REPOSITORY = GarminRepository()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Middle(
            ActivityFilter(),
            Center(LoadingIndicator()),
            ActivityTable(),
        )
        yield Footer()

    @on(DateInput.Changed, "#start_date")
    def update_start_date(self, event: DateInput.Changed):
        if event.validation_result and event.validation_result.is_valid:
            self.start_date = event.value
            self.update_activities()

    @on(DateInput.Changed, "#end_date")
    def update_end_date(self, event: DateInput.Changed):
        if event.validation_result and event.validation_result.is_valid:
            self.end_date = event.value
            self.update_activities()

    def _show_loading_indicator(self, display: bool):
        self.query_one(LoadingIndicator).display = display

    @work(exclusive=True, thread=True)
    async def update_activities(self):
        self.call_from_thread(self._show_loading_indicator, True)
        try:
            table = self.query_one(ActivityTable)
            table.clear()
            for act in self.REPOSITORY.get_activities(self.start_date):
                table.add_row(
                    act.start_time,
                    act.id,
                    act.formatted_visibility,
                    act.formatted_name,
                    act.formatted_distance,
                    act.formatted_duration,
                )
        except Exception as e:
            self.app.notify(f"Error fetching activities: {e}", severity="error")
        finally:
            self.call_from_thread(self._show_loading_indicator, False)
