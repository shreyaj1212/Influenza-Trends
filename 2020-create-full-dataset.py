# Author: Shreya Jain

# imports
import pandas as pd
import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing
import matplotlib

# Methods
def normalize_col(col, doi, norm_val):
    data=(((doi[col]-doi[col].min())/(doi[col].max()-doi[col].min()))*norm_val)
    return data

stdata = pd.read_csv("searchterm_data_2020.csv")
truthdata = pd.read_csv("truth_data_2020.csv")
x=stdata.columns[0]
stdata=stdata.drop(columns=x)
# The 11th week of 2005 corresponds with index 62
# meaning I don't need data values before index 62
# as the Google Trends Data I'm using starts 
# from the 11th week of 2005
truthdata = truthdata[62:]
truthdata = truthdata.drop(columns=x)
truthdata=truthdata.reset_index()
truthdata = truthdata.drop(columns='index')
data = pd.concat([stdata, truthdata],axis=1)
new = pd.read_csv('recentfludat/WHO_NREVSS_Clinical_Labs.csv')
new=new.drop(columns=['REGION TYPE','REGION'])
truthdata=truthdata.drop(columns='weeks')
new = new.drop(columns=new.columns[5:])
new['Total Cases']=new['TOTAL A']+new['TOTAL B']
new=new.drop(columns=new.columns[2:4])
new = new[11:]
truthdata=truthdata[:770]
new=new.drop(columns='TOTAL B')
truthdata=pd.concat([truthdata,new])
truthdata=truthdata.reset_index()
truthdata=truthdata.drop(columns='index')
data = pd.concat([stdata, truthdata],axis=1)
data = data.drop(780) # drop because it includes nans
data.to_csv('fulldataset2020.csv')
