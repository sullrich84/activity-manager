import subprocess
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
            username = self.get_1password_secret("op://Personal/Garmin/username")
            password = self.get_1password_secret("op://Personal/Garmin/password")
            client = Garmin(username, password)
            client.login()
            client.garth.dump(self.TOKEN_STORE)
        except GarminConnectAuthenticationError:
            client = Garmin()
            client.login(self.TOKEN_STORE)

        return client

    def get_1password_secret(self, item_path) -> str | None:
        try:
            cmd = ["op", "read", item_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Auslesen von 1Password Secret {item_path}: {e}")
            return None
