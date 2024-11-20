from typing import List

from models.step_type import StepType
from models.target import Target, NoTarget
from models.condition import Condition


class Step:
    """
    The Step class represents a single step in a workout.
    It includes the step's name, description, duration, type, and target.
    """
    def __init__(self,
                 step_name: str,
                 description: str,
                 step_type: StepType,
                 target: Target = None,
                 condition: Condition = None):        
        self.step_name = step_name
        self.description = description
        self.condition = condition
        self.step_type = step_type
        self.target = target if target else NoTarget()


class RepeatedStep:
    """
    The RepeatedStep class represents a step that is repeated a specified number of times.
    It contains a list of steps that are executed in sequence for each iteration.
    """
    def __init__(self,
                 iterations: int,
                 steps: List[Step]):
        self.step_type = StepType.Repeat
        self.iterations = iterations
        self.steps = steps