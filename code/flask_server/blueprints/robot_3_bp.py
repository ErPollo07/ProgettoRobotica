from flask import Blueprint, request, jsonify
import requests
from server_log import _log
import util

from camera.camera import get_color

bp = Blueprint('robot3', __name__, url_prefix='/robot3')


@bp.route("/detect_color", methods=["GET"])
def detect_color():
    """
    Get color from the camera and respond with the color
    """

    color = get_color()

    # Send the color to thingsboard

    return jsonify({"status": "ok", "message": color}), 200


