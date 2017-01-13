import pygame
from math import sqrt

def distance(sprite1, sprite2):
    x = sprite1.rect.topleft[0] - sprite2.rect.topleft[0]
    y = sprite1.rect.topleft[1] - sprite2.rect.topleft[1]
    return sqrt(x * x + y * y)

def xdir(sprite1, sprite2):
    if (sprite1.rect.topleft[0] - sprite2.rect.topleft[0]) > 0:
        return -1
    else:
        return 1
def ydir(sprite1, sprite2):
    if (sprite1.rect.topleft[1] - sprite2.rect.topleft[1]) > 0:
        return -1
    else:
        return 1