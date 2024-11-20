
class GarminConnect:
    """
    Garmin Connect HTTP client.
    This class provides methods to interact with the Garmin Connect API.
    It handles authentication using the provided username and password.

    Methods:
        __init__(username: str, password: str):
            Initializes the GarminConnect client with the provided username and password.
    """
    
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password