from SARIMAX.arima import predict_temp

#this file is just to test of the predict temp function of a another python file works 

# Example usage:
date_to_predict = '2024-05-06'  # Example date, use the format that matches your data
location = 'ams'
prediction, actual = predict_temp(date_to_predict, location)
print(f"Prediction for {date_to_predict} in {location}: {prediction} °C")
print(f"Actual value for {date_to_predict} in {location}: {actual} °C")