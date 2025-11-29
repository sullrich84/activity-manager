from webbrowser import open
from os import get_terminal_size
from typing import TypeAlias

from textual.app import ComposeResult
from textual.widgets import DataTable

from activity_manager.repositories.RaceIdRepository import RaceIdRepository
from activity_manager.models import ActivityModel

ActivityCache: TypeAlias = dict[str, ActivityModel]


class ActivityTable(DataTable):
    DEFAULT_CSS = """
        ActivityTable {
            width: 100%;
            height: 100%;
            scrollbar-visibility: hidden;
        }
    """

    COLS = {
        "Date": 19,
        "ID": 11,
        " ": 1,
        "󰆼 ": 1,
        "Name": None,
        "Distance": 8,
        "Duration": 8,
    }

    BINDINGS = [
        ("g", "scroll_top", "top"),
        ("G", "scroll_bottom", "bottom"),
        ("o", "open_in_web", "open in web"),
        ("s", "sync_with_raceid", "sync with RaceID"),
    ]

    REPOSITORY = RaceIdRepository()

    activity_cache: ActivityCache = {}
    selected_row_key = None

    def compose(self) -> ComposeResult:
        for name, width in self.COLS.items():
            if width == None:
                width = self.get_name_column_width()
            self.add_column(name, key=name, width=width)

        self.cursor_type = "row"
        self.zebra_stripes = True
        return super().compose()

    def on_resize(self) -> None:
        self.columns["Name"].width = self.get_name_column_width()
        self.refresh()

    # --- Action Handler ---

    def action_open_in_web(self) -> None:
        activity_id = self.coordinate_to_cell_key(self.cursor_coordinate).row_key.value
        open(self.activity_cache[activity_id].url)

    def action_sync_with_raceid(self) -> None:
        activity_id = self.coordinate_to_cell_key(self.cursor_coordinate).row_key.value
        activity = self.activity_cache[activity_id]
        if activity:
            try:
                self.REPOSITORY.set_result(activity)
                self.notify(f"Synced `{activity.name}` with RaceID")
            except:
                self.notify(f"Failed to sync `{activity.name}` with RaceID")

    # --- Utility Methods ---

    def set_data(self, activities: list[ActivityModel]) -> None:
        self.activity_cache.clear()
        self.clear()
        for activity in activities:
            self.activity_cache[activity.id] = activity
            self.add_row(
                activity.start_time,
                activity.id,
                activity.visibility_icon,
                activity.sync_icon,
                activity.name,
                activity.formatted_distance,
                activity.formatted_duration,
                key=activity.id,
            )
        self.refresh()

    def get_name_column_width(self) -> None:
        taken_size = sum(w for w in self.COLS.values() if w != None)
        gaps = self.COLS.__len__() * 2
        term_size = get_terminal_size().columns
        return term_size - taken_size - gaps
