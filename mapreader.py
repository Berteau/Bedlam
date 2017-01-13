import pygame
from pygame.locals import *
from box import PlayerBox
from box import WallBox
from box import InmateBox
from box import GuardBox
import os, sys

def readMap(walls, players, inmates, guards):
    #input = open('map.dat', 'r')
    allLines = open('map.dat', 'r').readlines()
    lineNo = 0
    for eachLine in allLines:
        colNo = 0
        for eachChar in eachLine:
            
            if eachChar == 'X':
                walls.add(WallBox([60, 60, 60], [colNo * 20, lineNo * 20], players))
            if eachChar == 'P':
                players.add(PlayerBox([20, 150, 0], [colNo * 20, lineNo * 20], len(eachLine) * 20, len(allLines) * 20, players, inmates, guards, walls))
            if eachChar == 'I':
                inmates.add(InmateBox([40, 40, 40], [colNo * 20, lineNo * 20], len(eachLine) * 20, len(allLines) * 20, players, inmates, guards, walls))
            if eachChar == 'G':
                guards.add(GuardBox([50, 50, 100], [colNo * 20, lineNo * 20], len(eachLine) * 20, len(allLines) * 20))
            colNo += 1
        lineNo += 1
        if len(eachLine) * 20 >= 640:
            swidth = len(eachLine) * 20
        else:
            swidth = 640

        if len(allLines) * 20 >= 480:
            sheight = len(allLines) * 20
        else:
            sheight = 480
            
    return pygame.Surface([swidth, sheight])