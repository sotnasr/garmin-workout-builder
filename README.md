# Garmin Workout Builder

This project is a Python-based tool for parsing and serializing workout routines, specifically designed to integrate with Garmin Connect. The core functionality is provided by the `RunFunParser` class, which interprets workout expressions and converts them into structured `Workout` objects. These objects can then be serialized into the JSON format required by Garmin Connect using the `GarminSerializer` class.

## Features:

- **Parsing Workouts**: The `RunFunParser` class can parse complex workout expressions, including repeated steps and heart rate zone targets.
- **Heart Rate Zone Configuration**: The project includes a `HeartRateZoneConfig` class to manage and validate heart rate zones.
- **Serialization**: The `GarminSerializer` class converts `Workout` objects into the JSON format required by Garmin Connect.
- **Extensibility**: The project is designed with extensibility in mind, allowing for easy addition of new parsing rules and serialization formats.