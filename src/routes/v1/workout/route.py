from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from dependencies import get_garmin_connect_client, get_workout_parser
from garmin.connect import GarminConnectClient
from garmin.exceptions import GarminWorkoutIdError
from parser.parser import Parser


router = APIRouter()

@router.put(
    "/parse/create",
    description="Parses a workout expression and creates a workout in Garmin Connect."
)
async def parse_and_create_workout(
    workout_expr: str,
    workout_parser: str,
    workout_schedule: Optional[date] = None,
    parser: Parser = Depends(get_workout_parser),
    client: GarminConnectClient = Depends(get_garmin_connect_client),
) -> Response:
    try:
        workout = parser.parse(workout_expr)
        workout_id = client.create_workout(workout)

        if workout_schedule is not None:
            client.schedule_workout(workout_id, workout_schedule)

        return Response(status_code=201)
    except NotImplementedError:
        return JSONResponse(
            status_code=400,
            content={"message": f"Parser type '{workout_parser}' is not supported"},
        )
    except GarminWorkoutIdError:
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to get workout id from Garmin Connect"},
        )
    except Exception as ex:
        return JSONResponse(
            status_code=500, content={"message": f"Failed to create workout: {str(ex)}"}
        )
