from lib.ui2 import Ui
from lib.gc import GarminClient


def main():
    ui = Ui()
    ui.run()

    client = GarminClient()

    start_date = "2025-10-01"

    for act in client.get_activities(start_date):
        ui.add_activity(act)


if __name__ == "__main__":
    main()
