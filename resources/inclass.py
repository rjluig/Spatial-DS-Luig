import pprint as pp
import json
import collections
import os, sys

f = open('/home/ryan/Documents/Programming/GitRepos/Spatial-DS-Luig/resources/airports_geo_json_test.geojson', 'r')

data = f.read()

json.load(data)