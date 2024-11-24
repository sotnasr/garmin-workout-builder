from datetime import date
from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dependencies import get_garmin_connect_client, get_workout_parser
from garmin.connect import GarminConnectClient
from garmin.exceptions import GarminWorkoutIdError
from parser.parser import Parser


router = APIRouter()


class CreateWorkoutRequest(BaseModel):
    """
    Request model for creating a workout in Garmin Connect.

    Attributes:
        workout_expr: A string expression defining the workout structure.
            Example: "10' zr + 5x (400m ze + 1' ra) + 15' zr"
        workout_schedule: Optional date when the workout should be scheduled.
            If not provided, the workout will only be created but not scheduled.
    """
    workout_expr: str
    workout_schedule: Optional[date] = None


@router.post(
    "/parse/create",
    description="Parses a workout expression and creates a workout in Garmin Connect.",
)
async def parse_and_create_workout(
    workout_parser: str,
    request: Annotated[
        CreateWorkoutRequest,
        Body(
            description="Request body containing the workout expression and parser type",
            examples=[
                {
                    "workout_expr": "10' zr + 5x (400m ze + 1' ra) + 15' zr",
                    "workout_schedule": "2024-10-10",
                },
            ],
        ),
    ],
    parser: Parser = Depends(get_workout_parser),
    client: GarminConnectClient = Depends(get_garmin_connect_client),
) -> Response:
    try:
        workout = parser.parse(request.workout_expr)
        workout_id = client.create_workout(workout)

        if request.workout_schedule is not None:
            client.schedule_workout(workout_id, request.workout_schedule)

        return Response(status_code=201)
    except NotImplementedError:
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_parser",
                "message": f"Parser type '{workout_parser}' is not supported"
            },
        )
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_workout",
                "message": f"Invalid workout format: {str(ve)}"
            },
        )
    except GarminWorkoutIdError:
        return JSONResponse(
            status_code=503,
            content={
                "error": "garmin_service_error",
                "message": "Unable to create workout in Garmin Connect"
            },
        )
    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": "An unexpected error occurred while processing the request",
                "detail": str(ex)
            },
        )
