from __future__ import annotations
from http.cookiejar import CookieJar
from re import search
from copy import deepcopy
from datetime import datetime, timedelta

import cloudscraper


class GarminAuthorization:
    """
    Garmin authorization class for handling authentication and token management with Garmin Connect.
    Attributes:
        _token (str): The bearer token for authorization.
        _expires_in (int): The time in seconds until the token expires.
        _refresh_token (str): The token used to refresh the bearer token.
        _refresh_token_expires_in (int): The time in seconds until the refresh token expires.
    Methods:
        __init__(token: str, expires_in: int, refresh_token: str, refresh_token_expires_in: int):
            Initializes the GarminAuthorization instance with the provided tokens and expiration times.
        authenticate(email: str, password: str, connect_url: str = "https://connect.garmin.com", sso_url: str = "https://sso.garmin.com") -> GarminAuthorization:
            Static method to authenticate with Garmin Connect using the provided email and password.
            Returns an instance of GarminAuthorization with the obtained tokens.
            Raises an exception if authentication fails.
    """

    def __init__(
        self,
        token: str,
        expires_in: int,
        refresh_token: str,
        refresh_token_expires_in: int,
        cookies: CookieJar,
    ):
        self._token = token
        self._epxires_in = expires_in
        self._refresh_token = refresh_token
        self._refresh_token_expires_in = refresh_token_expires_in
        self._cookies = cookies
        self._logged_in = datetime.now()

    @property
    def token(self) -> str:
        return self._token

    @property
    def cookies(self) -> CookieJar:
        return self._cookies

    def is_token_expired(self) -> bool:
        return (self._logged_in + timedelta(seconds=self._epxires_in) < datetime.now())

    @staticmethod
    def authenticate(
        email: str,
        password: str,
        connect_url: str = "https://connect.garmin.com",
        sso_url: str = "https://sso.garmin.com",
    ) -> GarminAuthorization:
        """
        Static method to authenticate with Garmin Connect and obtain a bearer token.
        Returns an instance of GarminAuthorization.
        """
        extract_ticket_id = lambda x: search(
            r'response_url\s*=\s*".*\?ticket=(.+)"', x
        ).group(1)

        try:
            session = cloudscraper.CloudScraper()

            r = session.post(
                url=f"{sso_url}/sso/signin",
                headers={"origin": "https://sso.garmin.com"},
                params={
                    "clientId": "GarminConnect",
                    "service": "https://connect.garmin.com/modern",
                },
                data={
                    "username": email,
                    "password": password,
                    "embed": "false",
                },
            )

            if r.status_code != 200:
                raise Exception("Authentication failed")

            ticket_id = extract_ticket_id(r.text)
            if not ticket_id:
                raise Exception("Authentication failed")

            r = session.get(url=f"{connect_url}/modern?ticket={ticket_id}")
            if r.status_code != 200:
                raise Exception("Authentication failed")

            r = session.post(url=f"{connect_url}/modern/di-oauth/exchange")
            if r.status_code != 200:
                raise Exception("Authentication failed")

            response = r.json()
            if "access_token" not in response and "refresh_token" not in response:
                raise Exception("Authentication failed")

            return GarminAuthorization(
                token=response["access_token"],
                expires_in=response["expires_in"],
                refresh_token=response["refresh_token"],
                refresh_token_expires_in=response["refresh_token_expires_in"],
                cookies=deepcopy(session.cookies),
            )
        except Exception as e:
            raise Exception("Authentication failed") from e
