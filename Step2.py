import pandas as pd
import requests
import openpyxl

# Read the data
DataPath = './Hotel_reviews_NLP/Tripadvisor Review Part3.xlsx'
Locations = pd.read_excel(DataPath, Headname=None, usecols=[2,3])
Data = pd.read_excel(DataPath, Headname=None)
LocList = []
CityList = []

# Save different Addresses of hotels
for i in range(0, Locations.shape[0]):
    if Locations.ix[i, 0] not in LocList:
        LocList.append(Locations.ix[i, 0])
        CityList.append(Locations.ix[i, 1])
Key = ',+CA&key=AIzaSyBin-hGUWXjPnlT8q_ETK17zRYFbLsuw-4'
Geocoding = 'https://maps.googleapis.com/maps/api/geocode/xml?address='
Latitude = []
longitude = []

print(LocList.index(Locations.ix[10000, 0]))

# Get Geocoding list
for i in range(0, len(LocList)):
# for i in range(0, 1):
    url = Geocoding + LocList[i] + ' ' + CityList[i] + Key
    data = requests.get(url).text
    print(i)
    Latitude.append(data[data.find('<lat>')+5:data.find('</lat>')])
    longitude.append(data[data.find('<lng>')+5:data.find('</lng>')])
print(Latitude, longitude)

# Transform all addresses to Geocoding
Data['Latitude'] = None
Data['Longitude'] = None
for i in range(0, Locations.shape[0]):
    index = LocList.index(Locations.ix[i, 0])
    Data.ix[i, 15] = Latitude[index]
    Data.ix[i, 16] = longitude[index]
Data.to_excel('./Hotel_reviews_NLP/Tripadvisor Review Part3-transformed.xlsx')