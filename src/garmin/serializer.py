from typing import List
from models.step import RepeatedStep, Step
from models.target import HeartRateZoneTarget
from models.workout import Workout


class GarminSerializer:
    """
    The GarminSerializer class serializes a Workout object into the JSON format required by Garmin Connect.
    """

    def __init__(self, ) -> None:
        self.step_order = 1

    def serialize(self, workout: Workout) -> dict:
        payload = {
            "sportType": {
                "sportTypeId": workout.type.value,
                "sportTypeKey": workout.type.key,
                "displayOrder": workout.type.value,
            },
            "subSportType": None,
            "workoutName": workout.name,
            "estimatedDistanceUnit": {"unitKey": None},
            "workoutSegments": [],
            "avgTrainingSpeed": None,
            "estimatedDurationInSecs": 0,
            "estimatedDistanceInMeters": 0,
            "estimateType": None,
        }

        segment = {
            "segmentOrder": 1,
            "sportType": {
                "sportTypeId": workout.type.value,
                "sportTypeKey": workout.type.key,
                "displayOrder": workout.type.value,
            },
            "workoutSteps": [],
        }
        
        for step in workout.steps:
            if isinstance(step, RepeatedStep):
                segment["workoutSteps"].append(self.serialize_repeat_step(step))
            else:
                segment["workoutSteps"].append(self.serialize_step(step))

        payload["workoutSegments"].append(segment)
        payload["estimatedDurationInSecs"] = calculate_estimated_duration(payload["workoutSegments"])
        
        return payload


    def serialize_step(self, step: Step) -> dict:
        """
        Convert the Step object into a dictionary that represents a Garmin Connect workout step.
        """

        payload = {
            "type": "ExecutableStepDTO",
            "stepId": self.step_order,
            "stepOrder": self.step_order,
            "stepType": {
                "stepTypeId": step.step_type.value,
                "stepTypeKey": step.step_type.key,
                "displayOrder": step.step_type.value,
            },
            "endCondition": {
                "conditionTypeId": step.condition.id,
                "conditionTypeKey": step.condition.type,
                "displayOrder": step.condition.id,
                "displayable": True,
            },
            "endConditionValue": step.condition.value,
            "description": step.description,
        }

        if isinstance(step.target, HeartRateZoneTarget):
            payload.update(
                {
                    "targetType": step.target.type.key,
                    "targetValueOne": step.target.values[0],
                    "targetValueTwo": step.target.values[1],
                }
            )

        self.step_order += 1
        return payload

    def serialize_repeat_step(self, step: RepeatedStep) -> dict:
        """
        Convert the RepeatedStep object into a dictionary that represents a Garmin Connect workout step.
        """

        payload = {
            "stepId": self.step_order,
            "stepOrder": self.step_order,
            "stepType": {
                "stepTypeId": step.step_type.value,
                "stepTypeKey": step.step_type.key,
                "displayOrder": step.step_type.value,
            },
            "numberOfIterations": step.iterations,
            "smartRepeat": False,
            "endCondition": {
                "conditionTypeId": 7,
                "conditionTypeKey": "iterations",
                "displayOrder": 7,
                "displayable": False,
            },
            "type": "RepeatGroupDTO",
        }

        self.step_order += 1

        result = [self.serialize_step(s) for s in step.steps]
        payload.update(
            {
                "workoutSteps": result
            }
        )

        return payload


def calculate_estimated_duration(workout_segments: list) -> int:
    """
    Calculate the estimated duration of the workout in seconds.
    """

    duration = 0

    for segment in workout_segments:
        for step in segment["workoutSteps"]:
            if step["type"] == "ExecutableStepDTO":
                duration += step["endConditionValue"]
            elif step["type"] == "RepeatGroupDTO":
                # Calculate duration for repeated steps
                repeat_duration = calculate_estimated_duration([{"workoutSteps": step["workoutSteps"]}])
                duration += step["numberOfIterations"] * repeat_duration
                
    return duration