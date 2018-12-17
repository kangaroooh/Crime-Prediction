import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from sklearn import cluster

# Read data
abb_link = './data/pnegreviews.xlsx'
zc_link = './data/England.json'

lst = pd.read_excel(abb_link)
zc = gpd.read_file(zc_link)

# Choose features
zbd = zc.join(lst[['nb_negreview', 'nb_allreview']])

# KMeans cluster
km5 = cluster.KMeans(n_clusters=5)
km5cls = km5.fit(zbd[['nb_negreview', 'nb_allreview']].values)

# Visualize hotels
f, ax = plt.subplots(1, figsize=(9, 9))

zbd.assign(cl=km5cls.labels_)\
   .plot(column='cl', categorical=True, legend=True, \
         linewidth=0.1, edgecolor='white', ax=ax)

ax.set_axis_off()
plt.show()