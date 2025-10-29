import subprocess
from rich.console import Console
from rich.table import Table
from datetime import timedelta
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)


def auth_garmin():
    username = get_1password_secret("op://Personal/Garmin/username")
    password = get_1password_secret("op://Personal/Garmin/password")
    token_store = "~/.garminconnect"

    try:
        client = Garmin()
        client.garth.load(token_store)
        print(f"Restored auth session")
    except (FileNotFoundError, GarminConnectConnectionError):
        client = Garmin(username, password)
        client.login()
        client.garth.dump(token_store)
        print(f"Created new auth session")
    except GarminConnectAuthenticationError:
        client = Garmin()
        client.login(token_store)
        print(f"Refreshed auth session")

    return client


def get_1password_secret(item_path):
    try:
        cmd = ["op", "read", item_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Auslesen von 1Password Secret {item_path}: {e}")
        return None


def format_hh_mm_ss(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def build_ui():
    console = Console()
    table = Table(show_header=True, show_footer=True)

    table.add_column("Date", style="dim")
    table.add_column("Name")
    table.add_column("Distance", justify="right")
    table.add_column("Duration", justify="right")

    return console, table


def main():
    console, table = build_ui()
    client = auth_garmin()
    start_date = "2025-10-01"
    end_date = "2025-10-28"
    activities = client.get_activities_by_date(start_date, end_date)
    # print(f"Found {len(activities)} activities between {start_date} and {end_date}")

    for act in activities:
        # id = act.get("activityId")
        name = act.get("activityName")
        # url = f"https://connect.garmin.com/modern/activity/{id}"
        start_time = str(timedelta(seconds=int(act.get("startTimeLocal"))))
        distance = round(act.get("distance", 1))
        duration = act.get("duration", 0)

        table.add_row(str(start_time), str(name), str(distance), str(duration))

    console.print(table)


if __name__ == "__main__":
    main()
