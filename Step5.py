import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from sklearn import cluster

# Read data
abb_link = './data/NewFinal.xlsx'
zc_link = './data/England.json'

lst = pd.read_excel(abb_link)
zc = gpd.read_file(zc_link)

# Choose features
zbd = zc.join(lst[['avg_crime_n', 'distance', 'EEF','Ratio']])

# KMeans cluster
km5 = cluster.KMeans(n_clusters=6)
zbd.dropna(subset=['avg_crime_n', 'distance', 'EEF','Ratio'], inplace=True)

# Min-Max Normalization
zbd['avg_crime_n'] = (zbd['avg_crime_n'] - zbd['avg_crime_n'].min()) / (zbd['avg_crime_n'].max() - zbd['avg_crime_n'].min())
zbd['distance'] = (zbd['distance'] - zbd['distance'].min()) / (zbd['distance'].max() - zbd['distance'].min())
zbd['EEF'] = (zbd['EEF'] - zbd['EEF'].min()) / (zbd['EEF'].max() - zbd['EEF'].min())
zbd['Ratio'] = (zbd['Ratio'] - zbd['Ratio'].min()) / (zbd['Ratio'].max() - zbd['Ratio'].min())

km5cls = km5.fit(zbd[['avg_crime_n', 'distance', 'EEF','Ratio']].values)

# Visualize hotels
f, ax = plt.subplots(1, figsize=(9, 9))

zbd.assign(cl=km5cls.labels_)\
   .plot(column='cl', categorical=True, legend=True, \
         linewidth=0.1, edgecolor='white', ax=ax)

ax.set_axis_off()
plt.show()