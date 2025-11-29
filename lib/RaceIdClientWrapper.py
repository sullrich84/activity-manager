from lib.RaceIdClient import RaceIdClient


class RaceIdClientWrapper:
    def auth_raceid(self) -> RaceIdClient:
        client = RaceIdClient()
        client.auth("username", "password")
        return client
