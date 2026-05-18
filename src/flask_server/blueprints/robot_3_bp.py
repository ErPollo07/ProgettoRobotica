from flask import Blueprint, request, jsonify
import requests
from src.shared.server_log import _log
import src.shared.util as util

from src.camera.camera import get_color

bp = Blueprint('robot3', __name__, url_prefix='/robot3')


@bp.route("/detect_color", methods=["GET"])
def detect_color():
    try:
        _log("[detect_color] Called camera.get_color()")

        color = get_color()

        _log(f"[detect_color] {color=}")

        if color == None:
            return jsonify({"status": "ok", "message": "none"}), 200

        return jsonify({"status": "ok", "message": color}), 200
    except Exception as e:
        _log(f"[detect_color] Error: {e}")
        return jsonify({"status": "error", "message": "Some things is not working"}), 500

