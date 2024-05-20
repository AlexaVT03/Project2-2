import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# Load the data
nl_df = pd.read_csv('Project_2-2/NL_data/train_set/processed_data.csv')

# Filter data for Amsterdam
ams_df = nl_df[(nl_df['latitude'] == 52.25) & (nl_df['longitude'] == 5.)]

# Sort values by time and set time as index
ams_df = ams_df.sort_values(by='time').set_index('time')

# Drop unnecessary columns
ams_df = ams_df.drop(['latitude', 'longitude', 'surface', 'step', 'number', 'valid_time'], axis=1)

# this just moves temp to the right of the DF, easier for X / y split
ams_df['temp'] = ams_df['t2m']
ams_df = ams_df.drop(['t2m'], axis = 1)

nl_df.head()

train_split = round(len(ams_df) * 0.8)
train_set = ams_df.iloc[:train_split, :]
valid_set = ams_df.iloc[train_split:, :]
print(train_set.shape)
print(valid_set.shape)

X_train, Y_train = train_set.iloc[:, :-1], train_set['temp']
X_valid, Y_valid = valid_set.iloc[:, :-1], valid_set['temp']

# Initialise and train the model
gbr = GradientBoostingRegressor()
gbr.fit(X_train, Y_train)

# Make predictions using the model
Y_pred = gbr.predict(X_valid)

# Print first few predictions
print("Predictions:", Y_pred[:10])

# Print some test data
print("Data to compare:", X_valid[:10])

# Evaluate the model
mae = mean_absolute_error(Y_valid, Y_pred)
mse = mean_squared_error(Y_valid, Y_pred)
mape = mean_absolute_percentage_error(Y_valid, Y_pred)

print("Mean absolute error:", mae)
print("Mean squared error", mse)
print(f"Mean absolute percentage error: {mape} %")

# Hyperparameter tuning
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 4, 5]
}
grid_search = GridSearchCV(estimator=gbr, param_grid=param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1)
grid_search.fit(X_train, Y_train)

print("Best hyperparameters:", grid_search.best_params_)

# Now let's train a new model with the best hyperparameters
best_gbr = grid_search.best_estimator_
best_gbr.fit(X_train, Y_train)

best_Y_pred = best_gbr.predict(X_valid)

best_mae = mean_absolute_error(Y_valid, best_Y_pred)
best_mse = mean_squared_error(Y_valid, best_Y_pred)
best_mape = mean_absolute_percentage_error(Y_valid, best_Y_pred)

print("Best mean absolute error:", best_mae)
print("Best mean squared error:", best_mse)
print(f"Best mean absolute percentage error: {best_mape} %")

# Plotting the results
plt.figure(figsize=(14, 6))
plt.plot(Y_valid, label='Actual')
plt.plot(best_Y_pred, label='Predicted (Gradient Boosting)')
plt.xlabel('Time')
plt.ylabel('Scaled temperature') #in this case

plt.legend()
plt.show()