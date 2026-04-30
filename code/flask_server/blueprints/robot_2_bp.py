from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os, requests
from server_log import _log

load_dotenv()

bp = Blueprint('robot_2', __name__, url_prefix='/robot_2')

global trigger_var
trigger_var = False

server_ips: dict[str, str] = {
    "1": str(os.getenv("ROBOT_1_SERVER")),
    "2": str(os.getenv("ROBOT_2_SERVER")),
    "3": str(os.getenv("ROBOT_3_SERVER")),
}


@bp.route("block_dropped", methods=["POST"])
def block_dropped():
    """
    This endpoint has to be called from the robot 2 to signal that he is above the collection point and the robot 1 can take the block from the drop point.
    It makes a post request to the robot 1 server.
    """

    requests.post(server_ips["1"] + "/trigger")
    return jsonify({"status": "ok", "message": "success"}), 200


@bp.route('/trigger', methods=["POST"])
def trigger():
    """
    Set a variable called trigger_var True when called.
    """
    global trigger_var
    _log(f"[trigger] {trigger_var=}")
    trigger_var = True
    return jsonify({"status": "ok", "message": "success"})


@bp.route('/is_triggered', methods=["GET"])
def is_triggered():
    """
    This function return true if the trigger variable is set to true and than make the variable False else return false and do nothing.
    """

    global trigger_var

    _log(f"[is_trigger] {trigger_var=}")

    if trigger_var:
        trigger_var = False
        return jsonify({"status": "ok", "message": True})
    return jsonify({"status": "ok", "message": False})
