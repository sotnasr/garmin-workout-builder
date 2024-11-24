from enum import Enum


class SportType(Enum):
    """
    SportType is an enumeration representing different types of sports activities.

    Attributes:
        Running (tuple): Represents running activity with a key "running" and id 1.
        Cycling (tuple): Represents cycling activity with a key "cycling" and id 2.
        Swimming (tuple): Represents swimming activity with a key "swimming" and id 4.
        Strength (tuple): Represents strength training activity with a key "strength_training" and id 5.
        Cardio (tuple): Represents cardio training activity with a key "cardio_training" and id 6.
    """
    Running = ("running", 1)
    Cycling = ("cycling", 2)
    Swimming = ("swimming", 4)
    Strength = ("strength_training", 5)
    Cardio = ("cardio_training", 6)
    
    def __init__(self, key: str, id: int) -> None:
        self.key = key
        self.id = id