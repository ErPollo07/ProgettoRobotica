# Flask server

## Overview

Between the comunication of the data from the robots to Thingsboard, a Flask server is used to handle the requests and responses.

The code is split between two main files:

- `main.py`: This file create the flask server at 127.0.0.10:8080 and register the endpoints to handle the requests from the robots.
- `robot_bp.py`: This file contains the route to send data to the Thingsboard server.

## Directory Structure

```txt
project/
│
├── main.py           # Main application file to run the server
└── blueprints/
    └── robot_bp.py   # Blueprint containing robot-related endpoints
```

## Endpoints

### Main

- **/test**: A test endpoint to verify the server is running. It returns a simple "Server is running" message.

- **/robot/status**: This endpoint receives GET requests to check if the server is running.

- **/robot/movement_executed**: This endpoint receives POST requests with JSON data containing information about the robot's movement execution. The data is then forwarded to the Thingsboard server.

- **/robot/infrared_sensor_event**: This endpoint receives POST requests with JSON data about infrared sensor events from the robot. The data is forwarded to the Thingsboard server.

- **/robot/infrared_sensor_error**: This endpoint handles POST requests with JSON data regarding infrared sensor errors from the robot. The data is sent to the Thingsboard server.

- **/robot/color_sensor_event**: This endpoint receives POST requests with JSON data about color sensor events from the robot. The data is forwarded to the Thingsboard server.
