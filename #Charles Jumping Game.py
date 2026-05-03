#Charles Jumping Game

#Source: https://www.youtube.com/watch?v=PjgLeP0G5Yw&t=601s & https://github.com/techwithtim/Side-Scroller-Game/tree/master/images


import pygame
from pygame.locals import *
import os
import random
import math
import sys
import time

pygame.init()

W, H = 1024, 576
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bg = pygame.transform.scale(bg, (W, H))
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.falling = False
        self.jumpCount = 0
        self.runCount = 0

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount//18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)

        elif self.falling: #draw hitbox for falling
            win.blit(self.fall, (self.x, self.y + 30))

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-13)

        pygame.draw.rect(win, (255,0,0), self.hitbox, 2) #Remind to delete this

        #pygame.draw.rect(win, (255,0,0),self.hitbox, 2)

class rock(object):
    img = [pygame.image.load(os.path.join('images', f'SAW{x}.png')) for x in range(4)]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, win):
        if self.count >= 8:
            self.count = 0
        self.hitbox = (self.x, self.y, self.width, self.height)
        win.blit(pygame.transform.scale(self.img[self.count//2], (64,64)), (self.x, self.y))
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]: #check if feet is below the hitbox of saw
                return True
            return False

    

def redrawGameWindow(): #draws background and objects (all drawings happen in one place)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    charles_runner.draw(win)
    for x in objects: #randomly draw image
        x.draw(win)
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Timer:' + str(currentTimer), 1 , (255,255,255))
    win.blit(text, (700, 10))
    pygame.display.update()



def endScreen(): #if collide, reset game
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)    
        #finishedTimer = largeFont.render('Timer: timer', 1, (255,255,255))
        #pygame.display.update()
            

rocky = rock(300, 410, 64, 64)
charles_runner = player(200, 420, 64,64) #64 x 64 Sprite

pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(2000, 3500))
speed = 80 
clock.tick(speed) #gets the FPS
run = True
pause = 0
won = False
fallSpeed = 0

objects = []
start_ticks = pygame.time.get_ticks()
while run:
    currentTimer = max(0, 30 - (pygame.time.get_ticks() - start_ticks) // 1000)

    if currentTimer <= 0:
        won = True
        endScreen()

    #currentTime = clock.ticks()
    #if currentTime 
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    for objectt in objects: 
        if objectt.collide(charles_runner.hitbox):
            charles_runner.falling = True

            if pause == 0: #pause game
                fallSpeed = speed
                pause = 1

        objectt.x -= 1.4
        if objectt.x < -objectt.width * -1:
            objects.pop(objects.index(objectt))

    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1: #first background image starts at 0 , 0 then start maoving backwwards then gets to the negative width, so it is off the screen
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == USEREVENT+1: #increase the spedd of character
            speed += 1
        if event.type == USEREVENT+2:  #
            r = random.randrange(0,2)
            if r == 0:
                objects.append(rock(810,410,64,64))
            #else: Put in the other object
            #   objects.append(name())

            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if not (charles_runner.jumping):
            charles_runner.jumping = True
    
    
    clock.tick(speed) #sets the FPS
    redrawGameWindow()

