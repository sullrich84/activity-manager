import requests
from dataclasses import dataclass
from typing import Literal, Optional, Any


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

    def auth(self, username: str, password: str):
        json = {"email": username, "password": password}
        response = self._make_request("POST", "/user/login", json=json)
        self.bearer_token = response.get("data", {}).get("token")

    def get_results(self, id: str, page: int = 1, limit: int = 100) -> list[Result]:
        params = {"page": page, "limit": limit}
        response = self._make_request("GET", f"/racers/{id}/segments", params=params)

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
        return self._make_request("POST", endpoint=endpoint, json=json)

    def _make_request(
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

        try:
            match (method):
                case "GET":
                    response = requests.get(url, headers=headers, params=params)
                case "POST":
                    response = requests.post(url, headers=headers, json=json)

            # print(f"method: {method}")
            # print(f"respone: {response.status_code}")
            # print(f"data: {response.json()}")

            response.raise_for_status()
            return response.json()

        except requests.RequestException as ex:
            print(ex)
            return None


if __name__ == "__main__":
    client = RaceID()
    client.auth("sebastian.ullrich@deepsource.de", "hqg.ufg@vnd8EUZ2jxt")

    result = Result(
        activity_link="https://connect.garmin.com/modern/activity/20870918926",
        distance_logged=33740,
        distance_logged_at="2025-11-02",
        time_result="01:07:17",
    )

    # client.log_result(id="995659", result=result)
    for result in client.get_results("995659"):
        print(
            f"{result.id} {result.result_id} {result.time_result} {result.activity_link}"
        )
