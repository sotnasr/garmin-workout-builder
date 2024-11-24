from enum import Enum


class TargetType(Enum):
    """
    Enum representing different types of workout targets.

    Attributes:
        NoTarget (tuple): Represents no specific target with key "no.target" and id 1.
        Power (tuple): Represents a power zone target with key "power.zone" and id 2.
        Cadence (tuple): Represents a cadence zone target with key "cadence.zone" and id 3.
        HeartRate (tuple): Represents a heart rate zone target with key "heart.rate.zone" and id 4.
        Speed (tuple): Represents a speed zone target with key "speed.zone" and id 5.
        Pace (tuple): Represents a pace zone target with key "pace.zone" and id 6.
    """
    NoTarget = ("no.target", 1)
    Power = ("power.zone", 2)
    Cadence = ("cadence.zone", 3)
    HeartRate = ("heart.rate.zone", 4)
    Speed = ("speed.zone", 5)
    Pace = ("pace.zone", 6)
    
    def __init__(self, key: str, id: int) -> None:
        self.key = key
        self.id = id