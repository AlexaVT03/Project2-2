import atexit
import os
from flask import Flask, request, jsonify
from LSTM import predict_temp

app = Flask(__name__)

def shutdown_server():
    print("Shutting down server...")
    os._exit(0)  # Forcefully stops the process

@app.route('/greet', methods=['GET'])
def greet():
    return jsonify({"message": "Hello from Python!"})


@app.route('/predict_temp', methods=['GET'])
def greet():
    # Retrieve parameters from the query string
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    date = request.args.get('date')

    if not all([latitude, longitude, date]):
        return jsonify({"error": "Missing parameters! Please provide latitude, longitude, and date."}), 400

    # Predict temperature
    temperature = predict_temp(latitude=float(latitude), longitude=float(longitude), date=date)
    return jsonify({"prediction": temperature})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server() 
    return 'Server will shut down shortly...' # That won't happen as it will be forced to stop

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
