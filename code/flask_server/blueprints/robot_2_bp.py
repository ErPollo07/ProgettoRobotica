from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os, requests
from server_log import _log
import util

bp = Blueprint('robot2', __name__, url_prefix='/robot2')

global can_drop_var
can_drop_var = False

server_ips = util.server_ips


@bp.route("/block_dropped", methods=["POST"])
def block_dropped():
    """
    This endpoint has to be called from the robot 2 to signal that he is above the collection point and the robot 1 can take the block from the drop point.
    It makes a post request to the robot 1 server.
    """

    res = requests.post(server_ips["1"] + "/block_dropped")

    return jsonify({"status": "ok", "message": "success"}), 200


@bp.route("/detect_color", methods=["GET"])
def detect_color():
    """
    This endpoint has to be called from the robot 2 when it's above the sensor
    this will call the endpoint robot1/detect_color that has to response with the color.
    When it respond the variable can_drop_var has to be set to True.
    """
    return jsonify({"status": "ok", "message": "success"}), 200


@bp.route("/detect_color", methods=["GET"])
def can_drop():
    """
    This endpoint will be polled by the robot 2.
    Return the can_drop_var value.
    """


    return jsonify({"status": "ok", "message": "success"}), 200
