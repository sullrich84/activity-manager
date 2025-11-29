from lib.RaceIdClient import Result
from lib.RaceIdClientWrapper import RaceIdClientWrapper
from lib.ConfigLoader import ConfigLoader
from src.models import ActivityModel


class RaceIdRepository:
    CLIENT = RaceIdClientWrapper().auth_raceid()
    CONFIG = ConfigLoader()

    def set_result(self, activity: ActivityModel):
        # Extract year-month from activity start_time (format: 'YYYY-MM-DD ...')
        year_month = activity.start_time[:7]  # Gets 'YYYY-MM'
        series_id = self.CONFIG.get_raceid_series_id(year_month)

        result = Result(
            activity_link=activity.url,
            distance_logged=max(1, activity.distance_m),
            distance_logged_at=activity.start_time[:10],
            time_result=activity.formatted_duration,
        )
        return self.CLIENT.log_result(id=series_id, result=result)
