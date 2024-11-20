from abc import ABC
from typing import TypeVar, Generic


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
    def __init__(self, duration: str):
        self.id = 2
        self.type = "time"
        self.value = int(duration) * 60


class Distance(Condition[float]):
    """
    The Distance class represents the distance of a workout step in kilometers.
    """
    def __init__(self, distance: str):
        self.id = 1
        self.type = "distance"
        self.value = float(distance.replace(",", ".")) * 1000