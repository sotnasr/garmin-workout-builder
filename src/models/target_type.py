from enum import Enum


class TargetType(Enum):
    NoTarget = ("no.target", 1)
    Power = ("power.zone", 2)
    Cadence = ("cadence.zone", 3)
    HeartRate = ("heart.rate.zone", 4)
    Speed = ("speed.zone", 5)
    Pace = ("pace.zone", 6)
    
    def __init__(self, key: str, id: int) -> None:
        self.key = key
        self.id = id