from enum import Enum


class StepType(Enum):
    """
    Enum representing different types of workout steps.
    
    Attributes:
        WarmUp: Represents the warm-up phase of a workout.
        CoolDown: Represents the cool-down phase of a workout.
        Interval: Represents an interval phase of a workout.
        Recovery: Represents the recovery phase of a workout.
        Rest: Represents the rest phase of a workout.
        Repeat: Represents a repeat phase of a workout.
    """
    WarmUp = ("warmup", 1)
    CoolDown = ("cooldown", 2)
    Interval = ("interval", 3)    
    Recovery = ("recovery", 4)
    Rest = ("rest", 5)
    Repeat = ("repeat", 6)
    
    def __init__(self, key: str, id: int) -> None:
        self.key = key
        self.id = id