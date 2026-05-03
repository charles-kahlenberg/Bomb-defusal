import pygame
import random
import sys
import numpy as np
from bomb_configs import *


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

vent = pygame.image.load("vent.png").convert_alpha()
rect_surf = pygame.Surface((300, 232), pygame.SRCALPHA) 
rect_surf.fill((255, 255, 255))

angle = 0

rx = 250
ry = 500
center_pos = (rx, ry)
count = 0

melody = []
player_melody = []
final_melody = []
change = 0

fling = False
last_pressed = None

KEYPAD_LAYOUT = keypad_keys if RPi else ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
key_to_index = {}
_idx = 0
for _row in KEYPAD_LAYOUT:
    for _k in _row:
        key_to_index[_k] = _idx
        _idx += 1
        
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if RPi:
            pressed = component_keypad.pressed_keys
        else:
            pressed = []

    screen.fill((30, 30, 30))
    

    if pressed:
        if last_pressed is None:
            key = pressed[0]
            last_pressed = key
            if key in key_to_index:
                i = key_to_index[key]
                player_melody.append(i)
                target = [4,1,2,3]
                if len(player_melody) == len(target):
                    fling = True
            
    if len(player_melody) > 3:
        player_melody = []

        
    if fling:
        count += 1
        angle += 20
        rx -= 40
        ry -= 40
        
    fvent = pygame.transform.rotate(vent, angle)

    if fling:
        screen.blit(fvent, (rx,ry))
    else:
        screen.blit(fvent, (rx, ry))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
