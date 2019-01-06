#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 23:13:17 2019

@author: r
"""

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from sklearn import cluster as skcluster
import random
random.seed(6728)
#%%
fp = "/home/r/Downloads/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"

map_df = gpd.read_file(fp)
map_df = map_df.to_crs(epsg=4326)
map_df['poly_backup'] = map_df['geometry']
map_df.head()

crime_fp = "/home/r/Codes/txt-mng/crimedata/AVG_CRIME_LOCAT_MTH38.csv"

crime_df = pd.read_csv(crime_fp)
#%%
crime_df = crime_df.dropna(subset=['Longitude', 'Latitude'])
crime_df.Longitude_x = crime_df.Longitude.astype(float)
crime_df.Latitude_x = crime_df.Latitude.astype(float)
crime_df['Coordinates'] = list(zip(crime_df.Longitude, crime_df.Latitude))
crime_df['Coordinates'] = crime_df['Coordinates'].apply(Point)

gdf = gpd.GeoDataFrame(crime_df, geometry='Coordinates')
crime_in_london = gpd.sjoin(gdf, map_df)
crime_in_london = crime_in_london.set_geometry('poly_backup')
#%%
crime_in_london.plot(column='avg_crime_n', legend=True, \
         linewidth=0.1, edgecolor='white', cmap='tab20')