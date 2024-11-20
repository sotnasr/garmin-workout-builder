from typing import List, Union

from models.sport_type import SportType
from models.step import RepeatedStep, Step


class Workout:
    """
    The Workout class represents a Garmin workout that consists of a series of steps.
    Attributes:
        name (str): The name of the workout.
        type (SportType): The type of sport for the workout.
        steps (List[Step]): A list of steps that make up the workout.
    """
    
    def __init__(self,
                 name: str,
                 type: SportType = SportType.Running) -> None:
        self.name: str = name
        self.type: SportType = type
        self.steps: List[Union[Step, RepeatedStep]] = []
    
    def add_step(self, step: Step) -> None:
        self.steps.append(step)