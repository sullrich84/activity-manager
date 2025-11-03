from lib.RaceIdClient import RaceIdClient
from lib.Utils import get_1password_secret


class RaceIdClientWrapper:
    def auth_raceid(self) -> RaceIdClient:
        username = get_1password_secret("op://Personal/Raceid/username")
        password = get_1password_secret("op://Personal/Raceid/password")
        client = RaceIdClient()
        client.auth(username, password)
        return client
