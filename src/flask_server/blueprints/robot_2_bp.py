from flask import Blueprint, jsonify
import requests, time
from src.shared.server_log import _log
import src.shared.util as util

bp = Blueprint('robot2', __name__, url_prefix='/robot2')

global can_drop_var
can_drop_var = False

server_ips = util.server_ips
port = util.port


@bp.route("/block_dropped", methods=["POST"])
def block_dropped():
    """
    This endpoint has to be called from the robot 2 to signal that he is above the collection point
    Then this endpoint will make a call to the endpoint /block_dropped of the robot 1 server so the robot 1 can take the block from the drop point.
    """

    requests.post(f"http://{server_ips["1"]}:{port}/robot1/block_dropped")

    return jsonify({"status": "ok", "message": "success"}), 200


@bp.route("/detect_color", methods=["GET"])
def detect_color():
    """
    This endpoint has to be called from the robot 2 when it's above the sensor
    this will call the endpoint camera/detect_color that has to response with the color.
    When it respond the variable can_drop_var has to be set to True.
    """
    global can_drop_var

    color = "none"
    i = 0

    while color == "none" and i < 3:
        color = requests.get(f"http://{server_ips["3"]}:{port}/camera/detect_color")
        i += 1
        time.sleep(1)

    can_drop_var = True

    return jsonify({"status": "ok", "message": "success"}), 200


@bp.route("/can_drop", methods=["GET"])
def can_drop():
    """
    This endpoint will be polled by the robot 2.
    Return the can_drop_var value.
    """
    global can_drop_var

    if can_drop_var == True:
        can_drop_var = False
        return jsonify({"status": "ok", "message": True}), 200

    return jsonify({"status": "ok", "message": False}), 200
