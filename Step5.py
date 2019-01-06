import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from sklearn import cluster as skcluster
#%%
import random
random.seed(1234)

# Read data
abb_link = 'NewFinal.xlsx'
zc_link = 'England.json'

lst = pd.read_excel(abb_link)
zc = gpd.read_file(zc_link)

# Choose features
zbd = zc.join(lst[['avg_crime_n', 'distance', 'EEF','Ratio']])
#%%
# Replace Nan by mean
zbd['avg_crime_n'] = zbd['avg_crime_n'].fillna(zbd['avg_crime_n'].mean())
zbd['distance'] = zbd['distance'].fillna(zbd['distance'].mean())
zbd['EEF'] = zbd['EEF'].fillna(zbd['EEF'].mean())
zbd['Ratio'] = zbd['Ratio'].fillna(zbd['Ratio'].mean())
# Min-Max Normalization
zbd['avg_crime_n_norm'] = (zbd['avg_crime_n'] - zbd['avg_crime_n'].min()) / (zbd['avg_crime_n'].max() - zbd['avg_crime_n'].min())
zbd['distance_norm'] = (zbd['distance'] - zbd['distance'].min()) / (zbd['distance'].max() - zbd['distance'].min())
zbd['EEF_norm'] = (zbd['EEF'] - zbd['EEF'].min()) / (zbd['EEF'].max() - zbd['EEF'].min())
zbd['Ratio_norm'] = (zbd['Ratio'] - zbd['Ratio'].min()) / (zbd['Ratio'].max() - zbd['Ratio'].min())
#%%
#elbow plot to select a suitable number of cluster
import numpy as np
from scipy import cluster

X =  [zbd['avg_crime_n_norm'],zbd['distance_norm'],zbd['EEF_norm'], zbd['Ratio_norm']]

X1 = np.array(X)
initial = [cluster.vq.kmeans(X1,i) for i in range(1,4)]
plt.xlabel('decreasing time (s)')
plt.plot([var for (cent,var) in initial])
#%%
# KMeans cluster
km5 = skcluster.KMeans(n_clusters=4)
km5cls = km5.fit(zbd[['avg_crime_n_norm', 'distance_norm', 'EEF_norm','Ratio_norm']].values)
#%%
# Visualize hotels
f, ax = plt.subplots(1, figsize=(15, 15))

zbd.assign(cl=km5cls.labels_)\
   .plot(column='cl', categorical=True, legend=True, \
         linewidth=0.1, edgecolor='white', ax=ax, cmap='tab20')
ax.set_axis_off()
plt.show()
#%%
zbd.to_csv("featuresmap.csv")