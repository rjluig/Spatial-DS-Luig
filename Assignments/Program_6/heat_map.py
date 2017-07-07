"""
Program:
------------
Program 6: Heat Map Implementation

Description:
------------
This program uses the data from attacks around the world to implement a heat map.
The areas with a greater concentration of attacks will be red and the areas of lower 
concentration will be colored blue.

Name: Ryan Luig, Matthew Trebing, Rephael Edwards
Date: July 7, 2017
"""


import pprint as pp
import pygame
import math
from math import radians, cos, sin, asin, sqrt
import sys
import json

EPSILON = sys.float_info.epsilon  # smallest possible difference

def convert_to_rgb(minval, maxval, val, colors):
    """
    Determines what color a point will be shaded.
    (This code was recieved from the instructor.)

    Args: minval: minimum value in the table
        maxval: maximum value in the table
        val: the count from the grid
        colors: a list of the possible colors for shading
    
    Returns: an rgb value

            example (0,0,255)

    Raises: none

    """
    print(val)
    print(maxval)
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    
    f = fi - i

    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

def convert_lon_lat(data, screen_width, screen_height):
    """
    Adjusts the longitude and latitude values to x and y coordinates for plotting
    on a screen.

    Args: data: a list of lat/lon points
        screen_width : the width of the screen that the new points will be plotted on
        screen_height: the height of the screen that the new points will be plotted on
    
    Returns: points: a list of the adjusted points
            screen_width : the width of the screen that the new points will be plotted on
            screen_height: the height of the screen that the new points will be plotted on
            
            example : (3,4), 1024, 512
    Raises: none

    """
    
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
    Converts the longitude value to an x coordinate for screen plotting.

    Args: lon : longitude value

    Returns: the converted x coordinate

    Raises: none

    """
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return a * b

def mercY(lat,zoom = 1):
    """
    Converts the latitude value to a y coordinate for screen plotting.

    Args: lat : latitude value

    Returns: the converted y coordinate

    Raises: none
    """
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    if(-1 * lat == math.pi/2):
        lat = -1.57 #round lat when so b != 0
    b = math.tan(math.pi / 4 + lat / 2) #math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return (a * c)

def adjust_location_coords(point,screen_width,screen_height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    x,y = point
    adjx = (x / 1024 * screen_width)
    adjy = (y / 512 * screen_height) - (screen_height/2)
    adjusted = ((int(adjx),int(adjy)))

    return adjusted


def main():

    screen_width  = 1024
    screen_height = 512
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Terrorism Heatmap')
    bg = pygame.image.load('bg-map.png')
   
    screen.blit(bg, (0,0))
    pygame.display.flip()

    file_name = "attacks.json"
    with open(file_name, 'r') as content_file:
            content = content_file.read()
    data = json.loads(content)

    grid = [[0 for x in range(screen_height)] for y in range(screen_width)] 

    for country_name in data:
        for place in data[country_name]:
            if not place.lower() == 'unknown':
                lon = float(data[country_name][place]['geometry']['coordinates'][0])
                lat = float(data[country_name][place]['geometry']['coordinates'][1])
                count = data[country_name][place]['count']

                x,y = adjust_location_coords((mercX(lon), mercY(lat)),screen_width,screen_height)
                if not x > 1024 or x < 0:
                    
                    if  not y > 512 or y < 0:
                    

                        grid[x][y] += count
                
            else:
                pass
                #print(place.lower())

    #blur stuff
    maxv = 0
    passes = 4
    mult = .2
    
    for i in range(passes):
        for x in range(screen_width):
            for y in range(screen_height):
                
                if grid[x][y] > 0:
                    grid[x][y] += 1
                    if(x > 0):
                        grid[x-1][y] += 1
                        if y > 0:
                            grid[x-1][y-1] += int(grid[x][y]* mult)
                        if y < screen_height -1:
                            grid[x-1][y+1] += int(grid[x][y]* mult)
                    if x < screen_width -1:
                        grid[x+1][y] += int(grid[x][y]* mult)
                        if y < screen_height -1:
                            grid[x+1][y+1] += int(grid[x][y]* mult)
                        if y > 0:    
                            grid[x+1][y-1] += int(grid[x][y]* mult)
                    if y > 0:
                        grid[x][y-1] += int(grid[x][y]* mult)
                    if y < screen_height - 1:
                        grid[x][y+1] += int(grid[x][y]* mult)

    for x in range(screen_width):
        for y in range(screen_height): 
            if grid[x][y] > maxv:
                maxv = grid[x][y]

    #pick color
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
    print(maxv)
    print(grid[x][y])

    for x in range(screen_width):
        for y in range(screen_height):
            if grid[x][y] > 10000:
                color = convert_to_rgb(50+passes, maxv, grid[x][y], colors)
                if not color == (0,0,255):
                    pygame.draw.circle(screen, color, (x,y), 1)
    #pygame 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
                

        
if __name__ == '__main__':
    main()