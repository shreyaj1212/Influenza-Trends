# Author: Shreya Jain

# Imports
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing
import matplotlib
from sklearn.tree import DecisionTreeRegressor
from keras import Sequential
from keras.layers import LeakyReLU
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
import keras.backend as K
from keras import models
from keras.layers import Conv1D
from keras.layers import Softmax
from keras.layers import Flatten

# Methods
def normalize_col(col, doi, norm_val):
    data=((doi[col]-doi[col].min())/(doi[col].max()-doi[col].min()))*norm_val
    return data

def rmse (y_true, y_pred):
    return sqrt(np.mean((y_pred -y_true)**2))

def krmse (y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred -y_true), axis=-1))

def sqrt (x):
    return x**(1/2.0)

def krmse (y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred -y_true), axis=-1))

# Data
data = pd.read_csv('2020shiftedByThreeWeeks.csv')
data = data.drop(columns=data.columns[0])
# data.head()

y = normalize_col('Total Cases',data,1)
x = pd.DataFrame()
for col in data.columns:
    if col!='index' and col!='YEAR' and col!='WEEK' and col!='index.1':
        x1 = normalize_col(col,data,1)
        x = pd.concat([x,x1],axis=1)
        
xlength = x.shape[0]
x_train = x[:int(2*xlength/3)]
y_train = y[:int(2*xlength/3)]
x_test = x[int(2*xlength/3):]
y_test = y[int(2*xlength/3):]
xlength = x_train.shape[0]
x_val = x_train[:3*int(xlength/10)]
y_val = y_train[:3*int(xlength/10)]

# Neural Network
input_dim = 26
alp = 0.03
model = models.Sequential()
model.add(Dense(100, input_shape=(input_dim,)))
model.add(LeakyReLU(alpha=alp))
model.add(Dense(100))
model.add(LeakyReLU(alpha=alp))
model.add(Dense(100))
model.add(LeakyReLU(alpha=alp))
model.add(Dense(100))
model.add(LeakyReLU(alpha=alp))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='sgd')

results = model.fit(x_train,y_train,epochs=1000)
y_pred= model.predict(x_val)
y_pred= model.predict(x_test)

data_train = data[:int(2*len(data)/3)]
data_test = data[int(2*len(data)/3):]
data_val = data_train[:3*int(len(data)/10)]
newytest = y_test.reset_index().drop(columns='index')
newdatatest = data_test.drop(columns='index').reset_index().drop(columns='index')
bot = newytest['Total Cases'][250]
top =newdatatest['Total Cases'][250]
scale = top/bot
final_test_vals = y_test*scale
final_pred_vals = y_pred*scale
x = final_test_vals
y = final_pred_vals

m, b = np.polyfit(np.array(x), y, 1)
print("y = "+str(m)+"x + "+ str(b))
# matplotlib.rcParams.update({'font.size': 20})
# fig = plt.figure(figsize=(20,10))
# plt.plot(np.arange(len(y_test)),final_test_vals)
# plt.plot(np.arange(len(y_test)),final_pred_vals)
# vrmse = rmse(np.array([final_test_vals]),final_pred_vals.reshape(1,-1))
# den = final_test_vals.mean()
# print("RMSE: "+str(vrmse))
# plt.suptitle('Neural Network Regressor: Plotting predicted and true values')
# plt.xlabel('time')
# plt.ylabel('total number of cases')

# fig = plt.figure(figsize=(20,10))
# plt.scatter(x, y)
# plt.plot([x.min(), x.max()], [x.min(), x.max()], 'k--', lw=4)
# print("got here")
# # plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),'red')
# # print(str(np.polyfit(x, y, 1)[0])+'x + '+ str(np.polyfit(x, y, 1)[1])+' = y')
# plt.xlabel('Measured')
# plt.ylabel('Predicted')
# print("epochs="+str(1000))
# print("RMSE: "+str(vrmse))
# # print(rmse(np.array([y_test]),y_pred.reshape(1,-1)))
# # print("RMSE/maximum value: "+str(100*vrmse/maxz))
# plt.suptitle("Neural Network Predicting Number of Influenza Cases 3 Weeks in Advance")
# plt.show()