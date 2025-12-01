from typing import Callable, List, Dict
from activity_manager.models import ActivityModel
from activity_manager.data.ActivityDatabase import ActivityDatabase


class ActivityStore:
    """
    Central data store for activities with event system.
    Acts as a single source of truth that can be modified by multiple actors.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActivityStore, cls).__new__(cls)
            cls._instance._initialized = False
            cls._instance._listeners = []
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.db = ActivityDatabase()
        self.activities: Dict[str, ActivityModel] = {}
        self._load_from_db()

    def _load_from_db(self):
        """
        Load activities from database into memory
        """
        db_activities = self.db.get_all()
        for activity in db_activities:
            self.activities[activity.id] = activity

    def subscribe(self, listener: Callable[[], None]):
        """
        Subscribe to store changes
        """
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: Callable[[], None]):
        """
        Unsubscribe from store changes
        """
        if listener in self._listeners:
            self._listeners.remove(listener)

    def _notify_listeners(self):
        """
        Notify all subscribers of changes
        """
        for listener in self._listeners:
            listener()

    def save_activity(self, activity: ActivityModel):
        """
        Save or update a single activity
        """
        self.activities[activity.id] = activity
        self.db.save(activity)
        self._notify_listeners()

    def save_activities(self, activities: List[ActivityModel]):
        """
        Save or update multiple activities
        """
        for activity in activities:
            self.activities[activity.id] = activity
        self.db.save_many(activities)
        self._notify_listeners()

    def update_sync_state(self, activity_id: str, synced: bool, notify: bool = True):
        """
        Update the sync state of a specific activity
        """
        if activity_id in self.activities:
            self.activities[activity_id].synced = synced
            self.db.save(self.activities[activity_id])
            if notify:
                self._notify_listeners()

    def batch_update_sync_states(self, updates: Dict[str, bool]):
        """
        Update multiple sync states without triggering notifications for each
        """
        for activity_id, synced in updates.items():
            self.update_sync_state(activity_id, synced, notify=False)
        # Notify once after all updates
        self._notify_listeners()

    def get_activity(self, activity_id: str) -> ActivityModel | None:
        """
        Get a single activity by ID
        """
        return self.activities.get(activity_id)

    def get_all_activities(self) -> List[ActivityModel]:
        """
        Get all activities sorted by start_time
        """
        activities = list(self.activities.values())
        return sorted(activities, key=lambda a: a.start_time, reverse=True)
