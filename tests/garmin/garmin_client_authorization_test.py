import pytest
from unittest.mock import patch

from garmin.authorization import GarminAuthorization
from garmin.exceptions import GarminLoginError, GarminServiceError


@patch('garmin.authorization.GarminAuthorization.authenticate')
def test_garmin_authorization_invalid_credentials(mock_authenticate):
    """Test authentication fails with invalid credentials"""
    mock_authenticate.side_effect = GarminLoginError("Invalid credentials")
    with pytest.raises(GarminLoginError) as exc:
        GarminAuthorization.authenticate(
            email="invalid@example.com",
            password="wrongpassword"
        )
    assert "Invalid credentials" in str(exc.value)

@patch('garmin.authorization.GarminAuthorization.authenticate')
def test_garmin_authorization_service_error(mock_authenticate):
    """Test authentication fails when service is unavailable"""
    mock_authenticate.side_effect = GarminServiceError("Failed to connect to Garmin SSO")
    with pytest.raises(GarminServiceError) as exc:
        GarminAuthorization.authenticate(
            email="test@example.com",
            password="password",
            connect_url="https://invalid.garmin.com"
        )
    assert "Failed to connect to Garmin SSO" in str(exc.value)

@pytest.mark.parametrize("email,password", [
    ("", "password"),
    ("test@example.com", ""),
    ("", ""),
    (None, "password"),
    ("test@example.com", None)
])
def test_garmin_authorization_invalid_input(email, password):
    """Test authentication fails with invalid input parameters"""
    with pytest.raises(Exception):
        GarminAuthorization.authenticate(email=email, password=password)