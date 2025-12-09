from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os, requests

bp = Blueprint('robot', __name__, url_prefix='/robot')

load_dotenv()

idToAccessToken: dict = {
    "1": str(os.getenv("ACCESS_TOKEN_1")),
    "2": str(os.getenv("ACCESS_TOKEN_2")),
    "3": str(os.getenv("ACCESS_TOKEN_3")),
}

BASE_LINK = str(os.getenv("BASE_LINK"))
print(f"{BASE_LINK=}")
def getTelemetryLink(robot_id: int):
    link = BASE_LINK + idToAccessToken[robot_id] + "/telemetry"
    print(f"{link=}")
    return link


@bp.route("/test", methods=['POST'])
def api_test():
    message = request.get_json()

    print("Received message:", message['data'])

    return jsonify({"status": "success", "message": "Message received"}), 200


@bp.route("/movement_executed", methods=['POST'])
def movement_executed():
    """
    Handle movement completion notifications from the robot.

    This endpoint receives a POST request containing a JSON payload that
    describes the execution of a movement (e.g., robot identifier,
    completion status and final position). The data is parsed
    and logged for tracking and debugging purposes.

    Expected JSON example:
    {
        "ts": <timestamp>,
        "robot_id": <robot_identifier>,
        "time": <timeOfExecution>
    }

    Returns
    ------
        flask.Response: A JSON response with:
            {
                "status": "success"
            }
        and HTTP status code 200.

    Notes:
    ------
        - No validation is currently applied to the payload.
        - Logging is performed via standard output; consider using
          a structured logging system for production environments.
        - Extend with error handling and data persistence as needed.
    """
    # TODO complete the implementation

    message = request.get_json()

    data = {
        "ts": message["ts"],
        "time": message["time"]
    }

    req = requests.post(url=getTelemetryLink(int(message["robot_id"])), json=data)

    print(f"{req=}")
    
    return jsonify({"status": "success"}), 200


@bp.route("/infrared_sensor_event", methods=['POST'])
def infrared_sensor_event():
    """
    Handle infrared sensor event notifications from the robot.

    The payload:
    {
        "ts": <timestamp>,
        "robot_id": <robot_identifier>
    }
    """
    # TODO complete the implementation and documentation
    message = request.get_json()

    print(f"{message=}")

    return jsonify({"status": "success"}), 200


@bp.route("/infrared_sensor_error", methods=['POST'])
def infrared_sensor_error():
    """
    """
    # TODO complete the implementation and documentation
    message = request.get_json()

    print(f"{message=}")

    return jsonify({"status": "success"}), 200


@bp.route("/color_sensor_event", methods=['POST'])
def color_sensor_event():
    """
    """
    # TODO complete the implementation and documentation
    message = request.get_json()

    print(f"{message=}")

    return jsonify({"status": "success"}), 200
