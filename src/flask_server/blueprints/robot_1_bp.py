from flask import Blueprint, request, jsonify
import os, requests
from src.shared.server_log import _log

bp = Blueprint('robot1', __name__, url_prefix='/robot1')


global can_collect_var
can_collect_var: bool = False


@bp.route("/can_collect", methods=["GET"])
def can_collect():
    """
    This is the endpoint that the robot 1 poll to ask if it can get the block
    """

    global can_collect_var

    if can_collect_var:
        can_collect_var = False
        return jsonify({"status": "ok", "message": True}), 200
    else:
        return jsonify({"status": "ok", "message": False}), 200


@bp.route("/block_dropped", methods=["POST"])
def block_dropped():
    """
    This is called from the robot 2.
    When called the variable can_collect_var has to be set to True
    """

    global can_collect_var

    can_collect_var = True

    return jsonify({"status": "ok", "message": "success"}), 200
