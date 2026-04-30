from flask import Flask, jsonify
from server_log import _log

# Import blueprints
from blueprints import robot_bp, robot_1_bp, robot_2_bp

app = Flask(__name__)


app.register_blueprint(robot_bp.bp)
app.register_blueprint(robot_1_bp.bp)
app.register_blueprint(robot_2_bp.bp)


@app.route('/')
def index():
    return "Welcome to the main page!"


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "message": "Server is running"})


if __name__ == '__main__':
    # run the app on http://127.0.0.10:8080/
    app.run(host='127.0.0.10', port=8080, debug=True)
