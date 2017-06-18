import pygame
import random
import read_crime_data
from dbscan import *
import sys,os
import pprint as pp


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs) 
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """
    for id in range(len(clusters)-1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs

#=====================================================================================================

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

#====================================================================================================
class Map(object):
    def __init__(self):
        self.xmin = 999999999
        self.xmax = -1

        self.ymin = 999999999
        self.ymax = -1

    def adjust_points(self, pointslst):
        newPoints = []

        for x, y in pointslst:
            if(x != ''):
                newx = int((x - self.xmin) / (self.xmax - self.xmin) * 1000)
                newy = int((1 - (y - self.ymin)/(self.ymax - self.ymin)) * 1000)
                newPoints.append((newx, newy))

        return newPoints

    def extract_points(self, crimelist):
        x = -1
        y = -1
        points = []
        for line in crimelist:
            x = line[19]
            y = line[20] 
            if(x != ''):
                x = int(x)
                y = int(y)
                if self.xmin > x:
                    self.xmin =x
                elif self.xmax < x:
                    self.xmax = x

                if self.ymin > y:
                    self.ymin = y
                elif self.ymax < y:
                    self.ymax = y
                points.append((x,y))

        return points

if __name__ == '__main__':
    DIRPATH = os.path.dirname(os.path.realpath(__file__))

    background_colour = (255,255,255)
    BLACK = (0,0,0)
    BLUE = (0,0,255)
    RED  =(255,0,0)
    GREEN = (0,255,0)
    YELLOW = (255,255,0)
    PURPLE = (128,0,128)

    (width, height) = (1000, 1000)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Simple Line')
    screen.fill(background_colour)

    pygame.display.flip()

    map = Map()

    epsilon = 10
    min_pts = 4.0
    t = 'filtered_'
    c = 'crimes_'
    pngName = '_screen_shot.png'
    extention = '.csv'
    keys = ['bronx', 'brooklyn', 'manhattan', 'queens', 'staten_island']

    colour ={'manhattan':(194,35,38), 'queens':(243,115,56), 'staten_island':(253,182,50), \
        'bronx':(2,120,120), 'brooklyn':(128,22,56) }
    images = []
    boroughs = {}

    for f in keys:
        points = []
        points = read_crime_data.get_crime_data(t+c+f+extention)
        points = map.extract_points(points)
        #print(points)
        boroughs[f] = points

    for key in boroughs:
        boroughs[key] = map.adjust_points(boroughs[key])
        for i in range(len(boroughs[key])):
            
            pygame.draw.circle(screen, colour[key], boroughs[key][i], 1, 0)
        #print(DIRPATH)
    pygame.image.save(screen, DIRPATH + '/' + 'all_buroughs_screen_shot.png' )
    screen.fill(background_colour)

    # mbrs = calculate_mbrs(points, epsilon, min_pts)
    screenshot = pygame.image.load(DIRPATH + '/' + 'all_buroughs_screen_shot.png' )
    screen.blit(screenshot, (0,0))
    running = True  
    while running:

        
        # for mbr in mbrs:
        #     pygame.draw.polygon(screen, black, mbr, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     clean_area(screen,(0,0),width,height,(255,255,255))
            #     points.append(event.pos)
            #     mbrs = calculate_mbrs(points, epsilon, min_pts)
        pygame.display.flip()