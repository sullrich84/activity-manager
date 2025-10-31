from dataclasses import dataclass
from datetime import timedelta

ICONS = {
    "RUN": "󰜎 ",
}


@dataclass
class ActivityItem:
    id: str
    name: str
    atype: str
    privacy: str
    start_time: str
    distance_m: int
    duration_sec: int

    @property
    def url(self) -> str:
        return f"https://connect.garmin.com/modern/activity/{self.id}"

    @property
    def is_public(self):
        return self.privacy == "public"

    @property
    def formatted_name(self) -> str:
        return self.name if self.is_public else f"[red]{self.name}[/red]"

    @property
    def visibility_icon(self) -> str:
        return "[green] [/green]" if self.is_public else f"[red] [/red]"

    @property
    def activity_icon(self) -> str:
        return "󰜎 "

    @property
    def formatted_distance(self) -> str:
        if self.distance_m < 1000:
            unit = "m"
            value = self.distance_m
        else:
            unit = "km"
            value = round(self.distance_m / 1000, 1)
            value = int(value) if value == int(value) else value
        return f"{value:>6}[dim italic]{unit:<2}[/dim italic]"

    @property
    def formatted_duration(self) -> str:
        td = timedelta(seconds=self.duration_sec)
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
