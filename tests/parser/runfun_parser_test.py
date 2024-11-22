import pytest

from models.condition import Distance, Duration
from models.step import RepeatedStep, Step
from models.target import HeartRateZoneTarget
from parser.runfun_parser import HeartRateZoneConfig, RunFunParser


@pytest.fixture
def parser():
    return RunFunParser()


def test_parse_simple_duration(parser):
    """Test parsing simple duration workout: 50' zr"""
    workout = parser.parse("50' zr")

    assert len(workout.steps) == 1
    step = workout.steps[0]
    assert isinstance(step, Step)

    assert isinstance(step.target, HeartRateZoneTarget)
    assert step.target.values == HeartRateZoneConfig.get_zone_range("ZR")


def test_parse_with_repetitions(parser):
    """Test parsing workout with repetitions: 15' zr + 2x (8' zm + 5' zr) + 10' zr"""
    workout = parser.parse("15' zr + 2x (8' zm + 5' zr) + 10' zr")

    assert len(workout.steps) == 3
    # First step
    assert isinstance(workout.steps[0], Step)
    assert isinstance(workout.steps[0].condition, Duration)
    assert workout.steps[0].condition.value == 900
    
    assert isinstance(workout.steps[0].target, HeartRateZoneTarget)
    assert workout.steps[0].target.values == HeartRateZoneConfig.get_zone_range("ZR")

    # Repetition block
    repeat_step = workout.steps[1]
    assert isinstance(repeat_step, RepeatedStep)
    assert repeat_step.iterations == 2
    assert len(repeat_step.steps) == 2
    
    assert isinstance(workout.steps[0].condition, Duration)
    assert repeat_step.steps[0].condition.value == 480
    assert isinstance(repeat_step.steps[0].target, HeartRateZoneTarget)
    assert repeat_step.steps[0].target.values == HeartRateZoneConfig.get_zone_range("ZM")

    assert isinstance(repeat_step.steps[1].condition, Duration)
    assert repeat_step.steps[1].condition.value == 300
    assert isinstance(repeat_step.steps[1].target, HeartRateZoneTarget)
    assert repeat_step.steps[1].target.values == HeartRateZoneConfig.get_zone_range("ZR")
    
    # Last step
    assert isinstance(workout.steps[2], Step)
    assert isinstance(workout.steps[2].condition, Duration)
    assert workout.steps[2].condition.value == 600
    assert isinstance(workout.steps[2].target, HeartRateZoneTarget)
    assert workout.steps[2].target.values == HeartRateZoneConfig.get_zone_range("ZR")


def test_parse_with_distance_and_pace(parser):
    """Test parsing workout with distance: 20' zr + 1,5km ritmo de prova 5km + 10' zr"""
    workout = parser.parse("20' zr + 1,5km ritmo de prova 5km + 10' zr")
    
    assert len(workout.steps) == 3
    # First step
    assert isinstance(workout.steps[0].condition, Duration)
    assert workout.steps[0].condition.value == 1200
    assert isinstance(workout.steps[0].target, HeartRateZoneTarget)
    assert workout.steps[0].target.values == HeartRateZoneConfig.get_zone_range("ZR")
    
    # Second step
    # Implement...
    assert isinstance(workout.steps[1].condition, Distance)
    assert workout.steps[1].condition.value == 1500.0
    
    # Last step
    assert isinstance(workout.steps[2].condition, Duration)
    assert workout.steps[2].condition.value == 600
    assert isinstance(workout.steps[2].target, HeartRateZoneTarget)
    assert workout.steps[2].target.values == HeartRateZoneConfig.get_zone_range("ZR")


def test_parse_with_repeats_and_distance(parser):
    """Test parsing workout with repeats and distance: 10' zr + 5x (400m ze + 1' ra) + 15' zr"""
    workout = parser.parse("10' zr + 5x (400m ze + 1' ra) + 15' zr")
    
    assert len(workout.steps) == 3
    # First step
    assert isinstance(workout.steps[0].condition, Duration)
    assert workout.steps[0].condition.value == 600
    assert isinstance(workout.steps[0].target, HeartRateZoneTarget)
    assert workout.steps[0].target.values == HeartRateZoneConfig.get_zone_range("ZR")
    
    # Second step (repeats)
    assert isinstance(workout.steps[1], RepeatedStep)
    assert workout.steps[1].repeat_count == 5
    assert len(workout.steps[1].steps) == 2
    
    # First step in repeats
    assert isinstance(workout.steps[1].steps[0].condition, Distance)
    assert workout.steps[1].steps[0].condition.value == 400
    assert isinstance(workout.steps[1].steps[0].target, HeartRateZoneTarget)
    assert workout.steps[1].steps[0].target.values == HeartRateZoneConfig.get_zone_range("ZE")
    
    # Second step in repeats
    assert isinstance(workout.steps[1].steps[1].condition, Duration)
    assert workout.steps[1].steps[1].condition.value == 60
    assert isinstance(workout.steps[1].steps[1].target, HeartRateZoneTarget)
    assert workout.steps[1].steps[1].target.values == HeartRateZoneConfig.get_zone_range("RA")
    
    # Last step
    assert isinstance(workout.steps[2].condition, Duration)
    assert workout.steps[2].condition.value == 900
    assert isinstance(workout.steps[2].target, HeartRateZoneTarget)
    assert workout.steps[2].target.values == HeartRateZoneConfig.get_zone_range("ZR")