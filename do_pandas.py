import pandas as pd
from geopy.geocoders import Nominatim

## GOOD SOURCES FOR REFERENCE
## https://www.w3resource.com/python-exercises/geopy/python-geopy-nominatim_api-exercise-4.php
## https://github.com/KeithGalli/pandas/blob/master/Pandas%20Data%20Science%20Tutorial.ipynb
## https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#iteration
## https://www.youtube.com/watch?v=eMOA1pPVUc4
## https://www.youtube.com/watch?v=vmEHCJofslg

csv_file = 'result.Report-2020-07-15.csv'

#'test.result.csv'
print(f"Working on the file {csv_file}")
# populate latitude and longitude
geolocator = Nominatim(user_agent="geoapiExercises")
            
df = pd.read_csv(csv_file)
lat = []
long = []
#city_set=set()
city_dict = dict()

# ## Try this:
# for row in df.itertuples():
#     if (df['Latitude'].empty & df['Longitude'].empty):
#         print(f'row already contains coordinates')
#         continue
#     elif df['City'] in city_dict:
#         #retrieve data from dict
#         latitude, longitude = city_dict[row['City']]
#         #print(f'Found city: {row} lat: {latitude}, long: {longitude}')
#     else:
#         addr = geolocator.geocode(row['City'], timeout=10)
#         #print(f'New city: {row}')
#         if addr is None:
#             latitude = 'None'
#             longitude = 'None'
#         else:
#             latitude = addr.latitude
#             longitude = addr.longitude
#             # city_dict[row]['Latitude'] = latitude
#             # city_dict[row]['Latitude'] = latitude
#             city_dict[row['City']] = (latitude, longitude)


for row in df['City']:
    # if (df['Latitude'].isnull().values.any()): # & df['Longitude'].isnull().values.any()):
    #     print(f'row already contains coordinates')
    #     continue
    if row in city_dict:
        #retrieve data from dict
        latitude, longitude = city_dict[row]
        #print(f'Found city: {row} lat: {latitude}, long: {longitude}')
    else:
        addr = geolocator.geocode(row, timeout=10)
        #print(f'New city: {row}')
        if addr is None:
            latitude = 'None'
            longitude = 'None'
        else:
            latitude = addr.latitude
            longitude = addr.longitude
            # city_dict[row]['Latitude'] = latitude
            # city_dict[row]['Latitude'] = latitude
            city_dict[row] = (latitude, longitude)
            
        
    # print(row)
    # print(latitude)
    # print(longitude)
    lat.append(latitude)
    long.append(longitude)
# print(lat)
# print(long)
df['Latitude'] = lat
df['Longitude'] = long

df.to_csv(csv_file, index=False)


#df.head()
#empty map
