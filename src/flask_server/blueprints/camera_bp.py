from flask import Blueprint, request, jsonify
import requests, time
from src.shared.server_log import _log
import src.shared.util as util


bp = Blueprint('camera', __name__, url_prefix='/camera')


@bp.route("/detect_color", methods=["GET"])
def detect_color():
    try:
        _log("[detect_color] Called camera.get_color()")

        res = requests.get("http://127.0.0.1:15001/get_color")

        color = res.json()["color"]

        _log(f"[detect_color] {color=}")

        message = {
            "ts": time.time() * 1000,
            "values": {
                "color_sensor_event": str(color)
            }
        }

        requests.post(util.retriveTelemetryLink("3"), json=message)

        return jsonify({"status": "ok", "message": str(color)}), 200
    except Exception as e:
        _log(f"[camera/detect_color] Error: {e}")
        return jsonify({"status": "error", "message": "Something is not working"}), 500
