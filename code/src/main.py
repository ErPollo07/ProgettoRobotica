from flask import Flask, request, Request, jsonify
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the main page!"

@app.route("/api/test", methods=['POST'])
def api_test():
    message = request.get_json()

    print("Received message:", message['data'])

    return "return"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)