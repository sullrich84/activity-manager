from textual import work
from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.widgets import Footer, Header, LoadingIndicator

from src.data.ActivityDatabase import ActivityDatabase
from lib.GarminRepository import GarminRepository
from src.message import BusyMessage, FilterMessage, DataMessage
from src.ui.widgets import ActivityFilter, ActivityTable


class ActivityScreen(Screen):
    CSS = """
        Screen { 
            layout: vertical; 
        }
        
        ActivityFilter { 
            dock: top; 
        }

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
            width: 100%;
            height: 5;
            layer: 10;
            background: $panel;
        }

        Center {
            layer: 10;
            display: none;
            margin: 0 60;
        }

        DateInput {
            width: 14;
            padding: 0 1 0 2;
        }
    """

    DATABASE = ActivityDatabase()
    REPOSITORY = GarminRepository()

    def compose(self) -> ComposeResult:
        self.title = "Garmin Connect Manager"
        yield Header()
        yield Middle(
            ActivityFilter(),
            Center(LoadingIndicator(), id="loading_indicator"),
            ActivityTable(),
        )
        yield Footer()

    # --- Event Handler ---

    def on_filter_message(self, message: FilterMessage) -> None:
        """
        Triggers refetch of activities respecting new start and end date
        """
        self.update_activities(message.start_date, message.end_date)

    def on_busy_message(self, message: BusyMessage) -> None:
        """
        Updates the loading spinner
        """
        self.show_loading_indicator(message.busy)

    def on_data_message(self, message: DataMessage) -> None:
        """
        Updates the activity table
        """
        tab = self.query_one(ActivityTable)
        tab.set_data(message.data)

    # --- I/O Methods ---

    @work(exclusive=True, thread=True)
    async def update_activities(self, start_date: str, end_date: str | None):
        """
        Fetches activities asynchronously
        """
        self.post_message(BusyMessage(True))
        try:
            activities = self.REPOSITORY.get_activities(start_date, end_date)
            self.post_message(DataMessage(activities))
        except Exception as e:
            self.app.notify(f"Error fetching activities: {e}", severity="error")
        finally:
            self.post_message(BusyMessage(False))

    # --- Utility Methods ---

    def show_loading_indicator(self, display: bool):
        indicator = self.query_one("#loading_indicator")
        indicator.display = display
