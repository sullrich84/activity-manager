from os import get_terminal_size
from textual.app import ComposeResult
from textual.widgets import DataTable, LoadingIndicator, Static
from lib.GarminRepository import GarminRepository


class UiActivityTable(DataTable):
    DEFAULT_CSS = """
        UiActivityTable {
            width: 100%;
            height: 100%;
        }
    """

    COLS = {
        "Date": 19,
        "ID": 11,
        " ": 2,
        "Name": None,
        "Distance": 8,
        "Duration": 8,
    }

    REPOSITORY = GarminRepository()

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

    def get_name_column_width(self):
        taken_size = sum(w for w in self.COLS.values() if w != None)
        gaps = self.COLS.__len__() * 2
        term_size = get_terminal_size().columns
        return term_size - taken_size - gaps
