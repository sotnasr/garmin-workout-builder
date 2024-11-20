from enum import Enum


class SportType(Enum):
    Running = ("running", 1)
    Cycling = ("cycling", 2)
    Swimming = ("swimming", 4)
    Strength = ("strength_training", 5)
    Cardio = ("cardio_training", 6)
    
    def __init__(self, key: str, id: int) -> None:
        self.key = key
        self.id = id