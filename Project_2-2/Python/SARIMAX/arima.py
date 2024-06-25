from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import statsmodels.tsa.ar_model
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from keras.models import load_model

import os
import pickle


#loading arima model
model_path = '/Users/jesselemeer/Documents/GitHub/Project2-2/Project_2-2/Python/SARIMAX/models/'



#forecast dataset
forecast_df = pd.read_csv('/Users/jesselemeer/Documents/GitHub/Project2-2/Project_2-2/NL_data/forecast_set/forecast.csv') # forecast purposes, let's see

ams_df_forecast = forecast_df[(forecast_df['latitude'] == 52.25) & (forecast_df['longitude'] == 5.)]
middelburg_df_forecast = forecast_df[(forecast_df['latitude'] == 51.50) & (forecast_df['longitude'] == 3.5)]
hertogenbosch_df_forecast = forecast_df[(forecast_df['latitude'] == 51.75) & (forecast_df['longitude'] == 5.5)]
maastricht_df_forecast = forecast_df[(forecast_df['latitude'] == 51.) & (forecast_df['longitude'] == 5.75)]
utrecht_df_forecast = forecast_df[(forecast_df['latitude'] == 52.) & (forecast_df['longitude'] == 5.)]
hague_df_forecast = forecast_df[(forecast_df['latitude'] == 52.) & (forecast_df['longitude'] == 4.25)]
arnhem_df_forecast = forecast_df[(forecast_df['latitude'] == 52.) & (forecast_df['longitude'] == 6.)]
lelystad_df_forecast = forecast_df[(forecast_df['latitude'] == 52.5) & (forecast_df['longitude'] == 5.5)]
zwolle_df_forecast = forecast_df[(forecast_df['latitude'] == 52.5) & (forecast_df['longitude'] == 6.)]
leeuwarden_df_forecast = forecast_df[(forecast_df['latitude'] == 53.25) & (forecast_df['longitude'] == 5.75)]
assen_df_forecast = forecast_df[(forecast_df['latitude'] == 53.) & (forecast_df['longitude'] == 6.5)]
groningen_df_forecast = forecast_df[(forecast_df['latitude'] == 53.25) & (forecast_df['longitude'] == 6.5)]

ams_df_forecast = ams_df_forecast.iloc[:73]
middelburg_df_forecast = middelburg_df_forecast.iloc[:73]
hertogenbosch_df_forecast = hertogenbosch_df_forecast.iloc[:73]
maastricht_df_forecast = maastricht_df_forecast.iloc[:73]
utrecht_df_forecast = utrecht_df_forecast.iloc[:73]
hague_df_forecast = hague_df_forecast.iloc[:73]
arnhem_df_forecast = arnhem_df_forecast.iloc[:73]
lelystad_df_forecast = lelystad_df_forecast.iloc[:73]
zwolle_df_forecast = zwolle_df_forecast.iloc[:73]
leeuwarden_df_forecast = leeuwarden_df_forecast.iloc[:73]
assen_df_forecast = assen_df_forecast.iloc[:73]
groningen_df_forecast = groningen_df_forecast.iloc[:73]

dataframes_forecast = [ams_df_forecast, middelburg_df_forecast, hertogenbosch_df_forecast, maastricht_df_forecast, utrecht_df_forecast, hague_df_forecast, arnhem_df_forecast, lelystad_df_forecast, zwolle_df_forecast, leeuwarden_df_forecast, assen_df_forecast, groningen_df_forecast]

df_names = ['ams', 'middelburg', 'hertogenbosch', 'maastricht', 'utrecht', 'hague', 'arnhem', 
            'lelystad', 'zwolle', 'leeuwarden', 'assen', 'groningen']

forecast_horizon = 72

predictions_dict = {} # store model predictions, according to the same keys as before, 'ams', etc ...
forecast_dict = {} 


    

    # plt.figure(figsize=(12, 6))
    # plt.plot(timeindex, forecasts- 273.15, label='Predicted Temperature', linestyle='--')
    # plt.plot(timeindex, real_test- 273.15, label = 'actual temperature')
    # plt.legend()
    # plt.title(plot_title)

    # # Group x-axis labels (dates)
    # plt.xticks(rotation=45)
    # plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))  # Adjust the number of ticks as needed
    
    #now only amsterdam, soon to be more locations
def predict_temp_sarimax(date, location):
        # Load the model from file
        with open(os.path.join(model_path+location, 'sarimax_model.pkl'), 'rb') as f:
            model = pickle.load(f)


        special = [location]
        
        
        for idx, i in enumerate(special):
        
            real_test = dataframes_forecast[idx]['t2m'][:-1].values

            timeindex = dataframes_forecast[idx]['time'][:-1]

            forecasts = model.forecast(steps=forecast_horizon)
            forecast_dict[i] = forecasts
            
            # Store predictions and actual values in a dictionary
            predictions_dict[i] = pd.Series(forecasts, index=timeindex)
            # print(predictions_dict)
            actual_values = pd.Series(real_test, index=timeindex)

            plot_title = str(f"Weather forecast for {i}")
        #date is in form of "2024-01-01 00:00:00"
        date = date + ' 12:00:00'
        if location in predictions_dict and date in predictions_dict[location].index:
            prediction = predictions_dict[location][date] - 273.15
            actual = actual_values[date] - 273.15
            return prediction, actual
        else:
            return None, None
        
#testing
# pred, true = predict_temp_sarimax("2024-05-05","ams")

# print(type(pred))
# print(type(true))
