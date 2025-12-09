from flask import Flask, request, Request, jsonify

# Import blueprints
from src.blueprints import robot_bp

app = Flask(__name__)

app.register_blueprint(robot_bp.bp)


@app.route('/')
def index():
    return "Welcome to the main page!"


if __name__ == '__main__':
    app.run(host='127.0.0.5', port=8080, debug=True)
