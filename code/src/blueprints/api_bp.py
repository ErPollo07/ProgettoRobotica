from flask import Blueprint, request, jsonify


bp = Blueprint('api', __name__, url_prefix='/api')

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
            "robot_id": <robot_identifier>,
            "completed": <true/false>,
            "position": {
                "x": <x>,
                "y": <y>,
                "z": <z>
            }
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

    print(f"{message=}")

    return jsonify({"status": "success"}), 200


@bp.route("/infrared_sensor_event", methods=['POST'])
def infrared_sensor_event():
    """
    Handle infrared sensor event notifications from the robot.

    This endpoint receives a POST request containing a JSON payload that


    Returns
    ------
    response : dict
        A JSON response with status and sensor_status
    """
    # TODO complete the implementation and documentation

    return jsonify({"status": "success"}), 200


@bp.route("/infrared_sensor_error", methods=['POST'])
def infrared_sensor_error():
    """
    """
    # TODO complete the implementation and documentation

    return jsonify({"status": "success"}), 200


@bp.route("/color_sensor_event", methods=['POST'])
def color_sensor_event():
    """
    """
    # TODO complete the implementation and documentation

    return jsonify({"status": "success"}), 200
