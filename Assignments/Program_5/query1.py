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



class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_cities = self.client.world_data.cities
        self.db_countries = self.client.world_data.countries
        self.db_earthquakes = self.client.world_data.earthquakes
        self.db_states = self.client.world_data.states
        self.db_volcanos = self.client.world_data.volcanos


    def find_near_features(self, lat, lon, dist):
        #features includes earthquakes, and volcanos
        #returns tuple of lists one the first with earthquakes the second with volcanos
        quake_list = []
        volcano_list = []
        all_equakes = self.db_earthquakes.find({ 'geometry' : { '$nearSphere' : {'$geometry' : {'coordinates' : [lon, lat] }, '$maxDistance' :1609.344  *dist }} })
        all_volcanos = self.db_volcanos.find({ 'geometry' : {'$nearSphere' : {'$geometry' : { 'coordinates' : [lon, lat] }, '$maxDistance' :1609.344  *dist }} })

        
        for quake in all_equakes:
            quake_list.append(quake)

        for volc in all_volcanos:
            volcano_list.append(volc)

        return (quake_list, volcano_list)


    def get_doc_by_keyword(self,db_name,field,key):

        if db_name == 'airports':
            res = self.db_airports.find_one({field : key})

        return res

    def get_nearest_neighbor(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        min = 999999
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1]
            d = self._haversine(lon,lat,lon2,lat2)
            if d < min:
                min = d

                closest_ap = ap

        return closest_ap
    
    def get_nearest_from_list(self,lst, lon, lat):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })

        min = 999999
        
        for ap in lst:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1]
            d = self._haversine(lon,lat,lon2,lat2)
            if d < min:
                min = d
                closest_ap = ap

        return closest_ap
    

    def get_ap_neighbors(self,lon,lat,r):
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )
        res = []
        for r in air_res:
            res.append(r) 
        return res

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


def flight_path():
    mh = mongoHelper()
    start = sys.argv[1]  #starting ap code
    end   = sys.argv[2]  #ending ap code
    maxd  = int(sys.argv[3])  #max distance between each ap

    start_doc = mh.get_doc_by_keyword("airports","properties.iata", start)
    end_doc   = mh.get_doc_by_keyword("airports","properties.iata", end)
    lon = end_doc["geometry"]["coordinates"][0]
    lat = end_doc["geometry"]["coordinates"][1]

    ap_list = [] #list of airports visited
    ap_list.append(start_doc)

    #loop finding ap close to start and closest to end
    while(start_doc != end_doc):
        close_ap = mh.get_ap_neighbors(start_doc["geometry"]["coordinates"][0],
                                            start_doc["geometry"]["coordinates"][1],
                                            maxd)

        closest_ap = mh.get_nearest_from_list(close_ap, lon, lat)
        if(start_doc["properties"]["name"] == closest_ap["properties"]["name"]):
            close_ap = mh.get_ap_neighbors(start_doc["geometry"]["coordinates"][0],
                                            start_doc["geometry"]["coordinates"][1],
                                            maxd * 1.5)
            closest_ap = mh.get_nearest_from_list(close_ap, lon, lat)                                
            
        ap_list.append(closest_ap)
        start_doc = closest_ap

    return ap_list

def find_features_on_route(route, d):
    
    mh = mongoHelper()
    quake_p = []
    volc_p = []
    volc = []
    earth = []
    for ap in route:
        #find all the features
        lon = ap['geometry']['coordinates'][0]
        lat = ap['geometry']['coordinates'][1]
        qua, vol = mh.find_near_features(lat, lon, d)
        earth = earth + qua
        volc  = volc + vol


    for e in earth:
        lon = e['geometry']['coordinates'][0]
        lat = e['geometry']['coordinates'][1]
        quake_p.append([lon,lat])
        
    for v in volc:
        lon = v['geometry']['coordinates'][0]
        lat = v['geometry']['coordinates'][1]
        volc_p.append([lon, lat])
        
    return (quake_p, volc_p)

def convert_lat_lon(data):
    
    points = []
    allx = []
    ally = []
    for lon, lat in data:
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

def mercX(lon):
    """
    Mercator projection from longitude to X coord
    """
    zoom = 1.0
    lon = radians(lon)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = lon + math.pi
    return int(a * b)


def mercY(lat):
    """
    Mercator projection from latitude to Y coord
    """
    zoom = 1.0
    lat = radians(lat)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return int(a * c)

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
        x = float(x)
        y = float(y)
        if deltax !=0 and deltay != 0:
            xprime = x/maxx         # val (0,1)
            yprime = y / maxy         # val (0,1)
            adjx = int(xprime*width)
            adjy = int(yprime*height) - 290
            adjusted.append((adjx,adjy))
    return adjusted




def main():
    #sys.argv is a list of arguments [0] is file name 
    mh = mongoHelper()
    start = sys.argv[1]  #starting ap code
    end   = sys.argv[2]  #ending ap code
    maxd  = int(sys.argv[3])  #max distance between each ap
    ap_p = []
    flight_plan = flight_path()

    quake, volc = find_features_on_route(flight_plan, 500) 

    for x in flight_plan:
        lon =x['geometry']['coordinates'][0]
        lat = x['geometry']['coordinates'][1]
        ap_p.append([lon, lat])


    route = convert_lat_lon(ap_p)
    quake = convert_lat_lon(quake)
    volc  = convert_lat_lon(volc)
    
    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query1.py')
    bg = pygame.image.load('bg-map.png')
    
    screen.blit(bg, (0,0))
    for p in quake:
        pygame.draw.circle(screen, (0,0,255), p, 1,0)

    for p in volc:
        pygame.draw.circle(screen, (255,0,0), p, 1, 0)   
    pygame.draw.lines(screen, (255,140,0), False, route, 2)


    pygame.display.flip()
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
                
                
                #clean_area(screen,(0,0),width,height,(255,255,255))
        pygame.display.flip()
            




if __name__=='__main__':
    main()