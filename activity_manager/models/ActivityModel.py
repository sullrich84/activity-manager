from dataclasses import dataclass
from datetime import timedelta


ICONS = {
    "running": "󰜎 ",
    "virtual_run": "󰜎 ",
    "trail_running": "󰜎 ",
    "treadmill_running": "󰜎 ",
    "hiking": "󰖃 ",
    "walking": "󰖃 ",
    "yoga": "󱅼 ",
    "cycling": "󰂣 ",
    "road_biking": "󰂣 ",
    "virtual_ride": "󰂣 ",
    "indoor_cycling": "󰂣 ",
    "mountain_biking": "󰂣 ",
    "hiit": "󱅝 ",
    "strength_training": "󱅝 ",
    "lap_swimming": "󰓣 ",
    "open_water_swimming": "󰓣 ",
    "multi_sport": " ",
    "meditation": "󱅻 ",
    "kayaking_v2": "󰢯 ",
    "stand_up_paddel": "󰢯 ",
    "stop_watch": " ",
    "other": " ",
    "floor_climb": "󰓍 ",
}


@dataclass
class ActivityModel:
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
    def visibility_icon(self) -> str:
        return f"[green] [/green]" if self.is_public else f"[red] [/red]"

    @property
    def sync_icon(self) -> str:
        return f"[green]󰪩 [/green]" if False else f"[red]󰳿 [/red]"

    @property
    def activity_icon(self) -> str:
        if self.atype in ICONS:
            return ICONS[self.atype]
        else:
            return self.atype

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
