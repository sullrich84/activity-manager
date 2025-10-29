import subprocess
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)

token_store = "~/.garminconnect"


def auth_garmin() -> Garmin:
    try:
        client = Garmin()
        client.garth.load(token_store)
    except (FileNotFoundError, GarminConnectConnectionError):
        username = get_1password_secret("op://Personal/Garmin/username")
        password = get_1password_secret("op://Personal/Garmin/password")
        client = Garmin(username, password)
        client.login()
        client.garth.dump(token_store)
    except GarminConnectAuthenticationError:
        client = Garmin()
        client.login(token_store)

    return client


def get_1password_secret(item_path) -> str | None:
    try:
        cmd = ["op", "read", item_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Auslesen von 1Password Secret {item_path}: {e}")
        return None
