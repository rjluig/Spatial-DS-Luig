import pprint as pp
import os,sys
import json
import collections



#DIRPATH = os.path.dirname(os.path.realpath(__file__))

myFile = '/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/resources/state_borders.json'
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
for v in data:

    gj = collections.OrderedDict()
    gj['type'] = "Feature"

    # print(v)
    # sys.exit()
    code = v['code']
    gj['properties'] = {}
    gj['properties']['name'] = v['name']
    gj['properties']['code'] = code
    gj["geometry"] = {}
    
    if len(v['borders']) == 1:
        gj["geometry"]["type"] = 'Polygon'
    else:
        gj["geometry"]["type"] = 'Multipolygon'
        
    gj["geometry"]["coordinates"] = v['borders']
    all_countries.append(gj)

#pp.pprint(all_airports)

myFile = "/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/Assignments/Program_4/geo_json/states_geo_json.json"
out = open(myFile,"w+")

out.write(json.dumps(all_countries, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()