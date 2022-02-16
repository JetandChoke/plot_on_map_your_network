#!/usr/bin/env/python3.8
import folium
import pandas as pd
from folium.plugins import MarkerCluster


## https://geopy.readthedocs.io/en/stable/#usage-with-pandas
## https://towardsdatascience.com/using-python-to-create-a-world-map-from-a-list-of-country-names-cd7480d03b10


#empty map
csv_file = input("Enter filename to map: ")
#'result.csv'
print(f"Working on the file {csv_file}")
df = pd.read_csv(csv_file)

world_map = folium.Map(tiles="cartodbpositron")

marker_cluster = MarkerCluster().add_to(world_map)

#for each coordinate create cirlemarker of device percent
IB_per_Country = str(df.groupby('Country').sum())
for i in range(len(df)):
    if df.iloc[i]['Report time']== '2021-12-06-11_43am':
        #df.iloc[i]['Hostname']
        lat = df.iloc[i]['Latitude']
        long = df.iloc[i]['Longitude']
        radius = 5
        popup_text = """Country : {}<br>
                    City : {}<br>
                    Hostname: {}<br>
                    Deployed: {}<br>"""
        popup_text = popup_text.format(df.iloc[i]['Country'], df.iloc[i]['City'], df.iloc[i]['Hostname'],  df.iloc[i]['Date Deployed'])
        folium.CircleMarker(location = [lat, long], radius = radius, popup = popup_text, fill=True).add_to(marker_cluster)

    #show the map
    world_map.save("map.html")
