import datetime

import cloudscraper

from garmin.authorization import GarminAuthorization
from garmin.exceptions import GarminWorkoutIdError
from garmin.serializer import GarminSerializer
from models.workout import Workout


class GarminConnectClient:
    """
    Garmin Connect client for interacting with the Garmin Connect API.

    Attributes:
        authorization (GarminAuthorization): The authorization object containing the token and cookies.

    Methods:
        __init__(authorization: GarminAuthorization):
            Initializes the GarminConnectClient with the given authorization.

        create_workout(workout: Workout) -> None:
            Creates a new workout on Garmin Connect.
    """

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://connect.garmin.com",
        "Di-Backend": "connectapi.garmin.com",
        "Accept": "application/json, text/plain, */*",
    }

    def __init__(self, authorization: GarminAuthorization):
        self.authorization = authorization
        self.session = cloudscraper.CloudScraper()
        self.session.cookies.update(self.authorization.cookies)

    def create_workout(self, workout: Workout) -> None:
        url = "https://connect.garmin.com/workout-service/workout"
        headers = {
            **self.DEFAULT_HEADERS,
            "Authorization": f"Bearer {self.authorization.token}",
        }

        try:
            sz = GarminSerializer()
            workout_serialized = sz.serialize(workout)

            r = self.session.post(
                url, headers=headers, json=workout_serialized
            )
            r.raise_for_status()

            response = r.json()
            workout_id = response.get("workoutId")
            if workout_id is None:
                raise GarminWorkoutIdError("Workout ID not found in the response")

            return workout_id
        except Exception as err:
            raise

    def schedule_workout(self, workout_id: int, date: datetime.date) -> None:
        url = f"https://connect.garmin.com/workout-service/schedule/{workout_id}"
        headers = {
            **self.DEFAULT_HEADERS,
            "Authorization": f"Bearer {self.authorization.token}",
        }

        payload = {"date": date.strftime("%Y-%m-%d")}

        try:
            r = self.session.post(
                url, headers=headers, json=payload,
            )
            r.raise_for_status()

            response = r.json()
            if "workoutScheduleId" not in response:
                raise Exception("Workout schedule ID not found in the response")
        except Exception as err:
            raise
