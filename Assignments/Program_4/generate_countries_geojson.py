import pprint as pp
import os,sys
import json
import collections



#DIRPATH = os.path.dirname(os.path.realpath(__file__))

myFile = '/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/resources/countries.geo.json'
f = open(myFile,"r")

data = f.read()

data = json.loads(data)

all_countries = []

'''
      "geometry": {
        "type": "Point",
        "coordinates": [
          -120.966003418,
          42.3642997742
        ]
      }
'''

count = 0

for v in data['features']:
    count += 1
    print(count)
    gj = collections.OrderedDict()
    gj['type'] = "Feature"

    id = v['id']
    # print(v['properties'])
    # sys.exit()
    gj['properties'] = {}
    gj['properties']['name'] = v['properties']['name']
    gj['properties']['id'] = id
    gj["geometry"] = {}
    gj["geometry"]["type"] = v['geometry']['type']
    gj["geometry"]["coordinates"] = v['geometry']['coordinates']
    all_countries.append(gj)

#pp.pprint(all_countries)

myFile = "/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/Assignments/Program_4/geo_json/countries_geojson.json"
out = open(myFile,"w+")

out.write(json.dumps(all_countries, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()