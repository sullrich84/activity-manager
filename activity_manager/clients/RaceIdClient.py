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
        # Try to load JWT token from config first
        self.bearer_token = self.config.get_raceid_jwt_token()

        if not self.bearer_token:
            raise ValueError(
                "No JWT token found. Please add 'token' field to raceid section in config.yaml"
            )

        for racer_id in self.config.get_raceid_series():
            self.cache[racer_id] = self.get_results(racer_id)

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
            headers["Pace-Authorization"] = f"Bearer {self.bearer_token}"

        try:
            match (method):
                case "GET":
                    response = requests.get(url, headers=headers, params=params)
                case "POST":
                    response = requests.post(url, headers=headers, json=json)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"RaceID API request failed: {e}")
