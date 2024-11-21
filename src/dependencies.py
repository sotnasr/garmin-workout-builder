import os
from fastapi import Depends, Query
from garmin.authorization import GarminAuthorization
from garmin.connect import GarminConnectClient
from parser.runfun_parser import RunFunParser

GARMIN_CLIENT_ID = os.getenv("GARMIN_CLIENT_ID")
GARMIN_CLIENT_SECRET = os.getenv("GARMIN_CLIENT_SECRET")

if GARMIN_CLIENT_ID is None:
    raise ValueError("GARMIN_CLIENT_ID environment variable is not set")

if GARMIN_CLIENT_SECRET is None:
    raise ValueError("GARMIN_CLIENT_SECRET environment variable is not set")

def get_garmin_authorization():
    return GarminAuthorization.authenticate(
        email=GARMIN_CLIENT_ID, password=GARMIN_CLIENT_SECRET
    )

def get_garmin_connect_client(
    auth: GarminAuthorization = Depends(get_garmin_authorization),
):
    return GarminConnectClient(
        authorization=auth
    )

def get_workout_parser(
    workout_parser: str = Query(alias="workout_parser")
):
    AVAILABLE_PARSERS = {
        "runfun": RunFunParser,
    }

    parser_class = AVAILABLE_PARSERS.get(workout_parser.lower())
    if not parser_class:
        raise NotImplementedError(f"Parser type '{workout_parser}' is not supported")
    
    return parser_class()
