from lib.Utils import get_1password_secret
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)


class GarminClientWrapper:
    TOKEN_STORE = "~/.garminconnect"

    def auth_garmin(self) -> Garmin:
        try:
            client = Garmin()
            client.garth.load(self.TOKEN_STORE)
        except (FileNotFoundError, GarminConnectConnectionError):
            username = get_1password_secret("op://Personal/Garmin/username")
            password = get_1password_secret("op://Personal/Garmin/password")

            client = Garmin(username, password)
            client.login()
            client.garth.dump(self.TOKEN_STORE)
        except GarminConnectAuthenticationError:
            client = Garmin()
            client.login(self.TOKEN_STORE)

        return client
