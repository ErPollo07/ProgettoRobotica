from flask import Flask, jsonify

# Import blueprints
from blueprints import robot_bp

app = Flask(__name__)

app.register_blueprint(robot_bp.bp)


global trigger_var
trigger_var = False


@app.route('/')
def index():
    return "Welcome to the main page!"


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "message": "Server is running"})


@app.route('/trigger', methods=["GET"])
def trigger():
    """
    Set a variable called trigger_var True when called.
    """
    global trigger_var
    print(f"[trigger] {trigger_var=}")
    trigger_var = True
    return jsonify({"status": "ok", "message": "success"})


@app.route('/is_triggered', methods=["GET"])
def is_triggered():
    """
    This function return true if the trigger variable is set to true and than make the variable False else return false and do nothing.
    """

    global trigger_var

    print(f"[is_trigger] {trigger_var=}")

    if trigger_var:
        trigger_var = False
        return jsonify({"status": "ok", "message": True})
    return jsonify({"status": "ok", "message": False})

if __name__ == '__main__':
    # run the app on http://127.0.0.10:8080/
    app.run(host='127.0.0.10', port=8080, debug=True)
