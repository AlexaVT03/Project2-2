import atexit
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def shutdown_server():
    print("Shutting down server...")
    os._exit(0)  # Forcefully stops the process

@app.route('/greet', methods=['GET'])
def greet():
    return jsonify({"message": "Hello from Python!"})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server() 
    return 'Server will shut down shortly...' # That won't happen as it will be forced to stop

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
