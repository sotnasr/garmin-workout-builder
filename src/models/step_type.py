from enum import Enum


class StepType(Enum):
    WarmUp = ("warmup", 1)
    CoolDown = ("cooldown", 2)
    Interval = ("interval", 3)    
    Recovery = ("recovery", 4)
    Rest = ("rest", 5)
    Repeat = ("repeat", 6)
    
    def __init__(self, key: str, id: int) -> None:
        self.key = key
        self.id = id