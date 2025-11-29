import sys
import yaml
from pathlib import Path
from typing import TypedDict


class Credentials(TypedDict):
    username: str
    password: str


class ConfigLoader:
    def __init__(self):
        """
        Loads properties from the config file.
        """

        # Loads /Users/sullrich/.acm/config.yaml
        config_path = Path.home() / ".acm" / "config.yaml"

        try:
            with open(config_path, "r") as file:
                self._config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file {config_path} not found!")
            sys.exit(1)
        except yaml.YAMLError as err:
            print(f"Could not parse {config_path}: {err}")
            sys.exit(1)

    def get_credentials(self, service: str) -> Credentials:
        """
        Returns credentials for a given service.
        """
        try:
            return {
                "username": self._config[service]["username"],
                "password": self._config[service]["password"],
            }
        except KeyError as err:
            print(f"Missing required field in config for service '{service}': {err}")
            sys.exit(1)
