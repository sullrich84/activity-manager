import pickle
from typing import List, Dict
from pathlib import Path
from model.ActivityItem import ActivityItem


class ActivityStore:
    def __init__(self, name: str = "activities"):
        db_dir = Path.home() / ".gcm"
        db_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = db_dir / f"{name}.pkl"
        self._activities: Dict[str, ActivityItem] = {}
        self._load()

    def _load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "rb") as f:
                    self._activities = pickle.load(f)
            except (pickle.PickleError, EOFError):
                self._activities = {}

    def _save(self):
        with open(self.file_path, "wb") as f:
            pickle.dump(self._activities, f)

    def save(self, activity: ActivityItem) -> None:
        self._activities[activity.id] = activity
        self._save()

    def save_many(self, activities: List[ActivityItem]) -> None:
        for activity in activities:
            self._activities[activity.id] = activity
        self._save()

    def get_all(self) -> List[ActivityItem]:
        activities = list(self._activities.values())
        return sorted(activities, key=lambda a: a.start_time, reverse=True)
