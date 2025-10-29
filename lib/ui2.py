from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import DataTable

from lib.models import ActivityItem


class Ui(App):
    CSS = """
    DataTable {
        width: 100%;
        height: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_ready(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Date", "ID", "Status", "Name", "Distance [m]", "Duration")

    def add_activity(self, item: ActivityItem):
        table = self.query_one(DataTable)
        table.add_row(("foo", "bar", "baz", "bing", "bong"))


if __name__ == "__main__":
    Ui().run()
