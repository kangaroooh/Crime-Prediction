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
#%%
fp = "/home/r/Downloads/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"

map_df = gpd.read_file(fp)
map_df = map_df.to_crs(epsg=4326)
map_df['poly_backup'] = map_df['geometry']
map_df.head()

#%%
# allhotel_reviews = pd.read_excel("combine_123_allcols.xlsx")
final_hotel = pd.read_excel("final.xlsx")
#%%
final_hotel = final_hotel.replace('l version="1.0" encoding="UTF-8"?>\n<GeocodeResponse>\n <status>ZERO_RESULTS</status>\n</GeocodeResponse>',np.NaN)
final_hotel = final_hotel.dropna(subset=['Longitude_x', 'Latitude_x'])
#%%
final_hotel.Longitude_x = final_hotel.Longitude_x.astype(float)
final_hotel.Latitude_x = final_hotel.Latitude_x.astype(float)
#%%
final_hotel['Coordinates'] = list(zip(final_hotel.Longitude_x, final_hotel.Latitude_x))
#%%
final_hotel['Coordinates'] = final_hotel['Coordinates'].apply(Point)
#%%
gdf = gpd.GeoDataFrame(final_hotel, geometry='Coordinates')
#%%
hotel_in_london = gpd.sjoin(gdf, map_df)
#%%
hotel_in_london = hotel_in_london.set_geometry('poly_backup')
#%%
hotel_in_london.plot(column='avg_crime_n', cmap='Blues', linewidth=0.8, edgecolor='0.8')
