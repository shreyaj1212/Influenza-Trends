# Author: Shreya Jain

# Imports
import numpy as np
import matplotlib.pyplot as plt

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

# Data
data = pd.read_csv('2020shiftedByThreeWeeks.csv')
data = data.drop(columns=data.columns[0])
np.poly1d(np.polyfit(x, y, 1))(np.unique(x))