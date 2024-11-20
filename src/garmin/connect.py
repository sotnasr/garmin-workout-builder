import json

import cloudscraper

from garmin.authorization import GarminAuthorization
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
    def __init__(self, authorization: GarminAuthorization):
        self.authorization = authorization
        self.session = cloudscraper.CloudScraper()
        self.session.cookies.update(self.authorization.cookies)

    def create_workout(self, workout: Workout) -> None:
        url = "https://connect.garmin.com/workout-service/workout"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://connect.garmin.com",
            "Di-Backend": "connectapi.garmin.com",
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {self.authorization.token}",
        }

        try:
            workout_serialized = GarminSerializer().serialize(workout)
            response = self.session.post(url, headers=headers, data=json.dumps(workout_serialized))
            response.raise_for_status()
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

    def schedule_workout(self) -> None:
        pass