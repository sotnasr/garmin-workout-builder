import re
from typing import List, Union

from models.condition import Distance, Duration
from models.sport_type import SportType
from models.step import RepeatedStep, Step, StepType
from models.target import HeartRateZoneTarget
from parser.parser import Parser
from models.workout import Workout

from enum import Enum
from typing import Dict, List, Tuple

class HeartRateZone(Enum):
    ZR = "ZR"
    ZM = "ZM"
    ZS = "ZS"
    ZE = "ZE"
    ZT = "ZT"

class HeartRateZoneConfig:
    """
    Configuration class for heart rate zones, defining the range of heart rates for each zone.
    """
    
    ZONES: Dict[HeartRateZone, Tuple[int, int]] = {
        HeartRateZone.ZR: (157, 167),
        HeartRateZone.ZM: (167, 176), 
        HeartRateZone.ZS: (176, 186),
        HeartRateZone.ZE: (186, 196),
        HeartRateZone.ZT: (196, 216)
    }

    @classmethod
    def get_zone_range(cls, zone_key: str) -> Tuple[int, int]:
        """
        Get min/max heart rate for a zone by key
        """
        zone = HeartRateZone[zone_key]
        return cls.ZONES[zone]

    @classmethod
    def validate_zone(cls, zone_key: str) -> bool:
        """
        Validate if zone key exists
        """
        try:
            HeartRateZone[zone_key]
            return True
        except KeyError:
            return False


class RunFunParser(Parser):
    """
    The RunFunParser class is a concrete implementation of the Parser interface for advisor RunFun.
    """

    PATTERN_TOKEN = r"\d+x\([^\)]+\)|\d+(?:,\d+)?km(?:ritmodeprova\d+km)?|\d+\'[a-zA-Z]+"
    PATTERN_DISTANCE = r"(\d+(?:,\d+)?)km\s*(?:ritmo\s*de\s*prova\s*(\d+)km)?"
    PATTERN_DURATION = r"(\d+)'([a-zA-Z]+)"
    PATTERN_REPEAT = r"(\d+)x\(([^\)]+)\)"

    def parse(self, value: str) -> Workout:
        workout = Workout(value)
        steps = self._parse_tokens(self._tokenize(value))

        for step in steps:
            workout.add_step(step)

        return workout

    def _tokenize(self, value: str) -> List[str]:
        normalized = value.replace(" ", "")
        return re.findall(self.PATTERN_TOKEN, normalized)

    def _parse_tokens(self, tokens: List[str]) -> List[Union[Step, RepeatedStep]]:
        steps = []
        total_steps = len(tokens)

        for position, token in enumerate(tokens):
            step_type = self._get_step_type(position, total_steps)
            
            if re.match(self.PATTERN_DISTANCE, token):
                m = re.match(self.PATTERN_DISTANCE, token)
                distance, race_pace = m.groups()
                steps.append(Step(
                    step_name=f"{distance}km",
                    description=f"Run {distance} kilometers",
                    condition=Distance(distance),
                    step_type=step_type
                ))
            elif re.match(self.PATTERN_DURATION, token):
                m = re.match(self.PATTERN_DURATION, token)
                duration, zone = m.groups()
                if not HeartRateZoneConfig.validate_zone(zone.upper()):
                    raise ValueError(f"Invalid heart rate zone: {zone}")
                steps.append(Step(
                    step_name=f"{duration}' {zone}",
                    description=f"Run for {duration} minutes in {zone} zone",
                    condition=Duration(duration),
                    step_type=step_type,
                    target=HeartRateZoneTarget(HeartRateZoneConfig.get_zone_range(zone.upper()))
                ))
            elif re.match(self.PATTERN_REPEAT, token):
                m = re.match(self.PATTERN_REPEAT, token)
                repeat_count, repeat_token = m.groups()
                inner_tokens = re.split(r"\s*\+\s*", repeat_token)
                repeat_steps = self._parse_tokens(inner_tokens)
                
                steps.append(RepeatedStep(
                    iterations=int(repeat_count),
                    steps=repeat_steps
                ))
            else:
                raise ValueError(f"The token {token} could not be recognized.")

        return steps

    @staticmethod
    def _get_step_type(position: int, total_steps: int) -> StepType:
        if position == 0:
            return StepType.WarmUp
        if position == total_steps - 1:
            return StepType.CoolDown
        return StepType.Interval