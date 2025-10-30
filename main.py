import pyperclip
from datetime import timedelta
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Input, Header
from lib.gc import GarminClient


class Ui(App):
    CSS = """
    Screen {
        layout: vertical;
    }

    Input {
        dock: top;
        height: 1;
    }

    DataTable {
        width: 100%;
        height: 100%;
    }

    Footer {
        dock: bottom;
    }
    """

    client = GarminClient()

    def compose(self) -> ComposeResult:
        yield Input(placeholder="2025-10-01", compact=True)
        yield DataTable()
        yield Footer()

    def on_ready(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Date", "ID", "\uf06e", "Name", "Distance", "Duration")
        table.selection_style = "row"
        self.render_table()

    def render_table(self):
        table = self.query_one(DataTable)
        start_date = "2025-10-01"
        for act in self.client.get_activities(start_date):
            if act.privacy == "public":
                name = act.name
                status = "[green]\uf06e\u0020[/green]"
            else:
                name = f"[red]{act.name}[/red]"
                status = "[red]\uf070\u0020[/red]"

            duration = self._format_duration(timedelta(seconds=act.duration_sec))
            distance = act.distance_m

            table.add_row(act.start_time, act.id, status, name, distance, duration)

    def _format_duration(self, td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.notify(f"On Data Table Row Selected")


if __name__ == "__main__":
    Ui().run()
