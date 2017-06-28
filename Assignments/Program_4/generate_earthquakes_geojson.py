import pprint as pp
import os,sys
import json
import collections



#DIRPATH = os.path.dirname(os.path.realpath(__file__))

myFile = '/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/resources/earthquakes-1960-2017.json'
f = open(myFile,"r")

data = f.read()

data = json.loads(data)

all_earthquakes = []

'''
"1960": [
        {
            "geometry": {
                "coordinates": [
                    -76.018,
                    -44.089,
                    20
                ],
                "type": "Point"
            },
            "mag": 6,
            "magType": "mw",
            "place": "off the coast of Aisen, Chile",
            "rms": null,
            "sig": 554,
            "time": -286813682000,
            "types": ",origin,"
        },
'''
geocollection = {}

geocollection['type'] = 'FeatureCollection'


for k,v in data.items():
    for i in v:
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = i
        geometry = gj['properties']['geometry']
        del gj['properties']['geometry']
        gj["geometry"] = {}
        gj["geometry"] = geometry

        all_earthquakes.append(gj)
"""

            "type": "Feature",
            "properties": {
                "icao": "00AK",
                "iata": "",
                "name": "Lowell Field",
                "city": "Anchor Point",
                "country": "US",
                "elevation": 450,
                "tz": "America/Anchorage"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -151.695999146,
                    59.94919968
                ]
            }
"""
#pp.pprint(all_airports)
geocollection['features'] = all_earthquakes
myFile = "/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/Assignments/Program_4/geo_json/earthquakes_geo_json.json"
out = open(myFile,"w+")

out.write(json.dumps(geocollection, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()