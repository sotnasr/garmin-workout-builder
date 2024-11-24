from abc import ABC
from typing import TypeVar, Generic

from models.distance_type import DistanceType


T = TypeVar('T')

class Condition(ABC, Generic[T]):
    """
    Conditions can be based on various metrics such as time, distance, etc. This class serves as a 
    blueprint for creating specific condition types by providing a common interface and structure. 

    Attributes:
    value (T): The value associated with the condition. The type of this value is generic and 
                can be specified when creating a subclass of Condition.
    """
    id: int
    type: str
    value: T


class Duration(Condition[int]):
    """
    The Duration class represents the duration of a workout step in seconds.
    """
    def __init__(self, duration: str) -> None:
        self.id = 2
        self.type = "time"
        self.value = int(duration) * 60


class Distance(Condition[float]):
    """
    The Distance class represents a condition based on the distance for a workout step.
    
    Attributes:
        id (int): The identifier for the distance condition, set to 3.
        type (str): The type of condition, set to "distance".
        value (float): The distance value in meters, converted from a string input in kilometers.

    Args:
        distance (str): The distance of the workout step as a string, which can include a comma or a dot as the decimal separator.
        type (DistanceType): The type of distance condition.
    """
    def __init__(self, distance: str, type: DistanceType) -> None:
        self.id = 3
        self.type = "distance"
        
        if type == DistanceType.KILOMETERS:
            self.value = float(distance.replace(",", ".")) * 1000
        elif type == DistanceType.METERS:
            self.value = float(f"0.{distance.replace(',', '')}")