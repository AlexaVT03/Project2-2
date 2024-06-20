import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# Load data
data = pd.read_csv('/Users/jakubsuszwedyk/Documents/University/Year_2/Project/Project_VSC_2/Project2-2/Project_2-2/NL_data/ams.csv')

# Convert 'time' to datetime and set as index
data['time'] = pd.to_datetime(data['time'])
data.set_index('time', inplace=True)

# Create 72 lagged features based on past temperature values
window_size = 72
for i in range(1, window_size + 1):
    data[f't2m_lag_{i}'] = data['t2m'].shift(i)

# Dictionary to store MSE for each forecast horizon
mse_results = {}

# Loop over different forecast horizons from 1 hour to 72 hours
for hours_ahead in range(1, 101):
    # Shift the target variable according to the current forecast horizon
    data['target'] = data['t2m'].shift(-hours_ahead)
    
    # Drop rows with NaN values (mostly at the end due to the shift)
    temp_data = data.dropna()

    # Split data into features and target
    X = temp_data[[f't2m_lag_{i}' for i in range(1, window_size + 1)]]
    y = temp_data['target']

    # Define training and validation set sizes
    train_size = int(len(X) * 0.6)
    val_size = int(len(X) * 0.2)
    X_train, X_val = X.iloc[:train_size], X.iloc[train_size:train_size + val_size]
    y_train, y_val = y.iloc[:train_size], y.iloc[train_size:train_size + val_size]

    # Create and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the validation set
    y_val_pred = model.predict(X_val)

    # Calculate the mean squared error on the validation set
    mse = mean_squared_error(y_val, y_val_pred)
    mse_results[hours_ahead] = mse

# Print and plot the results
print("MSE for different forecast horizons:")
for hours_ahead, mse in mse_results.items():
    print(f"{hours_ahead} hours ahead: MSE = {mse}")

# Plotting MSE results with vertical lines every 24 hours
plt.figure(figsize=(12, 6))
plt.plot(list(mse_results.keys()), list(mse_results.values()), marker='o', linestyle='-')
plt.xlabel('Hours Ahead')
plt.ylabel('Mean Squared Error')
plt.title('MSE for Different Forecast Horizons')
for hour in range(24, 73, 24):
    plt.axvline(x=hour, color='red', linestyle='--', label='Every 24 hours' if hour == 24 else "")
plt.legend()
plt.grid(True)
plt.show()
