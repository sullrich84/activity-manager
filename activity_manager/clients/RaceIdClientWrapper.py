from activity_manager.config.ConfigLoader import ConfigLoader, Credentials
from activity_manager.clients.RaceIdClient import RaceIdClient


class RaceIdClientWrapper:
    CONFIG = ConfigLoader()

    def auth_raceid(self) -> RaceIdClient:
        client = RaceIdClient()
        credentials: Credentials = self.CONFIG.get_credentials("raceid")
        client.auth(credentials["username"], credentials["password"])
        return client
