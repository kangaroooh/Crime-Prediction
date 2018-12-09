#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 20:33:21 2018

@author: r
"""

import pandas as pd
#%%
df = pd.read_excel("final.xlsx")
#%%
df.columns = ['Hotel Name', 'Hotel Address', 'Effective Star Rating',
       'ratio_negreviews', 'Latitude_x', 'Longitude_x', 'Latitude_y',
       'Longitude_y', 'location', 'avg_crime_n', 'distance']
co = df[['Effective Star Rating', 'ratio_negreviews',
                'avg_crime_n', 'distance']].corr()
