from activity_manager.clients.RaceIdClient import RaceIdClient, Result
from activity_manager.config.ConfigLoader import ConfigLoader
from activity_manager.models import ActivityModel


class RaceIdRepository:
    client = RaceIdClient()
    config = ConfigLoader()

    def set_result(self, activity: ActivityModel):
        year_month = activity.start_time[:7]  # Gets 'YYYY-MM'
        series_id = self.config.get_raceid_series_id(year_month)

        result = Result(
            activity_link=activity.url,
            distance_logged=max(1, activity.distance_m),
            distance_logged_at=activity.start_time[:10],
            time_result=activity.formatted_duration,
        )
        return self.client.log_result(id=series_id, result=result)
