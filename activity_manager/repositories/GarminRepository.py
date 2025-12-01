from activity_manager.models import ActivityModel
from activity_manager.clients.GarminClientWrapper import GarminClientWrapper
from activity_manager.data.ActivityStore import ActivityStore


class GarminRepository:
    CLIENT = GarminClientWrapper().auth_garmin()

    def __init__(self):
        self.store = ActivityStore()

    def get_activities(
        self, start_date: str, end_date: str | None = None
    ) -> list[ActivityModel]:
        """Fetch activities from Garmin and save to central store"""
        items = list()
        activities = self.CLIENT.get_activities_by_date(start_date, end_date)

        for act in activities:
            id = str(act.get("activityId"))
            name = str(act.get("activityName"))
            atype = str(act.get("activityType", dict()).get("typeKey"))
            privacy = str(act.get("privacy", dict()).get("typeKey"))
            start_time = str(act.get("startTimeLocal"))
            distance = int(act.get("distance", 0))
            duration = int(act.get("duration", 0))

            # Check if activity already exists in store to preserve sync state
            existing_activity = self.store.get_activity(id)
            synced = existing_activity.synced if existing_activity else False

            item = ActivityModel(
                id=id,
                name=name,
                atype=atype,
                privacy=privacy,
                start_time=start_time,
                distance_m=distance,
                duration_sec=duration,
                synced=synced,
            )

            items.append(item)

        # Save to central store (triggers UI update)
        self.store.save_activities(items)

        return items
