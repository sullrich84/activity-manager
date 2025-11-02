import requests
from typing import Optional, Dict, Any


class RaceID:
    BASE_API_URL = "https://api.raceid.com/api/v1/web"
    bearer_token: Optional[str] = None

    def login(self, username: str, password: str) -> bool:
        url = f"{self.BASE_API_URL}/user/login"
        payload = {"email": username, "password": password}

        try:
            response = requests.post(
                url,
                json=payload,
                headers={"accept": "application/json, text/plain, */*"},
            )
            response.raise_for_status()

            data = response.json()
            self.bearer_token = data.get("data", {}).get("token")

            if self.bearer_token:
                return True
            else:
                return False

        except requests.exceptions.HTTPError as err:
            return False
        except requests.exceptions.RequestException as err:
            return False

    def fetch_race_results(
        self, id: str, page: int = 1, limit: int = 100
    ) -> Optional[Dict[str, Any]]:
        if not self.bearer_token:
            return None

        url = f"{self.BASE_API_URL}/racers/{id}/segments"
        headers = {
            "accept": "application/json, text/plain, */*",
            "x-authorization": f"Bearer {self.bearer_token}",
        }

        params = {"page": page, "limit": limit}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as err:
            return None
        except requests.exceptions.RequestException as err:
            return None

    def log_race_segment(
        self,
        racer_id: str,
        activity_link: str,
        distance_logged: int,
        distance_logged_at: str,
        time_result: str,
    ) -> Optional[Dict[str, Any]]:
        if not self.bearer_token:
            return None

        url = f"{self.BASE_API_URL}/racers/{racer_id}/segments"
        payload = {
            "activity_link": activity_link,
            "distance_logged": distance_logged,
            "distance_logged_at": distance_logged_at,
            "time_result": time_result,
        }

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "x-authorization": f"Bearer {self.bearer_token}",
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as err:
            return None


if __name__ == "__main__":
    client = RaceID()

    client.login("sebastian.ullrich@deepsource.de", "hqg.ufg@vnd8EUZ2jxt")
    # print(client.fetch_race_results("995655"))
    client.log_race_segment(
        racer_id="995659",
        activity_link="https://connect.garmin.com/modern/activity/20870918926",
        distance_logged="33740",
        distance_logged_at="2025-11-02",
        time_result="01:07:17",
    )
