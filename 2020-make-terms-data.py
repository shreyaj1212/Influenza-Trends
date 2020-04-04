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

def merge_data(newname, name):
    data = pd.DataFrame()
    old = pd.read_csv('terms/2020/'+name+'3-7-10to3-7-15.csv')
    new = pd.read_csv('terms/2020/'+name+'3-1-15toprez.csv')
    old = old.drop('Week')
    new = new.drop('Week')
    reset_ind_colname = 'level_0'
    og_colname = 'Category: All categories'
    old = old.rename(columns={og_colname:newname})
    new = new.rename(columns={og_colname:newname})
    old[newname] = old[newname].replace('<1','0')
    new[newname] = new[newname].replace('<1','0')
    new[newname] = pd.to_numeric(new[newname])
    old[newname] = pd.to_numeric(old[newname])
    overlap_index = 260
    new[newname] = new[newname]*old[newname]['2015-03-01']/new[newname]['2015-03-01'] # normalizing it so that the last element in 
    # old[newname] is the same as the first element in new[newname] 
    # because both of these elements refer to the same week
    new = pd.concat([old,new])
    new = new.reset_index()
    new = new.drop(overlap_index)
    new = new.reset_index()
    new = new.drop(columns=[reset_ind_colname])

    #### ITERATION 2 OF CONCATENATION ####
    # concatenating 2005-2010 data
    old = pd.read_csv('terms/2020/'+name+'3-13-05to3-13-10.csv')
    old = old.drop('Week')
    old = old.rename(columns={og_colname:newname})
    old[newname] = old[newname].replace('<1','0')

    old[newname] = pd.to_numeric(old[newname])
    old = old.reset_index()
    new[newname] = new[newname]*old[newname][260]/new[newname][0] # normalizing it so that the last element in 
    new
    # old[newname] is the same as the first element in new[newname] 
    # because both of these elements refer to the same week
    new = pd.concat([old,new])
    new = new.reset_index()
    new = new.drop(columns=[reset_ind_colname])
    new = new.drop(overlap_index)
    new = new.reset_index()
    new = new.drop(columns=[reset_ind_colname])
    new = new.rename(columns={'index':'todrop'})
    data = pd.concat([data,new],axis=1)
    data = data.drop(columns=['todrop'])
    return data

# obtaining data
data = pd.DataFrame()
st_prelim_data = pd.DataFrame()
st_prelim_data=st_prelim_data.append([['influenza st','influenza-st-']])
st_prelim_data=st_prelim_data.append([['Influenza dis','influenza-dis-']])
st_prelim_data=st_prelim_data.append([['Common Cold dis','common-cold-dis-']])
st_prelim_data=st_prelim_data.append([['flu st','flu-st-']])
st_prelim_data=st_prelim_data.append([['flu symptoms st','flu-symptoms-st-']])
st_prelim_data=st_prelim_data.append([['Influenza Vaccine vacc','influenza-vaccine-vacc-']])
st_prelim_data=st_prelim_data.append([['prevent flu st','prevent-flu-st-']])
st_prelim_data=st_prelim_data.append([['Hand sanitizer topic','Hand-sanitizer-topic-']])
st_prelim_data=st_prelim_data.append([['Oseltamivir med','Oseltamivir-med-']])
st_prelim_data=st_prelim_data.append([['Oseltamivir st','Oseltamivir-st-']])
st_prelim_data=st_prelim_data.append([['tamiflu st','tamiflu-st-']])
st_prelim_data=st_prelim_data.append([['pneumonia st','pneumonia-st-']])
st_prelim_data=st_prelim_data.append([['Fever medcond','Fever-medcond-']])
st_prelim_data=st_prelim_data.append([['tylenol st','tylenol-st-']])
st_prelim_data=st_prelim_data.append([['chills st','chills-st-']])
st_prelim_data=st_prelim_data.append([['Nasal Congestion syndrome','Nasal-congestion-syndrome-']])
st_prelim_data=st_prelim_data.append([['Cough topic','Cough-topic-']])
st_prelim_data=st_prelim_data.append([['Cold medicine topic','Cold-medicine-topic-']])
st_prelim_data=st_prelim_data.append([['Antibiotics drugtype','Antibiotics-drugtype-']])
st_prelim_data=st_prelim_data.append([['Antimicrobial resistance topic','Antimicrobial-resistance-topic-']])
st_prelim_data=st_prelim_data.append([['Ibuprofen med','Ibuprofen-med-']])
st_prelim_data=st_prelim_data.append([['immunity st','immunity-st-']])
st_prelim_data=st_prelim_data.append([['Immunity topic','Immunity-topic-']])
st_prelim_data=st_prelim_data.append([['Swine influenza topic','Swine-influenza-topic-']])
st_prelim_data=st_prelim_data.append([['flu medicine st','flu-medicine-st-']])
st_prelim_data.columns=['newname','name']
st_prelim_data=st_prelim_data.reset_index().drop(columns='index')
data = pd.DataFrame()
for i in range(len(st_prelim_data)):
    data=pd.concat([data,merge_data(st_prelim_data['newname'][i],st_prelim_data['name'][i])],axis=1)
data.to_csv("searchterm_data_2020.csv")
