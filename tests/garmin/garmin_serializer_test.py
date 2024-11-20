import pytest

from parser.runfun_parser import RunFunParser
from garmin.serializer import GarminSerializer

@pytest.fixture
def parser():
    return RunFunParser()

@pytest.fixture
def serializer():
    return GarminSerializer()


def test_parse_with_repetitions_and_serialize(parser, serializer):
    """Test parsing workout with repetitions: 15' zr + 2x (8' zm + 5' zr) + 10' zr"""
    workout = parser.parse("15' zr + 2x (8' zm + 5' zr) + 10' zr")
    payload = serializer.serialize(workout)