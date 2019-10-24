import requests
import numpy as np

import geopy
import IPython

def request_map_at(lat, long, satellite=False,
                   zoom=10, size=(400, 400)):
    base = "https://static-maps.yandex.ru/1.x/?"
  
    params = dict(
        z = zoom,
        size = str(size[0]) + "," + str(size[1]),
        ll = str(long) + "," + str(lat),
        l = "sat" if satellite else "map",
        lang = "en_US"
    )

    return requests.get(base,params=params)

quakes = requests.get("http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
                      params={
                          'starttime': "2000-01-01",
                          "maxlatitude": "58.723",
                          "minlatitude": "50.008",
                          "maxlongitude": "1.67",
                          "minlongitude": "-9.756",
                          "minmagnitude": "1",
                          "endtime": "2018-10-11",
                          "orderby": "time-asc"}
                      )


mags = np.zeros(0)
location = []

for i in range (len(quakes.json()['features'])):
    if quakes.json()['features'][i]['properties']['place'] == 'England, United Kingdom':
        mags = np.append(mags,quakes.json()['features'][i]['properties']['mag'])
        location += [quakes.json()['features'][i]['geometry']['coordinates']]
        
max_earth = np.max(mags)

location_max = []
for j in range (len(mags)):
    if mags[j]==max_earth:
        location_max += [location[j]]

map_response = request_map_at(location_max[0][1], location_max[0][0])
map2_response = request_map_at(location_max[1][1], location_max[1][0])

with open('map_1.png','wb') as target:
    target.write(map_response.content)

with open('map_2.png','wb') as target:
    target.write(map2_response.content)
