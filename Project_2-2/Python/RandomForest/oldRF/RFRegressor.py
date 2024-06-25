import numpy as np
import pandas as pd
from collections import OrderedDict

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance

data = pd.read_csv("./data/processed_data.csv")

data.head()
data_ams = data[(data['latitude'] == 52.25) & (data['longitude'] == 5.0)]
data_ams.shape
data_ams['time'] = pd.to_datetime(data_ams['time'], format='%Y-%m-%d %H:%M:%S')

data_ams['days'] = (pd.Timestamp('20220101') - data_ams['time']).dt.days
data_ams['month'] = data_ams['time'].dt.month
data_ams['hour'] = data_ams['time'].dt.hour

data_ams = data_ams.drop(['time', 'latitude', 'longitude', 'surface', 'step', 'number', 'valid_time', 'month_1', 'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10', 'month_11', 'month_12', 'hour_0', 'hour_6', 'hour_12', 'hour_18'], axis=1)

data_ams.tail(10)
# Prepare dataset

def prepare_data(raw_data, interval):
    X, y = [], []
    for i in range(interval, len(raw_data)):
        X.append(raw_data.iloc[i - interval:i, :])
        y.append(raw_data.iloc[i, 3])
    return np.array(X), np.array(y)

X, y = prepare_data(data_ams, 30)
X.shape, y.shape
y[-10:]
X_train, X_test, y_train, y_test = train_test_split(X.reshape(X.shape[0], -1), y, test_size=0.2, random_state=0)
X_train.shape, y_train.shape
params = {
    "n_estimators": 500,
    "max_depth": 4,
    "min_samples_split": 5,
    "warm_start":True,
    "oob_score":True,
    "random_state": 42,
}
reg = RandomForestRegressor(**params)
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
train_score = round(reg.score(X_train, y_train) * 100, 2)
valid_score = round(reg.score(X_test, y_test) * 100, 2)

print('Mean Squared Error (MSE):', mse)
