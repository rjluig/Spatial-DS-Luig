import pprint as pp
import os,sys
import json
import collections



#DIRPATH = os.path.dirname(os.path.realpath(__file__))

myFile = '/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/resources/world_volcanos.json'
f = open(myFile,"r")

data = f.read()

data = json.loads(data)

all_volcanos = []

'''
      "geometry": {
        "type": "Point",
        "coordinates": [
          -120.966003418,
          42.3642997742
        ]
      }
'''
geocollection = {}

geocollection['type'] = 'FeatureCollection'


for v in data:
    # print(v)
    # sys.exit()
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = v
    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    lat = v['Lat']
    lon = v['Lon']
    if lat == '':
         gj["geometry"]["coordinates"] = []
    else:
        gj["geometry"]["coordinates"] = [lon, lat]
        
    del gj['properties']['Lat']
    del gj['properties']['Lon']
   
   
    all_volcanos.append(gj)

#pp.pprint(all_airports)
geocollection['features'] = all_volcanos
myFile = "/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/Assignments/Program_4/geo_json/volcanos_geo_json.json"
out = open(myFile,"w+")

out.write(json.dumps(geocollection, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()