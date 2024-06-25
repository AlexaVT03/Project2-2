import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

train_data = pd.read_csv('/Users/lixiang/Documents/GitHub/Project2-2/Project_2-2/NL_data/ams.csv')
test_data = pd.read_csv('/Users/lixiang/Desktop/forecast.csv')

ams_df = test_data[(test_data['latitude'] == 52.25) & (test_data['longitude'] == 5.0)]
ams_df = ams_df.drop(['Unnamed: 0', 'latitude', 'step', 'number', 'valid_time','longitude', 'surface'], axis=1)
test_data = ams_df

# Convert 'time' to datetime
train_data['time'] = pd.to_datetime(train_data['time'])
test_data['time'] = pd.to_datetime(test_data['time'])

dummy_train_data = train_data.tail(1)
dummy_train_data = dummy_train_data.loc[dummy_train_data.index.repeat(10)]
dummy_train_data['time'] = dummy_train_data['time'] + pd.to_timedelta(dummy_train_data.groupby("time").cumcount(),unit='h')
dummy_train_data = dummy_train_data[1:]

import datetime
full_data = pd.concat([train_data, dummy_train_data, test_data])

aug_test_data = full_data[full_data['time'] >= pd.to_datetime(datetime.date(2024, 4, 29))]
aug_test_data.shape

# Create features for training data
window_size = 71
for i in range(1, window_size + 1):
    train_data[f't2m_last_{i}'] = train_data['t2m'].shift(i)

# Create the target variable by shifting
prediction_horizon = 72
train_data['t2m_future'] = train_data['t2m'].shift(-prediction_horizon)

# Drop rows with NaN values which are the result of shifting
train_data = train_data.dropna()

# Re-establish 'time' as the DataFrame's index for training data
train_data.set_index('time', inplace=True)

# Splitting training data into features and target
X_train = train_data[[f't2m_last_{i}' for i in range(1, window_size + 1)]]
y_train = train_data['t2m_future']
    
# Process augmented test data to create features
for i in range(1, window_size + 1):
    aug_test_data[f't2m_last_{i}'] = aug_test_data['t2m'].shift(i)

# Create the target variable by shifting
aug_test_data['t2m_future'] = aug_test_data['t2m'].shift(-prediction_horizon)    

# Drop rows with NaN values which are the result of shifting in test data
aug_test_data = aug_test_data.dropna()

# Drop extra data
aug_test_data = aug_test_data[aug_test_data['time'] >= pd.to_datetime(datetime.date(2024, 5, 2))]

# Re-establish 'time' as the DataFrame's index for test data
aug_test_data.set_index('time', inplace=True)

# Splitting test data into features and target
X_test = aug_test_data[[f't2m_last_{i}' for i in range(1, window_size + 1)]]
y_test = aug_test_data['t2m_future']

# Initialize and train the model
reg = RandomForestRegressor()
reg.fit(X_train, y_train)

# Make predictions
y_pred = reg.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
train_score = round(reg.score(X_train, y_train) * 100, 2)
valid_score = round(reg.score(X_test, y_test) * 100, 2)

print('Mean Squared Error (MSE):', mse)
print('Train_score:', train_score)
print('Valid_score:', valid_score)

# Set correct time index
y_test_t = y_test.set_axis(y_test.index + pd.Timedelta(days=3))
# Plot the actual vs. predicted values
plt.figure(figsize=(9, 6))

# Plot predicted values
plt.plot(y_test_t.index, y_pred - 273.15, label='Predicted Values')
# Plot actual values
plt.plot(y_test_t.index, y_test_t - 273.15, label='Actual Values')

# Define the zoom range
zoom_start = pd.Timestamp('2024-05-05')
zoom_end = pd.Timestamp('2024-05-07 23:00:00')

# Set the x-axis limit to zoom into the desired timeframe
plt.xlim(zoom_start, zoom_end)
plt.ylim(5, 24)

# Title and labels
plt.title(f'Comparison of Actual and Predicted Values 72 hours ahead - MSE: {mse}')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.legend()

# Show the plot
plt.show()

