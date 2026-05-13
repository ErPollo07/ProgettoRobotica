from flask import Flask, jsonify
from server_log import _log
import camera

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the main page!"


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "message": "Server is running"})


@app.route("/detect_color", methods=["GET"])
def detect_color():
    try:
        _log("[detect_color] Called")
        color = camera.get_color()

        _log(f"[detect_color] {color=}")

        if color == None:
            return jsonify({"status": "ok", "message": "none"}), 200

        return jsonify({"status": "ok", "message": color}), 200
    except Exception as e:
        _log(f"[detect_color] Error: {e}")
        return jsonify({"status": "error", "message": "Some things is not working"}), 500


if __name__ == '__main__':
    app.run(host='10.33.77.100', port=8080, debug=True)
