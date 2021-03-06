# -*- coding: utf-8 -*-
"""StockPricePrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w_WJyPsQO-ppDmVjHFbS_ccX-72mQQNK
"""

# Importing Libraries for LSTM

# Commented out IPython magic to ensure Python compatibility.
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.preprocessing import MinMaxScaler

# Importing Training Dataset

dataset_train = pd.read_csv('NFLX.csv')
dataset_train.head()

# Using Open Stock Price Variable to Train Regression Model

training_set = dataset_train.iloc[:, 1:2].values

print(training_set)
print(training_set.shape)

#Scaling Dataset

scaler = MinMaxScaler(feature_range=(0,1))
scaled_training_set = scaler.fit_transform(training_set)

scaled_training_set

# Creating Data Split to X_train and Y_train

X_train = []
y_train = []
for i in range(60, 251):
  X_train.append(scaled_training_set[i-60:i, 0])
  y_train.append(scaled_training_set[i, 0])

X_train = np.array(X_train)
y_train = np.array(y_train)

print(X_train.shape)

print(y_train.shape)

#Reshaping the Data

X_train = np.reshape(X_train,(X_train.shape[0], X_train.shape[1], 1))

X_train.shape

# Visualizing Regression Model 
# Importing More Libraries
# Importing layers to LSTM

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout

#Creating regressors for each library

regressor = Sequential()

regressor.add(LSTM(units = 20, return_sequences= True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 20, return_sequences= True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 20, return_sequences= True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 20, return_sequences= False))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer='adam',loss = 'mean_squared_error', metrics=['accuracy'])

#Fitting the Model

regressor.fit(X_train, y_train, epochs= 60, batch_size= 32, verbose=2)

#Extracting Actual Stock Prices on Date - Year

dataset_test = pd.read_csv('NFLX.csv')
actual_stock_price = dataset_test.iloc[:, 1:2]

print(actual_stock_price)

#Preparing the Input for the Model

dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total)- len(dataset_test)-60:].values

inputs = inputs.reshape(-1,1)
inputs = scaler.transform(inputs)

X_test = []
for i in range(60,300):
  X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

#Predicting Values for July 2017 Stock Prices

predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

plt.plot(actual_stock_price, color = 'red', label = 'Actual Netflix Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Netflix Price')
plt.title('NFLX Stock Price Prediction', weight = 'bold')
plt.text(250, 60, 'Sources found on Yahoo', fontsize = 11, weight = 'bold')
plt.xlabel('Time')
plt.ylabel('Stock Price Prediction')
plt.legend()