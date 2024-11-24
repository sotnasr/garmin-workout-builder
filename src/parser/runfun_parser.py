import re
from typing import List, Union

from models.condition import Distance, Duration
from models.distance_type import DistanceType
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
    PATTERN_DISTANCE = r"(\d+(?:,\d+)?)(km|m)\s*(?:ritmo\s*de\s*prova\s*(\d+)(km|m))?"
    PATTERN_DURATION = r"(\d+)'([a-zA-Z]+)"
    PATTERN_REPEAT = r"(\d+)x\(([^\)]+)\)"
    PATTERN_HEART_RATE_ZONE = r"\b(zr|zm|zs|ze|zt)\b"

    def parse(self, value: str) -> Workout:
        value = self.normalize_heart_rate_zones(value)
        workout = Workout(value)
        steps = self.parse_tokens(self.tokenize(value))

        for step in steps:
            workout.add_step(step)

        return workout

    def normalize_heart_rate_zones(self, value: str) -> str:
        normalized = re.sub(r"\'", "", value)
        return re.sub(self.PATTERN_HEART_RATE_ZONE, r"'\1", normalized)

    def tokenize(self, value: str) -> List[str]:
        normalized = value.replace(" ", "")
        return re.findall(self.PATTERN_TOKEN, normalized)

    def parse_tokens(self, tokens: List[str], repeated: bool = False) -> List[Union[Step, RepeatedStep]]:
        steps = []
        total_steps = len(tokens)

        for position, token in enumerate(tokens):
            step_type = self.get_step_type(position, total_steps, repeated)
            step = self._parse_single_token(token, step_type)
            steps.append(step)

        return steps

    def _parse_single_token(self, token: str, step_type: StepType) -> Union[Step, RepeatedStep]:
        if re.match(self.PATTERN_DISTANCE, token):
            return self._create_distance_step(token, step_type)
        elif re.match(self.PATTERN_DURATION, token):
            return self._create_duration_step(token, step_type)
        elif re.match(self.PATTERN_REPEAT, token):
            return self._create_repeated_step(token)
        else:
            raise ValueError(f"The token {token} could not be recognized.")

    def _create_distance_step(self, token: str, step_type: StepType) -> Step:
        m = re.match(self.PATTERN_DISTANCE, token)
        distance, unit = m.groups()[:2]
        
        distance_type = {
            "km": DistanceType.KILOMETERS,
            "m": DistanceType.METERS
        }.get(unit, None)

        if not distance_type:
            raise ValueError(f"Invalid unit: {unit}")

        return Step(
            step_name=f"{distance}{unit}",
            description=f"Run {distance} {unit}",
            condition=Distance(distance, distance_type),
            step_type=step_type
        )

    def _create_duration_step(self, token: str, step_type: StepType) -> Step:
        m = re.match(self.PATTERN_DURATION, token)
        duration, zone = m.groups()
        
        if not HeartRateZoneConfig.validate_zone(zone.upper()):
            raise ValueError(f"Invalid heart rate zone: {zone}")

        return Step(
            step_name=f"{duration}' {zone}",
            description=f"Run for {duration} minutes in {zone} zone",
            condition=Duration(duration),
            step_type=step_type,
            target=HeartRateZoneTarget(HeartRateZoneConfig.get_zone_range(zone.upper()))
        )

    def _create_repeated_step(self, token: str) -> RepeatedStep:
        m = re.match(self.PATTERN_REPEAT, token)
        repeat_count, repeat_token = m.groups()
        inner_tokens = re.split(r"\s*\+\s*", repeat_token)
        repeat_steps = self.parse_tokens(inner_tokens, True)
        
        return RepeatedStep(
            iterations=int(repeat_count),
            steps=repeat_steps
        )

    @staticmethod
    def get_step_type(position: int, total_steps: int, repeated: bool = False) -> StepType:
        if repeated:
            if position == 0:
                return StepType.Interval
            elif position == total_steps - 1:
                return StepType.Recovery
        else:
            if position == 0:
                return StepType.WarmUp
            elif position == total_steps - 1:
                return StepType.CoolDown
        return StepType.Interval