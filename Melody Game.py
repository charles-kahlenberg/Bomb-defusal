#Melody Game

#######Notes
#Use sprits in the form of square for each key


#Psuedocode:

#1. Create a list of melodies (each melody is a list of notes)
#2. Each button has a sound for a melody
#3. When a button is pressed, play the corresponding melody, in which each button is presssed by the computer in corresponding order to the melody
#4. The player must repeat the melody by pressing the buttons in the correct order
#5. If the player presses the correct buttons in the correct order, they move on to the next melody
#6. If the player presses the wrong button, they get a strike counter added to them, and they have to start the melody over again
#7 If the player gets 3 strikes, they lose and have to start the game over again

import pygame
import random

COLOR = (255, 255, 255)        
SURFACE_COLOR = (115, 147, 179) 
WIDTH = 800
HEIGHT = 800

#Everything below is imported from https://www.geeksforgeeks.org/python/pygame-creating-sprites/ and modified to fit my game, I will be using sprites for the buttons that the user will press to play the melodies

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()

pygame.init()

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Melody Game")

all_sprites_list = pygame.sprite.Group()

object_ = Sprite(WHITE, 20, 30)
object2 = Sprite(BLACK, 20, 30)
object3 = Sprite(WHITE, 20, 30)
object4 = Sprite(BLACK, 20, 30)
object5 = Sprite(WHITE, 20, 30)

object_.rect.x = 100  
object_.rect.y = 300  
object2.rect.x = 200
object2.rect.y = 300
object3.rect.x = 300
object3.rect.y = 300
object4.rect.x = 400
object4.rect.y = 300
object5.rect.x = 500
object5.rect.y = 300

all_sprites_list.add(object_)
all_sprites_list.add(object2)
all_sprites_list.add(object3)
all_sprites_list.add(object4)
all_sprites_list.add(object5)

exit_game = True
clock = pygame.time.Clock()

while exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = False

    all_sprites_list.update()  
    screen.fill(SURFACE_COLOR)  
    all_sprites_list.draw(screen) 
    pygame.display.flip()       
    clock.tick(60)              

pygame.quit()