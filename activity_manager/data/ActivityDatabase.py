import pickle
from typing import List, Dict
from pathlib import Path

from activity_manager.models import ActivityModel


class ActivityDatabase:
    """
    Local Database for ActivityModels
    """

    STORAGE_FOLDER_NAME = ".gcm"

    def __init__(self, name: str = "activities") -> None:
        self.file_path = self.create_persistence_file(name)
        self.activities: Dict[str, ActivityModel] = {}
        self.read_from_disk()

    # --- Query Methods ---

    def save(self, activity: ActivityModel) -> None:
        self.activities[activity.id] = activity
        self.write_to_disk()

    def save_many(self, activities: List[ActivityModel]) -> None:
        for activity in activities:
            self.activities[activity.id] = activity
        self.write_to_disk()

    def get_all(self) -> List[ActivityModel]:
        activities = list(self.activities.values())
        return sorted(activities, key=lambda a: a.start_time, reverse=True)

    # --- I/O Methods ---

    def create_persistence_file(self, name: str) -> Path:
        dir = Path(Path.home(), self.STORAGE_FOLDER_NAME)
        dir.mkdir(parents=True, exist_ok=True)
        return Path(f"{dir}/{name}.pkl")

    def read_from_disk(self) -> None:
        if self.file_path.exists():
            try:
                with open(self.file_path, "rb") as f:
                    self.activities = pickle.load(f)
            except (pickle.PickleError, EOFError):
                self.activities = {}

    def write_to_disk(self) -> None:
        with open(self.file_path, "wb") as f:
            pickle.dump(self.activities, f)
