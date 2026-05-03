#Charles Jumping Game

#Source: https://www.youtube.com/watch?v=PjgLeP0G5Yw&t=601s & https://github.com/techwithtim/Side-Scroller-Game/tree/master/images


import pygame
from pygame.locals import *
import os
import random

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
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

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
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-13)

        #pygame.draw.rect(win, (255,0,0),self.hitbox, 2)

    class rock(object):
        img = (pygame.image.load(os.path.join('images'), 'SAW0'))
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.hitbox = (x,y,width, height)
            self.count = 0
        
        def draw(self, win):
            self.hitbox = ()
            if self.count >= 8:
                self.count = 0
            win.blit(self.img[self.count//2], (self.x,self.y))
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    

def redrawGameWindow(): #draws background and objects (all drawings happen in one place)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    charles_runner.draw(win)
    pygame.display.update()

charles_runner = player(200, 420, 64,64) #64 x 64 Sprite

pygame.time.set_timer(USEREVENT+1, 500)
speed = 80 
clock.tick(speed) #gets the FPS
run = True
while run: #while game is running
    redrawGameWindow()
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
        if event.type == USEREVENT+1:
            speed += 1
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if not (charles_runner.jumping):
            charles_runner.jumping = True
    
    
    
    clock.tick(speed) #sets the FPS

