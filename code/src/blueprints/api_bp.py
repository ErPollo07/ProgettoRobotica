from flask import Blueprint, request, jsonify


bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/test', methods=['POST'])
def api_test():
    message = request.get_json()

    print("Received message:", message['data'])

    return jsonify({"status": "success", "message": "Message received"}), 200

