from lib.RaceIdClient import Result
from lib.RaceIdClientWrapper import RaceIdClientWrapper
from src.models import ActivityModel


class RaceIdRepository:
    CLIENT = RaceIdClientWrapper().auth_raceid()

    def set_result(self, id: str, activity: ActivityModel):
        result = Result(
            activity_link=activity.url,
            distance_logged=activity.distance_m,
            distance_logged_at=activity.start_time[:10],
            time_result=activity.formatted_duration,
        )
        return self.CLIENT.log_result(id=id, result=result)
