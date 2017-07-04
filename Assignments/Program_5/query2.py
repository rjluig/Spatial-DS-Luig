"""
Ryan Luig
Spatial Data Structures
"""

from pymongo import MongoClient
import pygame
import pprint as pp
import math
from math import radians, cos, sin, asin, sqrt
import sys, os


screen_width = 1024
screen_height = 512

class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_cities = self.client.world_data.cities
        self.db_countries = self.client.world_data.countries
        self.db_earthquakes = self.client.world_data.earthquakes
        self.db_states = self.client.world_data.states
        self.db_volcanos = self.client.world_data.volcanos

    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth. Use 6371 for km. Use 3956 for miles
        return c * r

    def find_near_features(self, feature, lon, lat, dist=1000):
        volc_list = []
        quake_list = []
        #print('find lon, lat: ' + str(lon) + ' ' + str(lat) )
        if(feature == 'earthquakes'):
            all_equakes = self.db_earthquakes.find({ 'geometry' :{'$nearSphere' :{'$geometry' :{'coordinates' : [lon, lat] }, '$maxDistance' :1609.344 *dist} } })

            for quake in all_equakes:
                quake_list.append(quake)

            return quake_list

        if(feature == 'volcanos'):
            all_volcanos = self.db_volcanos.find({ 'geometry' :{'$nearSphere' :{'$geometry' :{'coordinates' : [lon, lat] }, '$maxDistance' :1609.344 *dist} } })
            for volc in all_volcanos:
                volc_list.append(volc)
            
            return volc_list
       

def convert_lon_lat(data):
    
    points = []
    allx = []
    ally = []
    for lon, lat, alt in data:
        x,y = (mercX(lon),mercY(lat))
        allx.append(x)
        ally.append(y)
        points.append((x,y))

    # Create dictionary to send to adjust method
    extremes = {}
    extremes['max_x'] = max(allx)
    extremes['min_x'] = min(allx)
    extremes['max_y'] = max(ally)
    extremes['min_y'] = min(ally)

    # Get adjusted points
    width = 1024
    height = 512
    return adjust_location_coords(extremes,points,width,height)

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
    b = math.tan(math.pi / 4 + lat / 2)
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


def adjust_location_coords(extremes,points,width,height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    maxx = float(extremes['max_x']) # The max coords from bounding rectangles
    minx = float(extremes['min_x'])
    maxy = float(extremes['max_y'])
    miny = float(extremes['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = []

    for p in points:
        x,y = p
        adjx = (x / 1024 * screen_width)
        adjy = (y / 512 * screen_height) - (screen_height/2)

        # x,y = p
        # # x = float(x)
        # # y = float(y)
        # # if deltax !=0 and deltay != 0:
        # #     xprime = x / maxx         # val (0,1)
        # #     yprime = y / maxy         # val (0,1)
        # adjx = (int(x))
        # adjy = (int(y))
        
        adjusted.append((int(adjx),int(adjy)))
        # print("unadjusted point:" + str(x)+ ', '+str(y))
        print(str(adjx) + ', ' + str(adjy))
    return adjusted


def get_features(feature, field, value, minmax, lon, lat, max_res, radius):
    mh = mongoHelper() 
    points = []
    unfiltered = mh.find_near_features(feature,lon, lat, radius)
    if len(unfiltered) != 0:
        if type(unfiltered[0]['properties'][field]) is int:
                value = int(value)

        if type(unfiltered[0]['properties'][field]) is float:
            value = float(value)
        filtered = []
        for obj in unfiltered:
            if minmax == 'max': #values greater than
                if obj['properties'][field] <= value:
                    filtered.append(obj)
                
            else: #values less than
                if obj['properties'][field] >= value:
                    filtered.append(obj)

        res = []
        if len(filtered) < max_res:
            max_res = len(filtered)

        for i in range(max_res):
            res.append(filtered.pop()['geometry']['coordinates'])
        
        points = convert_lon_lat(res)
    return points


def main():
    mh = mongoHelper()
    feature = sys.argv[1]
    field   = sys.argv[2]
    value   = sys.argv[3]
    minmax  = sys.argv[4]
    max_res = int(sys.argv[5])
    radius  = float(sys.argv[6])

    lat = 'x'

    if len(sys.argv) == 8:
        lonlat = sys.argv[7]
        pos = list(map(float, lonlat.strip('[]').split(',')))
        lon = pos[0]
        lat = pos[1]

    if feature == 'earthquakes':
        color = (0,0,255)
    if feature == 'volcanos':
        color = (255,0,0)
    else:
        color = (0, 255, 0)

    
    points = []

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Query2.py')
    bg = pygame.image.load('bg-map.png')
    
    screen.blit(bg, (0,0))

    running = True
    while running:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                lon, lat = toLL((x,y))
                print('mouse:'+str(x)+ ' ' + str(y))

        if(lat != 'x'):
            points = get_features(feature, field, value, minmax, lon, lat, max_res, radius)
            screen.blit(bg, (0,0))
            for p in points:
                #print(p)
                pygame.draw.circle(screen, color, p, 1)
            print('mouse lat/lon: ' +str(lon) + ',' + str(lat))
            pygame.display.flip()
            lat = 'x'

    
        
            

if __name__=='__main__':
    main()