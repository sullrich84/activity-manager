from activity_manager.clients.RaceIdClient import RaceIdClient, Result
from activity_manager.config.ConfigLoader import ConfigLoader
from activity_manager.models import ActivityModel
from activity_manager.data.ActivityStore import ActivityStore


class RaceIdRepository:
    client = RaceIdClient()
    config = ConfigLoader()

    def __init__(self):
        self.store = ActivityStore()
        self._sync_initial_state()

    def _sync_initial_state(self):
        """
        Check all activities in store against RaceID cache and update sync state
        """
        synced_urls = set()
        for results in self.client.cache.values():
            for result in results:
                if result.activity_link:
                    synced_urls.add(result.activity_link)

        # Collect all updates to batch them
        updates = {}
        all_activities = self.store.get_all_activities()
        for activity in all_activities:
            is_synced = activity.url in synced_urls
            if activity.synced != is_synced:
                updates[activity.id] = is_synced

        # Batch update all sync states with a single notification
        if updates:
            self.store.batch_update_sync_states(updates)

    def set_result(self, activity: ActivityModel):
        year_month = activity.start_time[:7]  # Gets 'YYYY-MM'

        try:
            series_id = self.config.get_raceid_series_id(year_month)
        except KeyError as e:
            raise ValueError(f"Cannot sync activity from {year_month}: {e}")

        result = Result(
            activity_link=activity.url,
            distance_logged=max(1, activity.distance_m),
            distance_logged_at=activity.start_time[:10],
            time_result=activity.formatted_duration,
        )
        response = self.client.log_result(id=series_id, result=result)

        # Update sync state in central store (triggers UI update)
        self.store.update_sync_state(activity.id, synced=True)

        return response
