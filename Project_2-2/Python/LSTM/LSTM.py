import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt

#nl_df = pd.read_csv('/Users/lpaggen/Documents/DACS COURSES/Project2-2/Project_2-2/test_nl/processed_data.csv')
nl_df = pd.read_csv('test_nl/processed_data.csv')
ams_df = nl_df[(nl_df['latitude'] == 52.25) & (nl_df['longitude'] == 5.)]

ams_df = ams_df.sort_values(by = ['time'])

ams_df = ams_df.set_index('time')

ams_df = ams_df.drop(['latitude', 'longitude', 'surface', 'step', 'number', 'valid_time'], axis = 1)

# this just moves temp to the right of the DF, easier for X / y split
ams_df['temp'] = ams_df['t2m']
ams_df = ams_df.drop(['t2m'], axis = 1)

# this does the train test split
train_split = round(len(ams_df) * 0.8)
ams_df_tra = ams_df.iloc[:train_split, :]
ams_df_tst = ams_df.iloc[train_split:, :]

# scales data, necessary for LSTM
scaler = MinMaxScaler(feature_range=(0,1))
ams_df_tst_scaled = scaler.fit_transform(ams_df_tra)
ams_df_tra_scaled = scaler.transform(ams_df_tst)

# found this online, basically gets data in 3d format i think? (3d involves timestep)
def createXY(dataset, n_past):
    dataX = []
    dataY = []
    for i in range(n_past, len(dataset)):
            dataX.append(dataset[i - n_past:i, :-1])
            dataY.append(dataset[i, -1])
    return np.array(dataX),np.array(dataY)

X_train, Y_train = createXY(ams_df_tra_scaled, 30)
X_test, Y_test = createXY(ams_df_tst_scaled, 30)

# now using keras we make the LSTM
model = Sequential()
model.add(LSTM(units = 50, input_shape = (X_train.shape[1], X_train.shape[2]))) # input shape -> (None, timestep, features) -> 3D (?)
model.add(Dense(units = 1))
# use adam (can use other, idk what that even is) / MSE (maybe look at cross-entropy instead)
model.compile(optimizer='adam', loss='mse')
# fit model
history = model.fit(X_train, Y_train, epochs=50, batch_size=32, validation_data=(X_test, Y_test), shuffle=False)
# evaluate model
loss = model.evaluate(X_test, Y_test)
# predictions 
predictions = model.predict(X_test)

plt.figure(figsize = (14, 6))

# plot observed temperature
plt.plot(Y_test, label='Actual')

# plot predicted temperature
plt.plot(predictions, label='Predicted')

plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()
