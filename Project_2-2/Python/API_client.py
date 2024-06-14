import atexit
import os
from flask import Flask, request, jsonify
#from dummy_model import predict_temp

from SARIMAX.arima import predict_temp

app = Flask(__name__)

def shutdown_server(): # A method behind the shutdown endpoint
    print("Shutting down server...")
    os._exit(0)  # Forcefully stops the process

@app.route('/greet', methods=['GET']) # Just a test endpoint to be able to easily check if the API is up
def greet():
    return jsonify({"message": "Hello from Python!"})

@app.route('/predict_temp', methods=['GET'])
def predict_temperature():  # Changed function name here
    # Retrieve parameters from the query string
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    date = request.args.get('date')
    # Check if the parameters are not null
    if not all([latitude, longitude, date]):
        return jsonify({"error": "Missing parameters! Please provide latitude, longitude, and date."}), 400

    #Predict temperature
    #longitude latitude
    #temperature = predict_temp(latitude=float(latitude), longitude=float(longitude), date=date)
    
    #location like: 'ams', 'middelburg', 'hertogenbosch', 'maastricht', 'utrecht', 'hague', 'arnhem', 'lelystad', 'zwolle', 'leeuwarden', 'assen', 'groningen'
    temperature_pred, temperature_actual = predict_temp(date=date, location='ams')
    return jsonify({"prediction": temperature_pred, "actual": temperature_actual})

@app.route('/shutdown', methods=['POST']) # Used to shut down the server so the port is not busy
def shutdown():
    shutdown_server() 
    return 'Server will shut down shortly...' # That won't happen as it will be forced to stop

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5100, debug=True)