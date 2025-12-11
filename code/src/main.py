from flask import Flask, request, Request, jsonify

# Import blueprints
from blueprints import robot_bp

app = Flask(__name__)

app.register_blueprint(robot_bp.bp)


@app.route('/')
def index():
    return "Welcome to the main page!"


if __name__ == '__main__':
    # print(f"{app.url_map=}")

    app.run(host='127.0.0.10', port=8080, debug=True)
