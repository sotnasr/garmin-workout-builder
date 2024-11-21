import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import workout_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up...")
    yield
    logging.info("Shutting down...")

app = FastAPI(
    title="Garmin Workout API",
    root_path="/api",
    description="API for managing Garmin workouts",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(
    workout_router, prefix="/v1/workout", tags=["workout"]
)

allowed_origins = [
    "http://localhost",
    "http://localhost:8000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
