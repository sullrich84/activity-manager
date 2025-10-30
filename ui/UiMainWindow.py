from logging import disable
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, LoadingIndicator
from lib.GarminRepository import GarminRepository
from ui.UiActivityFilter import UiActivityFilter
from ui.UiActivityTable import UiActivityTable


class UiMainWindow(App):
    CSS = """
        Screen { layout: vertical; }
        UiActivityFilter { dock: top; }

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
            UiActivityFilter(),
            UiActivityTable(),
        )
        yield Footer()

    async def on_ready(self) -> None:
        await self.load_activities()

    async def load_activities(self):
        table = self.query_one(UiActivityTable)
        for act in self.REPOSITORY.get_activities("2025-10-01"):
            table.add_row(
                act.start_time,
                act.id,
                act.formatted_visibility,
                act.formatted_name,
                act.formatted_distance,
                act.formatted_duration,
            )
