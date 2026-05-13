from flask import Flask, jsonify, render_template
from server_log import _log

# Import blueprints
#from blueprints import robot_bp, robot_1_bp, robot_2_bp, robot_3_bp


app = Flask(__name__)

#app.register_blueprint(robot_bp.bp)
#app.register_blueprint(robot_1_bp.bp)
#app.register_blueprint(robot_2_bp.bp)
#app.register_blueprint(robot_3_bp.bp)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "message": "Server is running"})


if __name__ == '__main__':
    # Usare i pc 10 e 12
    app.run(host='10.33.77.20', port=8080, debug=True)
