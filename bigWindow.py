import pygame
import random
from pygame.locals import *
from box import PlayerBox
from box import WallBox
from box import GuardBox
from box import InmateBox
import mapreader
import sys

pygame.init()

startTime = pygame.time.get_ticks()
screen = pygame.display.set_mode([640, 480])
title = pygame.image.load("title.png")
titlerect = title.get_rect()
sound = pygame.mixer.Sound("introtheme.ogg")
sound.play()

#while pygame.time.get_ticks() - startTime < 3000:

while pygame.event.poll().type != KEYDOWN:
    screen.blit(title, titlerect)
    pygame.display.update()
sound.stop()

right = False
up = False
down = False
left = False

light = False

walls = pygame.sprite.Group()
players = pygame.sprite.Group()
inmates = pygame.sprite.Group()
guards = pygame.sprite.Group()

gameSurface = mapreader.readMap(walls, players, inmates, guards) 
#walls.add(WallBox([20, 20, 20], [300, 240]))
#walls.add(WallBox([20, 20, 20], [300, 260]))
#walls.add(WallBox([20, 20, 20], [300, 280]))
#walls.add(WallBox([20, 20, 20], [300, 300]))

#players.add(PlayerBox([20, 150, 0], [200, 200], 640, 480))

genOn = False

while True:
    for event in pygame.event.get():
        if (event.type == KEYUP):
            if (event.key == K_RIGHT): right = False
            if (event.key == K_LEFT): left = False
            if (event.key == K_UP): up = False
            if (event.key == K_DOWN): down = False
        
        elif (event.type == KEYDOWN):
            if (event.key == K_RIGHT): right = True
            if (event.key == K_LEFT): left = True
            if (event.key == K_UP): up = True
            if (event.key == K_DOWN): down = True
            if (event.key == K_ESCAPE):
                pygame.display.quit
                sys.exit()
            if (event.key == K_l):
                light = not light

    if not light:
        gameSurface.fill([0, 0, 0]) # blank the screen.
    else:
        gameSurface.fill([30,30,10])
    
    
    
    players.update(pygame.time.get_ticks(), up, down, left, right, inmates, guards, walls, light)
    guards.update(pygame.time.get_ticks(), players, inmates, walls, light)
    inmates.update(pygame.time.get_ticks(), light)
    walls.update(pygame.time.get_ticks(), light)
    if not genOn and random.randint(1, 10000) <= 5:
        genOn = True
        s = pygame.mixer.Sound("generator.ogg")
        s.set_volume(0.6)
        s.play()
        generatorStartTime = pygame.time.get_ticks()
        
    if genOn and pygame.time.get_ticks() - generatorStartTime >= 1000:
        s.set_volume(0.9)
        light = True
        
    if genOn and pygame.time.get_ticks() - generatorStartTime >= 5000:
        s.stop()
        genOn = False
        light = False
        
    for b in players.sprites():
        gameSurface.blit(b.image, b.rect)
        cameraRect = b.rect.inflate(620, 460)
        if cameraRect.topleft[0] < 0:
            cameraRect.move_ip(-cameraRect.topleft[0], 0) 
        if cameraRect.topleft[1] < 0:
            cameraRect.move_ip(0, -cameraRect.topleft[1])
        if cameraRect.bottomright[0] > gameSurface.get_clip().bottomright[0] - 20:
            cameraRect.move_ip(-(cameraRect.bottomright[0] - (gameSurface.get_clip().bottomright[0] - 20)), 0) 
        if cameraRect.bottomright[1] > gameSurface.get_clip().bottomright[1]:
            cameraRect.move_ip(0, -(cameraRect.bottomright[1] - (gameSurface.get_clip().bottomright[1])))

    for w in walls.sprites(): gameSurface.blit(w.image, w.rect)
    for i in inmates.sprites(): gameSurface.blit(i.image, i.rect)
    for g in guards.sprites(): gameSurface.blit(g.image, g.rect)

    screen.blit(gameSurface.subsurface(cameraRect), titlerect)
    pygame.display.update()

