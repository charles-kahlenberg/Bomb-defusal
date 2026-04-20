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
import sys
import numpy as np

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.init()

#Chord library: note frequencies in Hz for each chord (root, third, fifth)
CHORD_LIBRARY = {
    "C_major":  [261.63, 329.63, 392.00],
    "D_minor":  [293.66, 349.23, 440.00],
    "E_minor":  [329.63, 392.00, 493.88],
    "F_major":  [349.23, 440.00, 523.25],
    "G_major":  [392.00, 493.88, 587.33],
    "A_minor":  [440.00, 523.25, 659.25],
    "B_dim":    [493.88, 587.33, 698.46],
}

def make_chord_sound(frequencies, duration=0.6, sample_rate=44100, volume=0.3):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = sum(np.sin(2 * np.pi * f * t) for f in frequencies) / len(frequencies)
    #Apply a short fade in/out to avoid clicks
    fade = int(sample_rate * 0.02)
    envelope = np.ones_like(wave)
    envelope[:fade] = np.linspace(0, 1, fade)
    envelope[-fade:] = np.linspace(1, 0, fade)
    wave = wave * envelope * volume
    audio = np.int16(wave * 32767)
    stereo = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(stereo)

COLOR = (255, 255, 255)        
SURFACE_COLOR = (115, 147, 179) 
WIDTH = 800
HEIGHT = 800

#Everything below is imported from https://www.geeksforgeeks.org/python/pygame-creating-sprites/ and modified to fit my game, I will be using sprites for the buttons that the user will press to play the melodies

#Make Sprites

HIGHLIGHT_COLOR = (255, 255, 0)  # yellow flash, visible on both red and black sprites
HIGHLIGHT_MS = 350

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.base_image = pygame.Surface([width, height])
        self.base_image.fill(SURFACE_COLOR)
        self.base_image.set_colorkey(COLOR)
        pygame.draw.rect(self.base_image, color, pygame.Rect(0, 0, width, height))

        self.highlight_image = pygame.Surface([width, height])
        self.highlight_image.fill(SURFACE_COLOR)
        self.highlight_image.set_colorkey(COLOR)
        pygame.draw.rect(self.highlight_image, HIGHLIGHT_COLOR, pygame.Rect(0, 0, width, height))

        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.highlight_until = 0

    def highlight(self, now):
        self.image = self.highlight_image
        self.highlight_until = now + HIGHLIGHT_MS

    def update_highlight(self, now):
        if self.highlight_until and now >= self.highlight_until:
            self.image = self.base_image
            self.highlight_until = 0

class ClickableSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click position (event.pos) is inside the sprite
            if self.rect.collidepoint(event.pos):
                print("Sprite clicked!")
               


RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Melody Game")

all_sprites_list = pygame.sprite.Group()

#Create Objects
object1 = Sprite(RED, 20, 30)
object2 = Sprite(BLACK, 20, 30)
object3 = Sprite(RED, 20, 30)
object4 = Sprite(BLACK, 20, 30)
object5 = Sprite(RED, 20, 30)

#Set the position of the objects
object1.rect.x = 100  
object1.rect.y = 300  
object2.rect.x = 200
object2.rect.y = 300
object3.rect.x = 300
object3.rect.y = 300
object4.rect.x = 400
object4.rect.y = 300
object5.rect.x = 500
object5.rect.y = 300

#Add the objects to the list of sprites
all_sprites_list.add(object1)
all_sprites_list.add(object2)
all_sprites_list.add(object3)
all_sprites_list.add(object4)
all_sprites_list.add(object5)

exit_game = True
clock = pygame.time.Clock()
print (clock)

sprite_objects = [object1, object2, object3, object4, object5]

#Assign one chord from the library to each button
button_chord_names = ["C_major", "D_minor", "E_minor", "F_major", "G_major"]
button_sounds = [make_chord_sound(CHORD_LIBRARY[name]) for name in button_chord_names]

#Game state
rounds = 0
strikes = 0
max_strikes = 3
game_over = False

melody = []
player_melody = []
state = "start_round"    # "start_round" -> "computer_playing" -> "player_input" -> "check"
note_index = 0
next_note_time = 0
chord_gap_ms = 800        # time between computer-played chords

while exit_game:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and state == "player_input":
            for i, obj in enumerate(sprite_objects): #Generated by Claude, modified to fit my game
                if obj.rect.collidepoint(event.pos):
                    print(f"Sprite{i+1} clicked! Playing {button_chord_names[i]}")
                    button_sounds[i].play()
                    obj.highlight(now)
                    player_melody.append(button_chord_names[i])
                    if len(player_melody) >= len(melody):
                        state = "check"
                    break

    if not game_over:
        if state == "start_round":
            melody_length = rounds + 1
            melody = [random.choice(button_chord_names) for _ in range(melody_length)]
            player_melody = []
            note_index = 0
            next_note_time = now
            print(f"Round {rounds + 1}: Listen to the melody! ({melody})")
            state = "computer_playing"

        elif state == "computer_playing":
            if now >= next_note_time:
                if note_index < len(melody):
                    chord_name = melody[note_index]
                    chord_idx = button_chord_names.index(chord_name)
                    button_sounds[chord_idx].play()
                    sprite_objects[chord_idx].highlight(now)
                    note_index += 1
                    next_note_time = now + chord_gap_ms
                else:
                    print("Your turn — repeat the melody!")
                    state = "player_input"

        elif state == "check":
            if player_melody == melody:
                print("Correct! Next round.")
                rounds += 1
            else:
                strikes += 1
                print(f"Wrong! Strike {strikes}/{max_strikes}.")
                if strikes >= max_strikes:
                    print("Game over!")
                    game_over = True
            if not game_over:
                state = "start_round"

    for s in sprite_objects:
        s.update_highlight(now)

    all_sprites_list.update()
    screen.fill(SURFACE_COLOR)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()