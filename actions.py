                                                                     
                                                                     
                                                                     
                                             
import pygame
from pygame.locals import *
import random
import ruler

class Action():
    def __init__(self, time):
        self.startTime = time
    def update(self, player, currentTime):
        return

class StandStillSilently(Action):
    def __init__(self, time, actor):
        self.startTime = time
        self.down = True
        self.right = True
        self.actor = actor
#        print('standing still...')
    
    def update(self, currentTime):
        if random.randint(1, 100) < 2: # check for break action
            self.actor.acting = False
#            print('done standing!')
        return

class WanderRandomSlow(Action):
    def __init__(self, time, actor):
        self.startTime = time
        if random.randint(1, 2) == 2: self.down = True
        else: self.down = False
        if random.randint(1, 2) == 2: self.right = True
        else: self.right = False
        self.actor = actor
#        print('Wandering randomly')

    def update(self, currentTime):
        # check to see if we quit wandering
        if currentTime %2 == 0:
            if random.randint(1, 1000) < 20:
                self.actor.acting = False
    
            # check to see if we change direction
            if random.randint(1, 100) < 3:
                self.down = not self.down
            if random.randint(1, 100) < 3:
                self.right = not self.right
            
            #call movement    
            if self.down:
                self.actor.moveDown()
            if not self.down:
                self.actor.moveUp()
            if self.right:
                self.actor.moveRight()
            if not self.right:
                self.actor.moveLeft()    

    
class WanderRandomly(Action):
    def __init__(self, time, actor):
        self.startTime = time
        if random.randint(1, 2) == 2: self.down = True
        else: self.down = False
        if random.randint(1, 2) == 2: self.right = True
        else: self.right = False
        self.actor = actor
#        print('Wandering randomly')

    def update(self, currentTime):
        # check to see if we quit wandering
        if random.randint(1, 1000) < 20:
            self.actor.acting = False

        # check to see if we change direction
        if random.randint(1, 100) < 3:
            s = pygame.mixer.Sound("slowstep1.ogg")
            if (100 - ruler.distance(self.actor, self.player) / 2) >= 0:
                s.set_volume(100.0 / (100 - ruler.distance(self.actor, self.player) / 2.0))
            else:
                s.set_volume(0)
            s.play()
            self.down = not self.down
        if random.randint(1, 100) < 3:
            s = pygame.mixer.Sound("slowstep1.ogg")
            if (100 - ruler.distance(self.actor, self.player) / 2) >= 0:
                s.set_volume(100.0 / (100 - ruler.distance(self.actor, self.player) / 2.0))
            else:
                s.set_volume(0)
            s.play()
            self.right = not self.right
        
        #call movement    
        if self.down:
            self.actor.moveDown()
        if not self.down:
            self.actor.moveUp()
        if self.right:
            self.actor.moveRight()
        if not self.right:
            self.actor.moveLeft()    
            
class WanderNearPlayer(Action):
    def __init__(self, time, actor, player):
        self.startTime = time
        if random.randint(1, 2) == 2: self.down = True
        else: self.down = False
        self.right = True
        self.actor = actor
        self.player = player
#        print('Following Player')
        
    def update(self, currentTime):
        dist = ruler.distance(self.actor, self.player)
        xdir = ruler.xdir(self.actor, self.player)
        ydir = ruler.ydir(self.actor, self.player)
        
        if dist > 150:
            if random.randint(1, 1000) < 5:
                self.actor.acting = False
        
        if dist > 50:
            if xdir > 0: self.right = True
            else: self.right = False
            if ydir > 0: self.down = True
            else: self.down = False

        if dist < 35:
            s = pygame.mixer.Sound("whisper2.ogg")
            if (100 - ruler.distance(self.actor, self.player)) >= 0:
                s.set_volume(100.0 / (100 - ruler.distance(self.actor, self.player) / 2.0))
            else:
                s.set_volume(0)
            s.play()
            if xdir > 0: self.right = False
            else: self.right = True
            if ydir > 0: self.down = False
            else: self.down = True

        if random.randint(1, 100) < 3:
            self.down = not self.down
            
        if random.randint(1, 100) < 3:
            self.right = not self.right
        
        if currentTime %2 == 0 or dist > 50:
            if self.down:
                self.actor.moveDown()
            if not self.down:
                self.actor.moveUp()
            if self.right:
                self.actor.moveRight()
            if not self.right:
                self.actor.moveLeft()
            

class ChargePlayer(Action):
    def __init__(self, time, actor, player):
        self.startTime = time
        if random.randint(1, 2) == 2: self.down = True
        else: self.down = False
        self.right = True
        self.actor = actor
        self.player = player
        self.xmomentum = ruler.xdir(self.actor, self.player) * 10
        self.ymomentum = ruler.ydir(self.actor, self.player) * 10
#        print('Charging Player')
        
    def update(self, currentTime):
        
#        print('x: ' +str(self.xmomentum))
#        print('y: ' +str(self.ymomentum))
        if self.xmomentum > 10: self.xmomentum = 10
        if self.ymomentum > 10: self.ymomentum = 10
        if self.xmomentum < -10: self.xmomentum = -10
        if self.ymomentum < -10: self.ymomentum = -10
        
        if ruler.distance(self.player, self.actor) < 35:
            self.xmomentum = ruler.xdir(self.actor, self.player)
            self.ymomentum = ruler.ydir(self.actor, self.player)

        self.xmomentum += ruler.xdir(self.actor, self.player)
        self.ymomentum += ruler.ydir(self.actor, self.player)

        if self.xmomentum > 0: self.right = True
        else: self.right = False
        if self.ymomentum > 0: self.down = True
        else: self.down = False

        if self.down:
            self.actor.moveDown()
        if not self.down:
            self.actor.moveUp()
        if self.right:
            self.actor.moveRight()
        if not self.right:
            self.actor.moveLeft()
