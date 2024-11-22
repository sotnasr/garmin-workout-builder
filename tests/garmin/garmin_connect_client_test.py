import pytest
from unittest.mock import patch, MagicMock

from garmin.authorization import GarminAuthorization
from garmin.connect import GarminConnectClient
from parser.runfun_parser import RunFunParser

@pytest.fixture
def mock_authorization():
    with patch('garmin.authorization.GarminAuthorization.authenticate') as mock_auth:
        mock_auth.return_value = MagicMock()
        yield mock_auth

@pytest.fixture
def mock_client():
    with patch('garmin.client.GarminConnectClient') as mock_client:
        yield mock_client

@pytest.fixture
def mock_parser():
    with patch('parser.runfun_parser.RunFunParser') as mock_parser:
        mock_instance = mock_parser.return_value
        mock_instance.parse.return_value = MagicMock(name="Test workout")
        yield mock_parser

@pytest.fixture
def test_credentials():
    return {
        "email": "test@example.com",
        "password": "test_password"
    }

def test_garmin_connect_client_create_workout(mock_authorization, mock_client, mock_parser, test_credentials):
    """Test Garmin client authorization and workout creation."""
    authorization = GarminAuthorization.authenticate(**test_credentials)
    
    parser = RunFunParser()
    workout = parser.parse("15' zr + 2x (8' zm + 5' zr) + 10' zr")
    workout.name = "Test workout"
    
    client = GarminConnectClient(authorization)
    client.create_workout(workout)
    
    mock_authorization.assert_called_once_with(**test_credentials)
    mock_parser.return_value.parse.assert_called_once()
    mock_client.return_value.create_workout.assert_called_once()

def test_garmin_connect_client_update_workout(mock_authorization, mock_client, mock_parser, test_credentials):
    """Test Garmin client workout update."""
    authorization = GarminAuthorization.authenticate(**test_credentials)
    
    parser = RunFunParser()
    workout = parser.parse("20' zr + 3x (10' zm + 5' zr) + 15' zr")
    workout.name = "Updated workout"
    
    client = GarminConnectClient(authorization)
    workout_id = 12345
    client.update_workout(workout_id, workout)
    
    mock_authorization.assert_called_once_with(**test_credentials)
    mock_parser.return_value.parse.assert_called_once()
    mock_client.return_value.update_workout.assert_called_once_with(workout_id, workout)