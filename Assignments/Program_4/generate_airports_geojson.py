import pprint as pp
import os,sys
import json
import collections

forGit = True
count = 0

#DIRPATH = os.path.dirname(os.path.realpath(__file__))

myFile = '/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/resources/airports.json'
f = open(myFile,"r")

data = f.read()

data = json.loads(data)

all_airports = []

'''
      "geometry": {
        "type": "Point",
        "coordinates": [
          -120.966003418,
          42.3642997742
        ]
      }
'''


for k,v in data.items():

    if forGit:
      count += 1
      print(count)
      if count == 1000:
        break
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = v
    lat = v['lat']
    lon = v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    gj["geometry"]["coordinates"] = [
          lon,
          lat
        ]
    all_airports.append(gj)

#pp.pprint(all_airports)

myFile = "/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/Assignments/Program_4/geo_json/airports_geo_json.json"
out = open(myFile,"w+")

out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()