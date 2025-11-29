import sys
import yaml
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ConfigLoader:
    username: str
    password: str

    def __init__(self):
        """
        Loads properties from the config file.
        """

        config_path = Path.home() / ".acm" / "config.yaml"

        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
                self.username = config["garmin"]["username"]
                self.password = config["garmin"]["password"]
        except FileNotFoundError:
            print(f"Config file {config_path} not found!")
            sys.exit(1)
        except yaml.YAMLError as err:
            print(f"Could not parse {config_path}: {err}")
            sys.exit(1)
        except KeyError as err:
            print(f"Missing required field in config: {err}")
            sys.exit(1)
