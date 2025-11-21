from flask import Flask, request, Request, jsonify


# Import blueprints
from blueprints import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp.bp)


@app.route('/')
def index():
    return "Welcome to the main page!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
