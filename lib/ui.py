from datetime import timedelta
from rich.console import Console
from rich.table import Table

from lib.models import ActivityItem


class Ui:
    console = Console()

    def __init__(self):
        self.total_duration_sec = 0
        self.activities = []
        self._build_table()

    def _build_table(self):
        self.table = Table(expand=True, show_footer=True, border_style="dim")
        self.table.add_column("Date", style="dim")
        self.table.add_column("Status")
        self.table.add_column("Name")
        self.table.add_column("Distance (m)", justify="right")

        delta = timedelta(seconds=self.total_duration_sec)
        total_duration_str = self._format_duration(delta)
        self.table.add_column("Duration", justify="right", footer=total_duration_str)

        for act in self.activities:
            if act.privacy == "public":
                name = act.url
                status = "[green]\uf06e\u0020[/green]"
            else:
                name = f"[red]{act.url}[/red]"
                status = "[red]\uf070\u0020[/red]"

            duration = self._format_duration(timedelta(seconds=act.duration_sec))
            distance = f"{act.distance_m}[dim]m[/dim]"

            self.table.add_row(act.start_time, status, name, distance, duration)

    def add_activity(self, act: ActivityItem):
        self.activities.append(act)
        self.total_duration_sec += act.duration_sec
        self._build_table()
        self.refresh()

    def refresh(self):
        self.console.clear()
        self.console.print(self.table)
