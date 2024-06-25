import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/lixiang/Documents/GitHub/Project2-2/Project_2-2/NL_data/ams.csv')
data.head()

def forecast_temperature(data, window_size, prediction_horizon):
   
    # Convert 'time' to datetime
    data['time'] = pd.to_datetime(data['time'])

    # Create lagged features
    for i in range(1, window_size + 1):
        data[f't2m_last_{i}'] = data['t2m'].shift(i)

    # Create the target variable by shifting
    data['t2m_future'] = data['t2m'].shift(-prediction_horizon)

    # Drop rows with NaN values which are the result of shifting
    data = data.dropna()

    # Re-establish 'time' as the DataFrame's index
    data.set_index('time', inplace=True)

    # Splitting data into features and target
    X = data[[f't2m_last_{i}' for i in range(1, window_size + 1)]]
    y = data['t2m_future']
    
    return X, y

X, y = forecast_temperature(data, window_size=72, prediction_horizon=0)
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

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

plt.figure(figsize=(12, 6))
plt.plot(y_test.index, y_test - 273.15, color='blue', label='Actual Values', linewidth=2, linestyle='dotted')
plt.plot(y_test.index, y_pred - 273.15, color='red', label='Predicted Values', linewidth=2, linestyle='--')
plt.title('Comparison of Actual and Predicted Value instantly')
plt.xlabel('Time')
plt.ylabel('Temperature)')
plt.legend()
plt.show()

X, y = forecast_temperature(data, window_size=72, prediction_horizon=24)
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

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

# Plot the actual vs. predicted values
plt.figure(figsize=(12, 6))
plt.plot(y_test.index, y_test - 273.15, color='blue', label='Actual Values', linewidth=2, linestyle='dotted')
plt.plot(y_test.index, y_pred - 273.15, color='red', label='Predicted Values', linewidth=2, linestyle='--')
plt.title('Comparison of Actual and Predicted Values of 24 hours ahead')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.legend()
plt.show()

for i in range(0, 73):
    X, y = forecast_temperature(data, window_size=72, prediction_horizon=i)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    # Initialize and train the model
    reg = RandomForestRegressor()
    reg.fit(X_train, y_train)

    # Make predictions
    y_pred = reg.predict(X_test)

    # Evaluation
    mse = mean_squared_error(y_test, y_pred)

    print(f'Mean Squared Error (MSE) {i} hours ahead:', mse)


