from abc import ABC
from typing import List

from models.target_type import TargetType


class Target(ABC):
    """
    The Target interface declares a method for getting the target value of a Workout.
    """

    type: TargetType
    values: List[int]
    unit: str

    def __init__(self, values: List[int]):
        if len(values) != 2:
            raise ValueError("Target values must have exactly 2 elements")
        self.values = values


class HeartRateZoneTarget(Target):
    """
    The HeartRateZoneTarget class represents a target that is based on heart rate zones.
    """

    def __init__(self, values: List[int]):
        super().__init__(values)
        self.type = TargetType.HeartRate
        self.unit = "bpm"


class NoTarget(Target):
    """
    The NoTarget class represents a target that is based on heart rate zones.
    """

    def __init__(self):
        self.type = TargetType.NoTarget
