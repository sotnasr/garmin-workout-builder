from abc import ABC, abstractmethod

from models.workout import Workout


class Parser(ABC):
    """
    The Parser interface declares a method for parsing a string value into a Workout. 
    """
    
    @abstractmethod
    def parse(self, value: str) -> Workout:
        raise NotImplementedError