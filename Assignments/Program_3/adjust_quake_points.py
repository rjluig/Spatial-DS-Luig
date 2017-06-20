import math
import json
import sys
import pprint as pp

def mercX(lon):
    """
    Mercator projection from longitude to X coord
    """
    zoom = 1.0
    lon = math.radians(lon)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = lon + math.pi
    return int(a * b)


def mercY(lat):
    """
    Mercator projection from latitude to Y coord
    """
    zoom = 1.0
    lat = math.radians(lat)
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
        xprime = (x - minx) / deltax         # val (0,1)
        yprime = ((y - miny) / deltay) # val (0,1)
        adjx = int(xprime*width)
        adjy = int(yprime*height)
        adjusted.append((adjx,adjy))
    return adjusted


def convert_quake_to_points():

    allx = []
    ally = []
    points = []

# Open our condensed json file to extract points
    years = [x for x in range(1960,2017)]
    yearlyquakes = []
    for y in years:
        count = 0
        yr = str(y)
        f = open('./Assignments/Program_3/quake-' + yr + '-condensed.json','r')
        data = json.loads(f.read())
        
        
        # Loop through converting lat/lon to x/y and saving extreme values. 
        for quake in data:
            #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            lon = quake['geometry']['coordinates'][0]
            lat = quake['geometry']['coordinates'][1]
            x,y = (mercX(lon),mercY(lat))
            allx.append(x)
            ally.append(y)
            points.append((x,y))
            count += 1
        yearlyquakes.append(count)

    # Create dictionary to send to adjust method
    extremes = {}
    extremes['max_x'] = max(allx)
    extremes['min_x'] = min(allx)
    extremes['max_y'] = max(ally)
    extremes['min_y'] = min(ally)

    # Get adjusted points
    screen_width = 1024
    screen_height = 512
    offset = 0
    yearsPoints= {}
    for i in range(1960,2017):
            j = i - 1960
            adj = adjust_location_coords(extremes,points[offset:offset+yearlyquakes[j]],screen_width,screen_height)
            offset += yearlyquakes[j]
            yr = str(i)
            yearsPoints[yr] = adj
    # Save adjusted points
    f = open('./Assignments/Program_3/quake-adjusted.json','w')
    f.write(json.dumps(yearsPoints, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()


if __name__=='__main__':
    convert_quake_to_points()
    
