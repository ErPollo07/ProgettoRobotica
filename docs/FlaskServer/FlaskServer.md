# Flask server

## Overview

Between the communication of the data from the robots to Thingsboard, a Flask server is used to handle the requests and responses.

The code is split between two main files:

- `main.py`: This file create the flask server at 127.0.0.10:8080 and register the endpoints to handle the requests from the robots.
- `robot_bp.py`: This file contains the route to send data to the Thingsboard server.

## Directory Structure

```txt
└── 📁flask_server
    └── 📁__pycache__
        └── ...
    └── 📁blueprints
        └── 📁__pycache__
            └── ...
        ├── __init__.py
        ├── camera_bp.py
        ├── robot_1_bp.py
        ├── robot_2_bp.py
        └── robot_bp.py
    └── 📁templates
        └── index.html
    ├── __init__.py
    ├── .env
    ├── .env.template.txt
    └── main.py
```

## Endpoints

### General endpoints

These endpoints are defined in robot_bp.py and handle general robot operations.

#### POST `/robot/test`

- **Description**: Test endpoint for basic communication
- **Request**: JSON message
- **Response**: `{"status": "success", "message": "Message received"}` (HTTP 200)

#### POST `/robot/movement_executed`

- **Description**: Handle movement completion notifications from the robot
- **Request JSON**:

  ```json
  {
    "ts": <timestamp>,
    "robot_id": <robot_identifier>,
    "time": <timeOfExecution>
  }
  ```

- **Response**: `{"status": "ok"}` (HTTP 200) or error message (HTTP 400/500)
- **Behavior**: Parses the payload and sends telemetry data to Thingsboard

#### POST `/robot/infrared_sensor_event`

- **Description**: Handle infrared sensor event notifications from the robot
- **Request JSON**:

  ```json
  {
    "ts": <timestamp>,
    "robot_id": <robot_identifier>,
    "status": <"ok"|"error">
  }
  ```

- **Response**: `{"status": "success"}` (HTTP 200) or error message (HTTP 400/500)
- **Behavior**: Logs infrared sensor status and sends telemetry to Thingsboard

### Robot 1

These endpoints are defined in robot_1_bp.py and handle Robot 1 specific operations.

#### GET `/robot1/can_collect`

- **Description**: Endpoint that Robot 1 polls to ask if it can collect the block
- **Response**: `{"status": "ok", "message": true|false}` (HTTP 200)
- **Behavior**: Returns `true` if the block has been dropped by Robot 2, then resets the flag to `false`

#### POST `/robot1/block_dropped`

- **Description**: Called from Robot 2 to signal that the block has been dropped at the collection point
- **Response**: `{"status": "ok", "message": "success"}` (HTTP 200)
- **Behavior**: Sets the internal `can_collect_var` flag to `true` so Robot 1 can proceed with collection

### Robot 2

These endpoints are defined in robot_2_bp.py and handle Robot 2 specific operations.

#### POST `/robot2/block_dropped`

- **Description**: Called from Robot 2 to signal that it has reached the drop point
- **Response**: `{"status": "ok", "message": "success"}` (HTTP 200)
- **Behavior**: Makes a call to Robot 1's `/robot1/block_dropped` endpoint to notify Robot 1 that the block is ready to be collected

#### GET `/robot2/detect_color`

- **Description**: Robot 2 polls this endpoint when it's above the sensor to detect the color
- **Response**: `{"status": "ok", "message": <color>}` (HTTP 200)
- **Behavior**: Calls the camera `/camera/detect_color` endpoint (with retry logic, max 3 attempts). Sets `can_drop_var` to `true` when color is detected

#### GET `/robot2/can_drop`

- **Description**: Robot 2 polls this endpoint to check if it can drop the block
- **Response**: `{"status": "ok", "message": true|false}` (HTTP 200)
- **Behavior**: Returns `true` if the color has been detected, then resets the flag to `false`

### Camera

These endpoints are defined in camera_bp.py and handle camera operations.

#### GET `/camera/detect_color`

- **Description**: Detects the color at the sensor position
- **Response**: `{"status": "ok", "message": <color>}` (HTTP 200) or error message (HTTP 500)
- **Behavior**:
  - Calls the external camera service at `http://127.0.0.1:15001/get_color`
  - Prepares telemetry message with timestamp and color value
  - Posts the telemetry data to Thingsboard for device "3" (camera device)
  - Returns the detected color as a string

## Data flow

The data flow of the project is drawn in the following diagram:

![Data Flow Diagram](/docs/_sheme/data-flow.excalidraw.svg)
