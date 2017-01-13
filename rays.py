import math
import pygame
from math import sqrt

class RayCastingResult():
    def __init__(self):
        self.doCollide = False
        self.sprite = pygame.sprite.Sprite()
        self.position = [0,0]

def normalize(vector):
    length = sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / length, vector[1] / length

def isPointTraversable(point, sprites):
    for eachGroup in sprites:
        for eachSprite in eachGroup:
            if eachSprite.rect.topleft == point:
#            if eachSprite.rect.collidepoint(point[0], point[1]):
#                print('hit!')
                return False, eachSprite
    return True, eachSprite

def castRay(position, direction, length, sprites):
    #print(position, direction, length)
    position = [position[0] / 20, position[1] / 20]
    result = RayCastingResult()
    
    # exit if ray length = 0
    if length <= 0:
        result.doCollide = isPointTraversable(position, sprites)
        result.position = position
        return result
    
    # get points from bresenham
    direction = normalize(direction)
    points = bresenham(position, [position[0] + direction[0] * length, position[1] + direction[1] * length])
    if len(points) > 0:
        #print points
        for point in points:
            traverse = isPointTraversable(point, sprites)
            if not traverse[0]:
                result.position = point
                result.sprite = traverse[1]
                result.doCollide = True
                return result
    return result

def bresenham(locA, locB):
    results = []
    
    steep = abs(locB[1] - locA[1]) > abs(locB[0] - locA[0])
    if steep:
        locA = (locA[1], locA[0])
        locB = (locB[1], locB[0])
        
    if locA[0] > locA[1]:
        temp = locA
        locA = locB
        locB = temp
    
    deltax = locB[0] - locA[0]
    deltay = abs(locB[1] - locA[1])
    error = 0
    ystep = 0
    y = locA[1]
    if (locA[1] < locB[1]):
        ystep = 1
    else:
        ystep = -1
    x = locA[0]
    while x <= locB[0]:
        #print 'x: '+str(x) +' of '+ str(locB[0])
        if steep: 
            results.append([y,x])
        else:
            results.append([x,y])
            error += deltay
            if (2* error >= deltax):
                y += ystep
                error -= deltax
        x += 1
    return results
