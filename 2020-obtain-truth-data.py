# Author: Shreya Jain
# IMPORTS
import pandas as pd
import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing

# Methods
def normalize_col(col, doi, norm_val):
    data=(((doi[col]-doi[col].min())/(doi[col].max()-doi[col].min()))*norm_val)
    return data

# CDC Truth Data
new = pd.read_csv('NewCDCData/WHO_NREVSS_Clinical_Labs.csv')
old = pd.read_csv('NewCDCData/WHO_NREVSS_Combined_prior_to_2015_16.csv')
new=new.drop(columns=['REGION TYPE','REGION'])
old=old.drop(columns=['REGION TYPE','REGION'])
new['Total Cases'] = round(new['TOTAL SPECIMENS']*(new['PERCENT POSITIVE'])/100)
old['Total Cases'] = round(old['TOTAL SPECIMENS']*(old['PERCENT POSITIVE'])/100)
new=new.drop(columns=['PERCENT POSITIVE','PERCENT A','PERCENT B'])
# old=old.drop(columns=['PERCENT POSITIVE','PERCENT A','PERCENT B'])
new = new.drop(columns=['TOTAL A','TOTAL B','TOTAL SPECIMENS'])
old = old.drop(columns=['TOTAL SPECIMENS','PERCENT POSITIVE','A (2009 H1N1)','A (H1)','A (H3)','A (Subtyping not Performed)','A (Unable to Subtype)','B','H3N2v'])
data=pd.concat([old,new])
oi = 0
for i in range(len(data)):
    data['weeks']=i
    oi = oi +1
data = data.reset_index()
data = data.reset_index()
data = data.drop(columns=["level_0",'index'])
data=data[14:]
data =data.reset_index()
data.to_csv("truth_data_2020.csv")