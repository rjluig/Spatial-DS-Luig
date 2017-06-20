"""
Ryan Luig
Spatial Data Structs

"""
import json
import pygame
import pprint as pp
import sys
import time


if __name__ == "__main__":

    f = open('./Assignments/Program_3/quake-adjusted.json','r')
    data = json.loads(f.read())
    #pp.pprint(data)

    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Earthquakes')
    bg = pygame.image.load('./Assignments/Program_3/bg-map.png')
    screen.blit(bg, (0,0))

    pygame.display.flip()
    years = []
    for x in range(1960,2017):
        years.append(str(x))
    pp.pprint(years)
    count = 0

    running = True
    while running:
        if count < len(years):
            for p in data[years[count]]:
                pygame.draw.circle(screen, (255,0,0), p, 1,0)
            time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                #clean_area(screen,(0,0),width,height,(255,255,255))
        pygame.display.flip()
        count += 1