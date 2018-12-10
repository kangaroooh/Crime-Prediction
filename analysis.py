#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 20:33:21 2018

@author: r
"""

import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy import stats    #%%
df = pd.read_excel("final.xlsx")
#%%
df.columns = [
    'Hotel Name', 'Hotel Address', 'Effective Star Rating', 'ratio_negreviews',
    'Latitude_x', 'Longitude_x', 'Latitude_y', 'Longitude_y', 'location',
    'avg_crime_n', 'distance'
]
df['distance'] = df['distance'].fillna(df['distance'].mean())
df['Effective Star Rating'] = df['Effective Star Rating'].fillna(
    df['Effective Star Rating'].mean())

#%%
X = df[['Effective Star Rating', 'ratio_negreviews', 'distance']]
y = df[['avg_crime_n']]

X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())
