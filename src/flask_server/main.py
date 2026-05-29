from flask import Flask, jsonify, render_template
from src.shared.server_log import _log
import src.shared.conf as conf

# Import blueprints
from src.flask_server.blueprints import robot_bp, robot_1_bp, robot_2_bp, camera_bp


app = Flask(__name__)

app.register_blueprint(robot_bp.bp)

# Register only the necessary blueprints for the server number specified
match (conf.server_number):
    case "1":
        app.register_blueprint(robot_1_bp.bp)
    case "2":
        app.register_blueprint(robot_2_bp.bp)
    case "3":
        app.register_blueprint(camera_bp.bp)
    case "100":
        app.register_blueprint(robot_1_bp.bp)
        app.register_blueprint(robot_2_bp.bp)
        app.register_blueprint(camera_bp.bp)
    case _:
        raise Exception("Missing or wrong SERVER_NUMBER in .env file")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "message": "Server is running"})


if __name__ == '__main__':
    # Usare i pc 10 e 12
    app.run(host=f'10.33.77.{conf.server_number}', port=int(conf.port), debug=True)
