#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime as dt
import random as rd
import os

default_df = pd.read_csv('/home/josh/Documents/dsi/caps/cap1/data/EPL.csv') # original file downloaded from https://www.kaggle.com/irkaal/english-premier-league-results
df = default_df.copy()

'''
The major issue with the data is that the referee names are not standard.  Some instances have first initials and last names, some are last names first.  
EDA was primarily to fix this issue
'''

for name in df.Referee:
    if name[-1] == ' ':
        name.strip()
    name.replace('.','')

refname = [name.split(' ') for name in df.Referee] # split the Referee column into parts of names
df['Reffirst'] = [name[0] for name in refname]
df['Reflast'] = [name[-1] if len(name) > 1 else name[0] for name in refname] # some of the names are in the order (last, first, middle init.).  after removing periods, the initials
                                                                             # are one character long.  So the last names are in the first index

# My solution to this problem is to create a ref name dictionary and reference the last names of refs to a new column in the dataframe.  
RefNames = open('ref_names.txt','r')
ref_list = RefNames.read().split(',') # list of premier league referee names (first last)
ref_dict = {} 
for k in df.Reflast:
    ref_dict[k] = 1
for k in ref_dict.keys():
    for v in ref_list:
        if str(k) in v:
            ref_dict[k] = v

df['ref_name'] = [ref_dict[x] for x in df.Reflast]

epl2000to2020_cleaned = df.copy()

epl2000to2020_cleaned.drop('Referee',axis=1,inplace=True) # Drop the unneccessary columns
epl2000to2020_cleaned.drop('Reflast',axis=1,inplace=True)
epl2000to2020_cleaned.drop('Reffirst',axis=1,inplace=True)

epl2000to2020_cleaned.dropna(axis=0,how='all',inplace=True) # 16 rows of Nan values were created in this process
epl2000to2020_cleaned.drop([7570,7585],axis=0,inplace=True)

epl2000to2020_cleaned.Date = pd.to_datetime(epl2000to2020_cleaned.Date)

epl2000to2020_cleaned.to_csv('epl_cleaned.csv') # export to csv to be imported into the capstone code 




