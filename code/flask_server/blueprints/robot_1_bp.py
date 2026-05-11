from flask import Blueprint, request, jsonify
import os, requests
from server_log import _log

bp = Blueprint('robot1', __name__, url_prefix='/robot1')


global can_collect_var
can_collect_var = False


@bp.route("/can_collect", methods=["GET"])
def can_collect():
    """
    This is the endpoint that the robot 1 poll to ask if it can get the block
    """
    return jsonify({"status": "ok", "message": "success"}), 200


@bp.route("/block_dropped", methods=["GET"])
def block_dropped():
    """
    This is called from the robot 2.
    When called the variable can_collect_var has to be set to True
    """
    return jsonify({"status": "ok", "message": "success"}), 200
