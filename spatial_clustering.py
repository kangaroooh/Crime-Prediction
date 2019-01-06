#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 20:25:56 2019

@author: r
"""

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from sklearn import cluster as skcluster
import random
random.seed(1234)
#%%
fp = "/home/r/Downloads/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"

map_df = gpd.read_file(fp)
map_df = map_df.to_crs(epsg=4326)
map_df['poly_backup'] = map_df['geometry']
map_df.head()

#%%
def read_final_and_process():
    final_hotel = pd.read_excel("final.xlsx")
    final_hotel = final_hotel.replace('l version="1.0" encoding="UTF-8"?>\n<GeocodeResponse>\n <status>ZERO_RESULTS</status>\n</GeocodeResponse>',np.NaN)
    final_hotel = final_hotel.dropna(subset=['Longitude_x', 'Latitude_x'])
    final_hotel.Longitude_x = final_hotel.Longitude_x.astype(float)
    final_hotel.Latitude_x = final_hotel.Latitude_x.astype(float)
    final_hotel['Coordinates'] = list(zip(final_hotel.Longitude_x, final_hotel.Latitude_x))
    final_hotel['Coordinates'] = final_hotel['Coordinates'].apply(Point)
    return final_hotel

final_hotel = read_final_and_process()

gdf = gpd.GeoDataFrame(final_hotel, geometry='Coordinates')
hotel_in_london = gpd.sjoin(gdf, map_df)
hotel_in_london = hotel_in_london.set_geometry('poly_backup')
#%%hotel_in_london.plot(column='avg_crime_n', cmap='Blues', linewidth=0.8, edgecolor='0.8')
def replace_nan(hotel_in_london):
    hotel_in_london['avg_crime_n'] = hotel_in_london['avg_crime_n'].fillna(hotel_in_london['avg_crime_n'].mean())
    hotel_in_london['distance'] = hotel_in_london['distance'].fillna(hotel_in_london['distance'].mean())
    hotel_in_london['EFF'] = hotel_in_london['EFF'].fillna(hotel_in_london['EFF'].mean())
    hotel_in_london['ratio_negreviews'] = hotel_in_london['ratio_negreviews'].fillna(hotel_in_london['ratio_negreviews'].mean())
    return hotel_in_london
#%%
def normalization_e(hotel_in_london):
    # Min-Max Normalization
    hotel_in_london['avg_crime_n_norm'] = (hotel_in_london['avg_crime_n'] - hotel_in_london['avg_crime_n'].min()) / (hotel_in_london['avg_crime_n'].max() - hotel_in_london['avg_crime_n'].min())
    hotel_in_london['distance_norm'] = (hotel_in_london['distance'] - hotel_in_london['distance'].min()) / (hotel_in_london['distance'].max() - hotel_in_london['distance'].min())
    hotel_in_london['EFF_norm'] = (hotel_in_london['EFF'] - hotel_in_london['EFF'].min()) / (hotel_in_london['EFF'].max() - hotel_in_london['EFF'].min())
    hotel_in_london['ratio_negreviews_norm'] = (hotel_in_london['ratio_negreviews'] - hotel_in_london['ratio_negreviews'].min()) / (hotel_in_london['ratio_negreviews'].max() - hotel_in_london['ratio_negreviews'].min())
    return hotel_in_london
#%%
hotel_in_london.rename(columns={'Effective Star Rating': 'EFF', 'percent_negreviews': 'ratio_negreviews'}, inplace=True)
hotel_in_london = replace_nan(hotel_in_london)
hotel_in_london = normalization_e(hotel_in_london)
#%%
hotel_agg = hotel_in_london.groupby('NAME').mean()
#%%
hotel_agg = hotel_agg.reset_index()
#%%
hotel_agg_poly = hotel_agg.merge(map_df[['NAME', 'poly_backup']])
hotel_agg_poly = gpd.GeoDataFrame(hotel_agg_poly, geometry='poly_backup')
#%%
# KMeans cluster
km5 = skcluster.KMeans(n_clusters=4)
km5cls = km5.fit(hotel_agg_poly[['avg_crime_n_norm', 'distance_norm', 'EFF_norm','ratio_negreviews_norm']].values)
#%%
# Visualize hotels
f, ax = plt.subplots(1, figsize=(15, 15))

hotel_agg_poly.assign(cl=km5cls.labels_)\
   .plot(column='cl', categorical=True, legend=True, \
         linewidth=0.1, edgecolor='white', ax=ax, cmap='tab20')
ax.set_axis_off()
plt.show()
#%%
hotel_agg_poly.to_csv("hotel_cluster.csv", index=False)