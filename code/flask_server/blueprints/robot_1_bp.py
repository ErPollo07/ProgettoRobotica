from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os, requests
from server_log import _log

bp = Blueprint('robot_1', __name__, url_prefix='/robot_1')


global trigger_var
trigger_var = False


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
