from enum import Enum


class DistanceType(Enum):
    """
    The DistanceType representing different types of distance measurements.

    Attributes:
        KILOMETERS (int): Represents distance in kilometers.
        METERS (int): Represents distance in meters.
    """
    KILOMETERS = 1
    METERS = 2
