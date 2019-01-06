import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from sklearn import cluster

# Read data
abb_link = './data/NewFinal.xlsx'
zc_link = './data/London.geojson'

lst = pd.read_excel(abb_link)
zc = gpd.read_file(zc_link)


# Choose features
# zbd = zc.join(lst[['avg_crime_n', 'distance', 'EEF','Ratio']])


# KMeans cluster
km5 = cluster.KMeans(n_clusters=5)
lst.dropna(subset=['avg_crime_n', 'distance', 'EEF','Ratio'], inplace=True)
df = lst.reset_index(drop=True) # reset index

# Min-Max Normalization
lst['avg_crime_n'] = (lst['avg_crime_n'] - lst['avg_crime_n'].min()) / (lst['avg_crime_n'].max() - lst['avg_crime_n'].min())
lst['distance'] = (lst['distance'] - lst['distance'].min()) / (lst['distance'].max() - lst['distance'].min())
lst['EEF'] = (lst['EEF'] - lst['EEF'].min()) / (lst['EEF'].max() - lst['EEF'].min())
lst['Ratio'] = (lst['Ratio'] - lst['Ratio'].min()) / (lst['Ratio'].max() - lst['Ratio'].min())

km5cls = km5.fit(lst[['avg_crime_n', 'distance', 'EEF','Ratio']].values)

label = km5cls.labels_
# print(label)
# Visualize hotels
f, ax = plt.subplots(1, figsize=(12, 9))

zc.plot(ax=ax)
for i in range(0,df.shape[0]):
    if label[i] == 0:
        x = float(df.ix[i,5])
        y = float(df.ix[i,4])
        if x > -0.6 and y > 50:
            plt.plot(float(x), float(y), 'r.')
    if label[i] == 1:
        x = float(df.ix[i, 5])
        y = float(df.ix[i, 4])
        if x > -0.6 and y > 50:
            plt.plot(float(x), float(y), 'y.')
    if label[i] == 2:
        x = float(df.ix[i, 5])
        y = float(df.ix[i, 4])
        if x > -0.6 and y > 50:
            plt.plot(float(x), float(y), 'w.')
    if label[i] == 3:
        x = float(df.ix[i, 5])
        y = float(df.ix[i, 4])
        if x > -0.6 and y > 50:
            plt.plot(float(x), float(y), 'k.')
    if label[i] == 4:
        x = float(df.ix[i, 5])
        y = float(df.ix[i, 4])
        if x > -0.6 and y > 50:
            plt.plot(float(x), float(y), 'c.')
ax.set_axis_off()
plt.show()