from textual import on, work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Center, Middle
from textual.widgets import Footer, Header, LoadingIndicator
from textual.reactive import reactive
from activity_manager.repositories.GarminRepository import GarminRepository
from activity_manager.data.ActivityStore import ActivityStore
from activity_manager.ui.widgets.ActivityFilter import ActivityFilter
from activity_manager.ui.widgets.ActivityTable import ActivityTable
from activity_manager.ui.widgets.DateInput import DateInput
from debouncer import debounce


class MainScreen(Screen):
    is_loading = reactive(False)

    def __init__(self):
        super().__init__()
        self.start_date = None
        self.end_date = None
        self.store = ActivityStore()
        self.garmin_repository = GarminRepository()

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

    def compose(self) -> ComposeResult:
        self.title = "Garmin Connect Manager"
        yield Header()
        yield Middle(
            ActivityFilter(),
            Center(LoadingIndicator(), id="loading_indicator"),
            ActivityTable(),
        )
        yield Footer()

    def on_mount(self) -> None:
        """
        Called when screen is mounted - load initial activities
        """
        self.store.subscribe(self.on_store_update)
        self.on_store_update()

        start_date_input = self.query_one("#start_date", DateInput)
        if start_date_input.value:
            self.start_date = start_date_input.value
            self.update_activities()

    def on_unmount(self) -> None:
        """
        Called when screen is unmounted - cleanup
        """
        self.store.unsubscribe(self.on_store_update)

    @debounce(wait=0.3)
    @on(DateInput.Changed, "#start_date")
    def update_start_date(self, event: DateInput.Changed):
        if event.validation_result and event.validation_result.is_valid and event.value:
            self.start_date = event.value
            self.update_activities()

    @debounce(wait=0.3)
    @on(DateInput.Changed, "#end_date")
    def update_end_date(self, event: DateInput.Changed):
        if event.validation_result and event.validation_result.is_valid and event.value:
            self.end_date = event.value
            self.update_activities()

    def watch_is_loading(self, is_loading: bool) -> None:
        """
        Automatically called when is_loading changes
        """
        indicator = self.query_one("#loading_indicator")
        indicator.display = is_loading

    def on_store_update(self):
        """
        Called whenever the store is updated
        """
        try:
            activities = self.store.get_all_activities()
            self.query_one(ActivityTable).set_data(activities)
        except Exception as e:
            self.app.notify(f"Error updating from store: {e}", severity="error")

    @work(exclusive=True, thread=True)
    async def update_activities(self):
        if not self.start_date:
            return

        self.is_loading = True
        try:
            # Fetch from Garmin - automatically updates store and triggers UI update
            self.garmin_repository.get_activities(self.start_date)
        except Exception as e:
            self.app.notify(f"Error fetching activities: {e}", severity="error")
        finally:
            self.is_loading = False
