"""
Ryan Luig
Spatial Data Structures
"""

from dbscan import *
from pymongo import MongoClient
import pygame
import pprint as pp
import math
from math import radians, cos, sin, asin, sqrt
import sys

class mongoHelper(object):

    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_cities = self.client.world_data.cities
        self.db_countries = self.client.world_data.countries
        self.db_earthquakes = self.client.world_data.earthquakes
        self.db_states = self.client.world_data.states
        self.db_volcanos = self.client.world_data.volcanos
        self.db_meteorites = self.client.world_data.meteorites

    def get_feature(self, feature):
        volc_list = []
        quake_list = []
        meteor_list = []
        #print('find lon, lat: ' + str(lon) + ' ' + str(lat) )
        if(feature == 'earthquakes'):
            all_equakes = self.db_earthquakes.find()

            for quake in all_equakes:
                quake_list.append(quake)

            return quake_list

        if(feature == 'volcanos'):
            all_volcanos = self.db_volcanos.find()
            for volc in all_volcanos:
                volc_list.append(volc)
        
            return volc_list

        if(feature == 'meteorites'):
            all_meteors = self.db_meteorites.find()
            for met in all_meteors:
                meteor_list.append(met)

            return meteor_list

def extract_points(feature_list):
    lonlat_pairs = []
    for obj in feature_list:
        lon = obj['geometry']['coordinates'][0]
        lat = obj['geometry']['coordinates'][1]
        lonlat_pairs.append((lon,lat))

    return lonlat_pairs


def convert_lon_lat(data, screen_width, screen_height):
    
    points = []
    allx = []
    ally = []
    for lon, lat in data:
        x,y = (mercX(lon),mercY(lat))
        allx.append(x)
        ally.append(y)
        points.append((x,y))

    # Get adjusted points
    return adjust_location_coords(points,screen_width, screen_height)
 
def mercX(lon,zoom = 1):
    """
    """
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return a * b

def mercY(lat,zoom = 1):
    """
    """
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    if(-1 * lat == math.pi/2):
        lat = -1.57 #round lat when so b != 0
    b = math.tan(math.pi / 4 + lat / 2) #math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return (a * c)

def mercToLL(point):
    lng,lat = point
    lng = lng / 256.0 * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * lat / 256.0
    lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    return (lng, lat)
    
def toLL(point):
    x,y = point
    return mercToLL((x/4,y/4))


def adjust_location_coords(points,screen_width,screen_height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """

    adjusted = []

    for p in points:
        x,y = p
        adjx = (x / 1024 * screen_width)
        adjy = (y / 512 * screen_height) - (screen_height/2)
        adjusted.append((int(adjx),int(adjy)))

    return adjusted


##HERES WHERE YOU NEED TO CODE


def main():
    feature    = sys.argv[1]
    min_points = int(sys.argv[2])
    eps        = float(sys.argv[3])

    print(feature)
    print(min_points)
    print(eps)

    mh = mongoHelper()
    feature_list = []
    lonlat_pairs = []
    merc_pairs = []
    draw_list = []
    clusters = []

    screen_width = 1024
    screen_height = 512

    feature_list = mh.get_feature(feature)
    lonlat_pairs = extract_points(feature_list)
    merc_pairs = convert_lon_lat(lonlat_pairs, screen_width, screen_height)

    clusters = dbscan(merc_pairs, eps, min_points)
    clusters.pop(-1, None)

    pp.pprint(clusters)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Query3.py')
    bg = pygame.image.load('bg-map.png')
    
    screen.blit(bg, (0,0))
    for p in merc_pairs:
        pygame.draw.circle(screen, (255,0,0), p, 1)

    max_x = -1
    max_y = -1
    min_x = 9999
    min_y = 9999

    sorted_len = []
    if(len(clusters) > 5):
        for key in clusters:
            sorted_len.append((key, len(clusters[key])))

        sorted_len.sort(key=lambda tup : tup[1])

    for i in range(5):
        key, length = sorted_len.pop()
        allx = []
        ally = []
        #find the min/max and draw bounding box
        for x,y in clusters[key]:
            allx.append(x)
            ally.append(y)

        max_x = max(allx)
        max_y = max(ally)
        min_x = min(allx)
        min_y = min(ally)
        del allx
        del ally
        pygame.draw.rect(screen, (0,0,0), (min_x, min_y, max_x-min_x, max_y-min_y), 3)

    running = True
    while running:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

if __name__ == "__main__":
    main()