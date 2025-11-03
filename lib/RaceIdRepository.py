from lib.RaceIdClient import Result
from lib.RaceIdClientWrapper import RaceIdClientWrapper
from model.ActivityItem import ActivityItem


class RaceIdReposiotry:
    CLIENT = RaceIdClientWrapper().auth_raceid()

    def set_result(self, id: str, activity: ActivityItem):
        result = Result(
            activity_link=activity.url,
            distance_logged=activity.distance_m,
            distance_logged_at=activity.start_time[:10],
            time_result=activity.formatted_duration,
        )
        return self.CLIENT.log_result(id=id, result=result)
