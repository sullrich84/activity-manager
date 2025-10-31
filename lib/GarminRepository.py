from model.ActivityItem import ActivityItem
from lib.GarminClientWrapper import GarminClientWrapper


class GarminRepository:
    CLIENT = GarminClientWrapper().auth_garmin()

    def get_activities(
        self, start_date: str, end_date: str | None = None
    ) -> list[ActivityItem]:
        items = list()
        activities = self.CLIENT.get_activities_by_date(start_date, end_date)

        for act in activities:
            id = str(act.get("activityId"))
            name = str(act.get("activityName"))
            atype = str(act.get("activityType"))
            privacy = str(act.get("privacy", dict()).get("typeKey"))
            start_time = str(act.get("startTimeLocal"))
            distance = int(act.get("distance", 0))
            duration = int(act.get("duration", 0))

            item = ActivityItem(
                id=id,
                name=name,
                atype=atype,
                privacy=privacy,
                start_time=start_time,
                distance_m=distance,
                duration_sec=duration,
            )

            items.append(item)

        return items
