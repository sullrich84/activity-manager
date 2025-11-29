import sys
import yaml
from pathlib import Path
from typing import TypedDict


class Credentials(TypedDict):
    username: str
    password: str


class ConfigLoader:
    garmin: Credentials
    raceid: Credentials

    def __init__(self):
        """
        Loads properties from the config file.
        """

        # Loads /Users/sullrich/.acm/config.yaml
        config_path = Path.home() / ".acm" / "config.yaml"

        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
                self.garmin: Credentials = {
                    "username": config["garmin"]["username"],
                    "password": config["garmin"]["password"],
                }
                self.raceid: Credentials = {
                    "username": config["raceid"]["username"],
                    "password": config["raceid"]["password"],
                }
        except FileNotFoundError:
            print(f"Config file {config_path} not found!")
            sys.exit(1)
        except yaml.YAMLError as err:
            print(f"Could not parse {config_path}: {err}")
            sys.exit(1)
        except KeyError as err:
            print(f"Missing required field in config: {err}")
            sys.exit(1)
