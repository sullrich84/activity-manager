from dataclasses import dataclass
import requests
from typing import Optional, Dict, Any


@dataclass
class Result:
    activity_link: str
    distance_logged: int
    distance_logged_at: str
    time_result: str
    id: str | None = None
    result_id: str | None = None


class RaceID:
    BASE_API_URL = "https://api.raceid.com/api/v1/web"
    bearer_token: Optional[str] = None

    def login(self, username: str, password: str):
        url = f"{self.BASE_API_URL}/user/login"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        payload = {
            "email": username,
            "password": password,
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        self.bearer_token = data.get("data", {}).get("token")

    def get_results(self, id: str, page: int = 1, limit: int = 100):
        params = {"page": page, "limit": limit}
        return self._make_request("GET", f"/racers/{id}/segments", params=params)

    def log_result(self, id: str, log: Result) -> Optional[Dict[str, Any]]:
        data = {
            "activity_link": log.activity_link,
            "distance_logged": log.distance_logged,
            "distance_logged_at": log.distance_logged_at,
            "time_result": log.time_result,
        }

        results = []
        for response in self._make_request("POST", f"/racers/{id}/segments", data=data):
            result = Result(
                id=response["id"],
                result_id=response["result_id"],
                activity_link=response["activity_link"],
                distance_logged=response["distance_logged"],
                distance_logged_at=response["distance_logged_at"],
                time_result=response["time_result"],
            )
            results.append(result)
        return results

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Any = {},
        data: Any = {},
        with_auth: bool = True,
    ) -> Dict[str, Any]:
        url = f"{self.BASE_API_URL}{endpoint}"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        if with_auth:
            headers["x-authorization"] = f"Bearer {self.bearer_token}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Invalid method: {method}")

            # print(f"method: {method}")
            # print(f"respone: {response.status_code}")
            # print(f"data: {response.json()}")

            response.raise_for_status()
            return response.json().get("data", {})

        except requests.RequestException as ex:
            print(ex)
            return None


if __name__ == "__main__":
    client = RaceID()
    client.login("sebastian.ullrich@deepsource.de", "hqg.ufg@vnd8EUZ2jxt")

    log = Result(
        activity_link="https://connect.garmin.com/modern/activity/20870918926",
        distance_logged=33740,
        distance_logged_at="2025-11-02",
        time_result="01:07:17",
    )

    print(client.get_results("995659"))
    # client.log_result(id="995659", log=log)
