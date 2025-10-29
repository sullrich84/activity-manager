from dataclasses import dataclass


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
