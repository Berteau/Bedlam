import pygame
import math
import random
import actions
import ruler
import rays

class Box(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

class PlayerBox(pygame.sprite.Sprite):
    def __init__(self, color, initial_position, width, height, players, inmates, guards, walls):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.light = False
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.restart_pos = initial_position
        self.right_edge = width
        self.bottom_edge = height
        self.players = players
        self.inmates = inmates
        self.guards = guards
        self.walls = walls
        self.width = width
        self.next_update_time = 0 # update() hasn't been called yet.

    def update(self, current_time, up, down, left, right, inmates, guards, walls, light):
        if self.next_update_time < current_time:

            if down:
                self.moveDown()
            if up:
                self.moveUp()
            if right:
                self.moveRight()
            if left:
                self.moveLeft()
#            self.castLight()
            self.next_update_time = current_time + 10

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= 1
            if pygame.sprite.spritecollideany(self, self.inmates): 
                self.kill()
                self.rect.left += 1
            if pygame.sprite.spritecollideany(self, self.guards):self.kill()
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.left += 1
    def moveRight(self):
        if self.rect.right < self.right_edge:
            self.rect.right += 1
            if pygame.sprite.spritecollideany(self, self.inmates): 
                self.kill()
                self.rect.right -= 1
            if pygame.sprite.spritecollideany(self, self.guards):self.kill()
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.right -= 1
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= 1
            if pygame.sprite.spritecollideany(self, self.inmates): 
                self.kill()
                self.rect.top += 1
            if pygame.sprite.spritecollideany(self, self.guards):self.kill()
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.top += 1
    def moveDown(self):
        if self.rect.bottom < self.bottom_edge:
            self.rect.top += 1
            if pygame.sprite.spritecollideany(self, self.inmates): 
                self.kill()
                self.rect.top -= 1
            if pygame.sprite.spritecollideany(self, self.guards): 
                self.rect.top -= 1
                self.kill()
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.top -= 1
            
    def castLight(self):
        for eachDegree in range(0, 360, 10):
            castResult = rays.castRay(self.rect.topleft, [1, math.tan(eachDegree * 0.0174532925)], 5 , [self.walls])
            if castResult.doCollide:
                #print('I lit something up!')
                castResult.sprite.light = True
                
            
    def kill(self):
        self.rect.topleft = self.restart_pos
        self.image.fill([100, 30, 0])

class InmateBox(pygame.sprite.Sprite):
    def __init__(self, color, initial_position, width, height, players, inmates, guards, walls):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.right_edge = width
        self.bottom_edge = height
        self.players = players
        self.inmates = inmates
        self.guards = guards
        self.walls = walls
        self.next_update_time = 0 # update() hasn't been called yet.
        self.acting = False
        self.action = actions.WanderRandomly(0, self)
        self.following = False

    def update(self, current_time, light):
        if self.next_update_time < current_time:

            #check for notice of player
            for p in self.players.sprites():
                if ruler.distance(self,p) < 150:
                    self.following = True
                else:
                    self.following = False

            #determine color
            if not light:
                bright = 50 - ruler.distance(self,p)
                if bright < 0: bright = 0
                self.image.fill([bright,bright,bright])
            
            #if following
            if self.following and self.acting == False:
                self.acting = True
                s = pygame.mixer.Sound("whisper3.ogg")
                s.set_volume(100 - ruler.distance(self, p))
                s.play()
                self.action = actions.WanderNearPlayer(current_time, self, p)
      
            #if light was turned on, then charge
            if self.following and light:
                if not isinstance(self.action, actions.ChargePlayer):
                    s = pygame.mixer.Sound("whisper2.ogg")
                    s.play()
                    self.action = actions.ChargePlayer(current_time, self, p)
                    
            #if light was turned off, stop charging
            if isinstance(self.action, actions.ChargePlayer) and not light:
                self.action = actions.StandStillSilently(current_time, self)
                    
            # if wandering
            if self.acting == False:
                if random.randint(1, 100) < 30:
                    self.acting = True
                    self.action = actions.StandStillSilently(current_time, self)
                else:
                    self.acting = True
                    s = pygame.mixer.Sound("slowstep1.ogg")
                    if (100 - ruler.distance(self, p) / 2) >= 0:
                        s.set_volume(100 - ruler.distance(self, p))
                    else:
                        s.set_volume(0)
                    s.play()
                    self.action = actions.WanderRandomSlow(current_time, self)
            self.action.update(current_time)
            self.next_update_time = current_time + 30

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= 1
            if pygame.sprite.spritecollideany(self, self.players): 
                if isinstance(self.action, actions.ChargePlayer):
                    for p in self.players.sprites():
                        p.kill();
                self.rect.left += 1
            if pygame.sprite.spritecollideany(self, self.guards): self.rect.left += 1
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.left += 1
            self.inmates.remove(self)
            if pygame.sprite.spritecollideany(self, self.inmates): self.rect.left += 1
            self.inmates.add(self)
    def moveRight(self):
        if self.rect.right < self.right_edge:
            self.rect.right += 1
            if pygame.sprite.spritecollideany(self, self.players): 
                if isinstance(self.action, actions.ChargePlayer):
                    for p in self.players.sprites():
                        p.kill();
                self.rect.right -= 1
            if pygame.sprite.spritecollideany(self, self.guards): self.rect.right -= 1
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.right -= 1
            self.inmates.remove(self)
            if pygame.sprite.spritecollideany(self, self.inmates): self.rect.right -= 1
            self.inmates.add(self)
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= 1
            if pygame.sprite.spritecollideany(self, self.players): 
                if isinstance(self.action, actions.ChargePlayer):
                    for p in self.players.sprites():
                        p.kill();
                self.rect.top += 1
            if pygame.sprite.spritecollideany(self, self.guards): self.rect.top += 1
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.top += 1
            self.inmates.remove(self)
            if pygame.sprite.spritecollideany(self, self.inmates): self.rect.top += 1
            self.inmates.add(self)
    def moveDown(self):
        if self.rect.bottom < self.bottom_edge:
            self.rect.top += 1
            if pygame.sprite.spritecollideany(self, self.players): 
                if isinstance(self.action, actions.ChargePlayer):
                    for p in self.players.sprites():
                        p.kill();
                self.rect.top -= 1
            if pygame.sprite.spritecollideany(self, self.guards): self.rect.top -= 1
            if pygame.sprite.spritecollideany(self, self.walls): self.rect.top -= 1
            self.inmates.remove(self)
            if pygame.sprite.spritecollideany(self, self.inmates): self.rect.top -= 1
            self.inmates.add(self)

class GuardBox(pygame.sprite.Sprite):
    def __init__(self, color, initial_position, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.right_edge = width
        self.bottom_edge = height
        self.going_down = True # Start going downwards            
        self.next_update_time = 0 # update() hasn't been called yet.

    def update(self, current_time, players, inmates, walls, light):
        if self.next_update_time < current_time:
            # If we're at the top or bottom of the screen, switch directions.
            for p in players:
                b = 1
            if self.rect.bottom == self.bottom_edge - 1: self.going_down = False
            elif self.rect.top == 0: self.going_down = True
            
            if pygame.sprite.spritecollideany(self, walls) and self.going_down == False:
                self.going_down = True
                self.rect.top += 1
            if pygame.sprite.spritecollideany(self, players) and self.going_down == False:
                p.kill()
                self.going_down = True
                self.rect.top += 1
            if pygame.sprite.spritecollideany(self, inmates) and self.going_down == False:
                self.going_down = True
                self.rect.top += 1
            
            if pygame.sprite.spritecollideany(self, walls) and self.going_down == True: self.going_down = False
            if pygame.sprite.spritecollideany(self, players): p.kill()
            if pygame.sprite.spritecollideany(self, inmates) and self.going_down == True: self.going_down = False
     
            # Move our position up or down by one pixel
            if self.going_down: self.rect.top += 1
            else: self.rect.top -= 1

            self.next_update_time = current_time + 25
            
class WallBox(pygame.sprite.Sprite):
    def __init__(self, color, initial_position, players):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill([60,60,60])
        self.rect = self.image.get_rect()
        self.light = False
        self.players = players
        for p in players:
            self.p = p
        self.lit = False
        self.rect.topleft = initial_position
        
    def update(self, current_time, light):
        
        for p in self.players:
            self.p = p
        
        #determine color
        if not light:
            bright = 100 - ruler.distance(self, self.p)
            if bright < 0: bright = 0
            self.image.fill([bright,bright/2,bright/2])
        
        if self.light and not self.lit:
            self.lit = True
            self.image.fill([60,60,60])
        if not self.light and self.lit:
            self.lit = False
            self.image = pygame.image.load('wallblock.png').convert()
        
class UpDownBox(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.going_down = True # Start going downwards
        self.next_update_time = 0 # update() hasn't been called yet.

    def update(self, current_time, bottom):
        # Update every 10 milliseconds = 1/100th of a second.
        if self.next_update_time < current_time:

            # If we're at the top or bottom of the screen, switch directions.
            if self.rect.bottom == bottom - 1: self.going_down = False
            elif self.rect.top == 0: self.going_down = True
     
            # Move our position up or down by one pixel
            if self.going_down: self.rect.top += 1
            else: self.rect.top -= 1

            self.next_update_time = current_time + 10
