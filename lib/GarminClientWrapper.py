from lib.ConfigLoader import ConfigLoader
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)


class GarminClientWrapper:
    CONFIG = ConfigLoader()
    TOKEN_STORE = "~/.acm/.gcm"

    def auth_garmin(self) -> Garmin:
        try:
            client = Garmin()
            client.garth.load(self.TOKEN_STORE)
        except (FileNotFoundError, GarminConnectConnectionError):
            client = Garmin(self.CONFIG.garmin.username, self.CONFIG.garmin.password)
            client.login()
            client.garth.dump(self.TOKEN_STORE)
        except GarminConnectAuthenticationError:
            client = Garmin()
            client.login(self.TOKEN_STORE)

        return client
