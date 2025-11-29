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
            credentials = self.CONFIG.get_credentials("garmin")
            client = Garmin(credentials["username"], credentials["password"])
            client.login()
            client.garth.dump(self.TOKEN_STORE)
        except GarminConnectAuthenticationError:
            client = Garmin()
            client.login(self.TOKEN_STORE)

        return client
