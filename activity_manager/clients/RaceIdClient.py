import requests
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Literal, Optional, Any

from activity_manager.config import ConfigLoader


@dataclass
class Result:
    activity_link: str
    distance_logged: int
    distance_logged_at: str
    time_result: str
    id: str | None = None
    result_id: str | None = None


class RaceIdClient:
    BASE_API_URL = "https://api.raceid.com/api/v1/web"
    TOKEN_STORE = Path.home() / ".raceid" / "token.jwt"

    config = ConfigLoader()
    bearer_token: Optional[str] = None
    cache = {}

    def __init__(self):
        self.load_token()

        if not self.bearer_token:
            self.auth()  # TODO: handle token expire

        for racer_id in self.config.get_raceid_series():
            self.cache[racer_id] = self.get_results(racer_id)

        print(self.cache)
        exit(1)

    def auth(self):
        credentials = self.config.get_credentials("raceid")
        auth_json = {
            "email": credentials["username"],
            "password": credentials["password"],
        }
        response = self.request("POST", "/user/login", json=auth_json, with_auth=False)

        self.save_token(response)
        self.bearer_token = response.get("data", {}).get("token")

    def load_token(self) -> None:
        try:
            if self.TOKEN_STORE.exists():
                with open(self.TOKEN_STORE, "r") as token_file:
                    auth_response = json.load(token_file)
                    self.bearer_token = auth_response.get("data", {}).get("token")
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_token(self, auth_response: dict):
        self.TOKEN_STORE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.TOKEN_STORE, "w") as f:
            json.dump(auth_response, f, indent=2)

    def get_results(self, id: str, page: int = 1, limit: int = 100) -> list[Result]:
        params = {"page": page, "limit": limit}
        response = self.request("GET", f"/racers/{id}/segments", params=params)

        results = []
        for res in response.get("data", {}):
            result = Result(
                activity_link=res["activity_link"],
                distance_logged=res["distance_logged"],
                distance_logged_at=res["distance_logged_at"],
                time_result=res["time_result"],
                result_id=res["result_id"],
                id=res["id"],
            )
            results.append(result)
        return results

    def log_result(self, id: str, result: Result):
        json = {
            "activity_link": result.activity_link,
            "distance_logged": result.distance_logged,
            "distance_logged_at": result.distance_logged_at,
            "time_result": f"{result.time_result}.000",
        }

        endpoint = f"/racers/{id}/segments"
        return self.request("POST", endpoint=endpoint, json=json)

    def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        params: Any = {},
        json: Any = {},
        with_auth: bool = True,
    ) -> Any:
        url = f"{self.BASE_API_URL}{endpoint}"
        headers = {"accept": "application/json", "content-type": "application/json"}

        if with_auth:
            headers["x-authorization"] = f"Bearer {self.bearer_token}"

        match (method):
            case "GET":
                response = requests.get(url, headers=headers, params=params)
            case "POST":
                response = requests.post(url, headers=headers, json=json)

        response.raise_for_status()
        return response.json()
