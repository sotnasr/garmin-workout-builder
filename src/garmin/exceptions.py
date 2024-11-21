class GarminAuthException(Exception):
    """
    Base exception for Garmin authentication errors
    """

    pass


class GarminLoginError(GarminAuthException):
    """
    Exception raised when login credentials are invalid
    """

    pass


class GarminServiceError(GarminAuthException):
    """
    Exception raised when Garmin service is unavailable
    """

    pass


class GarminTokenError(GarminAuthException):
    """
    Exception raised when token operations fail
    """

    pass


class GarminWorkoutIdError(Exception):
    """
    Exception raised when a workout ID could not be retrieved from Garmin Connect
    """

    pass
