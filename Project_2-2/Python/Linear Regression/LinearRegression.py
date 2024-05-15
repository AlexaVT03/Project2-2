import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load the data
nl_df = pd.read_csv('/Users/jesselemeer/Documents/GitHub/Project2-2/Project_2-2/NL_data/train_set/processed_data.csv')

# Filter data for Amsterdam
ams_df = nl_df[(nl_df['latitude'] == 52.25) & (nl_df['longitude'] == 5.)]

# Sort values by time and set time as index
ams_df = ams_df.sort_values(by='time').set_index('time')

# Drop unnecessary columns
ams_df = ams_df.drop(['latitude', 'longitude', 'surface', 'step', 'number', 'valid_time'], axis=1)

# this just moves temp to the right of the DF, easier for X / y split
ams_df['temp'] = ams_df['t2m']
ams_df = ams_df.drop(['t2m'], axis = 1)

# Rename 't2m' column to 'temp'
# ams_df.rename(columns={'t2m': 'temp'}, inplace=True)

# Train-test split
train_split = round(len(ams_df) * 0.8)
ams_df_train = ams_df.iloc[:train_split]
ams_df_test = ams_df.iloc[train_split:]

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
ams_df_train_scaled = scaler.fit_transform(ams_df_train)
ams_df_test_scaled = scaler.transform(ams_df_test)  # Use transform for test data

# Define function to create X, y pairs
def createXY(dataset, n_past):
    dataX = []
    dataY = []
    for i in range(n_past, len(dataset)):
        dataX.append(dataset[i - n_past:i, :-1])
        dataY.append(dataset[i, -1])
    return np.array(dataX), np.array(dataY)

# Create X, y pairs for training and testing sets
n_past = 30
X_train, Y_train = createXY(ams_df_train_scaled, n_past)
X_test, Y_test = createXY(ams_df_test_scaled, n_past)


# Reshape the data for linear regression
X_train_linear = X_train.reshape(X_train.shape[0], -1)
X_test_linear = X_test.reshape(X_test.shape[0], -1)
#Y_train_linear = Y_train.reshape(Y_train.shape[0], -1)
#Y_test_linear = Y_test.reshape(Y_test.shape[0], -1)


# Create a linear regression model
linear_model = LinearRegression()

# Train the linear regression model
linear_model.fit(X_train_linear, Y_train)

# Make predictions
predictions_linear = linear_model.predict(X_test_linear)

# Print first few predictions
print("Predictions:", predictions_linear[:20])

# Print trained model coefficients
# print("Model Coefficients:", linear_model.coef_)

# Print scaled test data
print("Scaled Test Data:", X_test_linear[:10])

# Evaluate the model
mse_linear = mean_squared_error(Y_test, predictions_linear)
print("Mean Squared Error (Linear Regression):", mse_linear)

# Plotting the results
plt.figure(figsize=(14, 6))
plt.plot(Y_test, label='Actual')
plt.plot(predictions_linear, label='Predicted')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()
