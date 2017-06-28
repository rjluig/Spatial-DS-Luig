import pprint as pp
import os,sys
import json
import collections


forGit = True
count = 0
#DIRPATH = os.path.dirname(os.path.realpath(__file__))

myFile = '/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/resources/world_cities_large.json'
f = open(myFile,"r")

data = f.read()

data = json.loads(data)

all_cities = []

'''
  "AD": [
    {
      "city-name": "El Tarter",
      "country-code": "AD",
      "lat": "42.57952",
      "lon": "1.65362",
      "time-zone": "Europe/Andorra"
    },
    {
      "city-name": "Sant Julia de Loria",
      "country-code": "AD",
      "lat": "42.46372",
      "lon": "1.49129",
      "time-zone": "Europe/Andorra"
    }
]
'''

for k,v in data.items():
  for i in v:
    if forGit:
      count += 1
      print(count)
      if count == 1000:
        break 
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = i
    lat = gj['properties']['lat']
    lon = gj['properties']['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']

    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    gj["geometry"]["coordinates"] = [
      float(lon),
      float(lat)
    ]
    all_cities.append(gj)
  if count == 1000:
    break

#pp.pprint(all_airports)
myFile = "/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/Assignments/Program_4/geo_json/city_locations_geo_json.json"
out = open(myFile,"w+")

out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()