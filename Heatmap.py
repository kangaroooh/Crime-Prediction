import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import numpy as np

# Read data
DataPath = './UK_police_data/2017'
Month3Path = './UK_police_data/2017/2017-03-metropolitan-street.csv'
zc_link = './data/London.geojson'
LongitudeList=[]
LatitudeList = []
Count = []
Month3 = pd.read_csv(Month3Path, usecols=[4,5])
Month3.dropna(subset=['Longitude', 'Latitude'], inplace=True)

Month31 = pd.read_csv(Month3Path, usecols=[4])
Month31.dropna(subset=['Longitude'], inplace=True)

# data3 = np.array(Month3)#np.ndarray()
# # data3_list=data3.tolist()#list
# # data3_tuple = tuple(data3_list)
# # print(data3_tuple[0])
# # data3_tuple2=()
# # for i in range(0, len(data3_tuple)):
# #     data3_tuple2[i] = tuple(data3_tuple[i])
# # print(data3_tuple2)
# # data3_set = set(data3_tuple2)
# # print(data3_set)
Month3['Location'] = Month3['Longitude'].astype(str) + '_' + Month3['Latitude'].astype(str)
CountList = Month3['Location'].value_counts()


# print(Month3['Longitude','Latitude'].value_counts())
# print(Month3['Latitude'].value_counts())

# for i in range(0, Month3.shape[0]):
#     if Month3.ix[i, 0] not in LongitudeList and Month3.ix[i, 1] not in LatitudeList:
#         LongitudeList.append(Month3.ix[i, 0])
#         LatitudeList.append(Month3.ix[i, 1])
#     print(i)
# print(len(LongitudeList))

zc = gpd.read_file(zc_link)
f, ax = plt.subplots(1, figsize=(12, 9))

zc.plot(ax=ax)
for i in range (28000,30000):
    x = float(CountList.index[i].split("_", 1)[0])
    y = float(CountList.index[i].split("_", 1)[1])
    Num = int(CountList.ix[i,0])
    if x > -0.5 and y > 51.2 and x < 0.4 and y < 51.7:
        plt.plot(x, y, color='darkblue', marker='o')

for i in range (500,2000):
    x = float(CountList.index[i].split("_", 1)[0])
    y = float(CountList.index[i].split("_", 1)[1])
    Num = int(CountList.ix[i,0])
    if x > -0.5 and y > 51.2 and x < 0.4 and y < 51.7:
        plt.plot(x, y, color='lawngreen', marker='o')

for i in range (80,500):
    x = float(CountList.index[i].split("_", 1)[0])
    y = float(CountList.index[i].split("_", 1)[1])
    Num = int(CountList.ix[i,0])
    if x > -0.5 and y > 51.2 and x < 0.4 and y < 51.7:
        plt.plot(x, y, color='yellow', marker='o')

for i in range (5,80):
    x = float(CountList.index[i].split("_", 1)[0])
    y = float(CountList.index[i].split("_", 1)[1])
    Num = int(CountList.ix[i,0])
    if x > -0.5 and y > 51.2 and x < 0.4 and y < 51.7:
        plt.plot(x, y, color='coral', marker='o')

for i in range(0, 5):
    x = float(CountList.index[i].split("_", 1)[0])
    y = float(CountList.index[i].split("_", 1)[1])
    Num = int(CountList.ix[i, 0])
    if x > -0.5 and y > 51.2 and x < 0.4 and y < 51.7:
        plt.plot(x, y, color='red', marker='o')
ax.set_axis_off()
plt.show()