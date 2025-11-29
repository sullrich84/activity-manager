from lib.ConfigLoader import ConfigLoader, Credentials
from lib.RaceIdClient import RaceIdClient


class RaceIdClientWrapper:
    CONFIG = ConfigLoader()

    def auth_raceid(self) -> RaceIdClient:
        client = RaceIdClient()
        credentials: Credentials = self.CONFIG.raceid
        client.auth(credentials.username, credentials.password)
        return client
