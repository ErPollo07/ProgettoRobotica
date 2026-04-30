from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os, requests
from server_log import _log

bp = Blueprint('robot', __name__, url_prefix='/robot')

load_dotenv()

access_token_dict: dict[str, str] = {
    "1": str(os.getenv("ACCESS_TOKEN_1")),
    "2": str(os.getenv("ACCESS_TOKEN_2")),
    "3": str(os.getenv("ACCESS_TOKEN_3")),
}

server_ips: dict[str, str] = {
    "1": str(os.getenv("ROBOT_1_SERVER")),
    "2": str(os.getenv("ROBOT_2_SERVER")),
    "3": str(os.getenv("ROBOT_3_SERVER")),
}

def retriveTelemetryLink(robotId: str):
    baseLink = str(os.getenv("TELEMETRY_LINK"))
    accessTok: str = str(access_token_dict.get(str(robotId)))
    link = baseLink + accessTok + "/telemetry"
    _log(f"[retriveTelemetryLink] {link=}")
    return link



@bp.route("/test", methods=['POST'])
def api_test():
    message = request.get_json()
    _log(f"[api_test] {message=}")

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

    request_json = request.get_json()
    _log(f"[movement_executed] {request_json=}")

    try:
        message = [
            {
                "ts": float(request_json["ts"]),
                "values": {
                    "time": request_json["time"]
                }
            }
        ]

        _log(f"[movement_executed] {message=}")

        response = requests.post(retriveTelemetryLink(request_json["robot_id"]), json=message)
        _log(f"[movement_executed] {response.text=}")
        _log(f"[movement_executed] {response.status_code=}")

        return jsonify({"status": "ok"}), 200
    except KeyError:
        m = "Bad json format\nAccepted format: {'ts': <timestamp>,'robot_id': <robot_identifier>, 'time': <timeOfExecution>}"
        return jsonify({"status": "error", "message": m})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@bp.route("/infrared_sensor_event", methods=['POST'])
def infrared_sensor_event():
    """
    Handle infrared sensor event notifications from the robot.

    The payload:
    {
        "ts": <timestamp>,
        "robot_id": <robot_identifier>,
        "infrared_sensor_status": <"ok"|"error">
    }
    """
    request_json = request.get_json()
    _log(f"[infrared_sensor_event] {request_json=}")

    try:
        message = [
            {
                "ts": float(request_json["ts"]),
                "values": {
                    "infrared_sensor_status": request_json["status"]
                }
            }
        ]

        _log(f"[infrared_sensor_event] {message=}")

        response = requests.post(retriveTelemetryLink(request_json["robot_id"]), json=message)
        _log(f"[infrared_sensor_event] {response.text=}")
        _log(f"[infrared_sensor_event] {response.status_code=}")

        return jsonify({"status": "success"}), 200
    except KeyError:
        m = "Bad json format\nAccepted format: {'ts': <timestamp>,'robot_id': <robot_identifier>, 'infrared_sensor_status': <'success'|'error'>}"
        return jsonify({"status": "error", "message": m})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@bp.route("/color_sensor_event", methods=['POST'])
def color_sensor_event():
    """
    Handle color sensor event notifications from the robot.

    The payload:
    {
        "ts": <timestamp>,
        "robot_id": <1|2|3>,
        "color": <"red"|"blue"|"green"|"error">
    }
    """
    request_json = request.get_json()
    _log(f"[color_sensor_event] {request_json=}")

    try:
        message = [
            {
                "ts": float(request_json["ts"]),
                "values": {
                    "color": request_json["color"]
                }
            }
        ]

        _log(f"[color_sensor_event] {message=}")

        # Send request
        response = requests.post(retriveTelemetryLink(request_json["robot_id"]), json=message)
        _log(f"[color_sensor_event] {response.text=}")
        _log(f"[color_sensor_event] {response.status_code=}")

        # Send a get request to the trigger endpoint of the robot 2 server
        requests.get(server_ips["2"] + "robot_2/trigger")

        return jsonify({"status": "success"}), 200
    except KeyError:
        m = "Bad json format\nAccepted format: { 'ts': <timestamp>, 'robot_id': <1|2|3>, 'color': <'red'|'blue'|'green'|'error'> }"
        return jsonify({"status": "error", "message": m})
    except Exception as e:
        _log(f"[color_sensor_event] {e=}")
        return jsonify({"status": "error", "message": str(e)})
