#Pseudocode:
#Create wire class that allows me set an end position for 
#1,2,3,4 wires are the input wires that  cannot be modified
#5,6,7,8 wires are the end points of the wires
#Game starts with the user having to move Wire 1 to Output 5, if they fail, add a strike
#Next the user has to move Wire 2 to Output 9, if they fail, add a strike
#Next the user has to move Wire 3 to Output 7, if they fail, add a strike
#Next the user has to move Wire 4 to Output 8, if they fail, add a strike
#If the user gets 3 strikes, they lose. If they get all 4 wires correct, they win and get a winning screen
#Pygame for GUI
#2x4 grid of circles, with the top row being the input wires and the bottom row being the output wires. Each circle will have a letter in it that corresponds to the color of the wire. The user will have to press the corresponding key to cut the wire and move it to the correct output. If they cut the wrong wire, they get a strike. If they get 3 strikes, they lose. If they get all 4 wires correct, they win and get a winning screen.
#When the correct wire is attached, the wire will be drawn on the screen connecting the input and output circles. When the wrong wire is attached, a strike will be added and the wire will not be drawn. The user will have to press the corresponding key to cut the wire and move it to the correct output. If they cut the wrong wire, they get a strike. If they get 3 strikes, they lose. If they get all 4 wires correct, they win and get a winning screen.
#Circles for the start positions and output positons




import abc
import random
import pygame
from pygame import *
from pygame.sprite import *
import sys


class WiresGUI(metaclass=abc.ABCMeta):
    def __init__(self, color, end_position, start_position):
        self.color = color
        self.end_position = end_position
        self.start_position = start_position
    #Getters
    def get_color(self):
        return self.color
    def get_end_position(self):
        return self.end_position
    def get_start_position(self):
        return self.start_position
    #Setters
    def set_color(self, color):
        self.color = color
    def set_end_position(self, end_position):
        self.end_position = end_position
    def set_start_position(self, start_position):
        self.start_position = start_position
    #Methods
    def draw(self, screen):
        pass
    def check_attached(self, wires):
        pass

class RedWire(WiresGUI):
    def __init__(self, end_position, start_position):
        super().__init__("red", end_position, start_position)
        self.expected_key = K_5
    def draw(self, screen):
        draw.line(screen, (255, 0, 0), self.start_position, self.end_position, 5)
    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key

class BlueWire(WiresGUI):
    def __init__(self, end_position, start_position):
        super().__init__("blue", end_position, start_position)
        self.expected_key = K_6
    def draw(self, screen):
        draw.line(screen, (0, 0, 255), self.start_position, self.end_position, 5)
    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key


class YellowWire(WiresGUI):
    def __init__(self, end_position, start_position):
        super().__init__("yellow", end_position, start_position)
        self.expected_key = K_7
    def draw(self, screen):
        draw.line(screen, (255, 255, 0), self.start_position, self.end_position, 5)
    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key

class GreenWire(WiresGUI):
    def __init__(self, end_position, start_position):
        super().__init__("green", end_position, start_position)
        self.expected_key = K_8
    def draw(self, screen):
        draw.line(screen, (0, 255, 0), self.start_position, self.end_position, 5)
    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key
# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
        

#Main Program
pygame.init()
screen = display.set_mode((800, 800))
display.set_caption("Wires GUI")

#Variables
strike_count = 0
pygame.font.init()
font = pygame.font.SysFont(None, 36)


# create / set up any sprites necessary.

# Define circles for wire connection points

circle_radius = 30

# Top row (input wires) - 4 columns evenly spaced
circle1_x, circle1_y = 150, 250   # Red input
circle2_x, circle2_y = 310, 250   # Blue input
circle3_x, circle3_y = 470, 250   # Yellow input
circle4_x, circle4_y = 630, 250   # Green input

# Bottom row (output wires) - 4 columns evenly spaced
circle5_x, circle5_y = 150, 550   # Red output
circle6_x, circle6_y = 310, 550   # Blue output
circle7_x, circle7_y = 470, 550   # Yellow output
circle8_x, circle8_y = 630, 550   # Green output

#Draw circles

print("Watch the wires! Pressed the designate key that corresponds to the wire color to cut it. Red = R, Green = G, Blue = B, Yellow = Y")

# Wire objects (created once; drawn each frame when connected)
red_wire = RedWire((circle5_x, circle5_y), (circle1_x, circle1_y))
blue_wire = BlueWire((circle6_x, circle6_y), (circle2_x, circle2_y))
yellow_wire = YellowWire((circle7_x, circle7_y), (circle3_x, circle3_y))
green_wire = GreenWire((circle8_x, circle8_y), (circle4_x, circle4_y))

# Which wires have been connected
connected = {"red": False, "blue": False, "yellow": False, "green": False}

# Sequential order: player must connect these wires one at a time, in order.
wires_in_order = [red_wire, blue_wire, yellow_wire, green_wire]
current_index = 0
game_over = False
won = False
big_font = pygame.font.SysFont(None, 72)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not game_over:
            expected_wire = wires_in_order[current_index]
            if expected_wire.check_attached(event.key):
                connected[expected_wire.color] = True
                current_index += 1
                if current_index == len(wires_in_order):
                    game_over = True
                    won = True
            else:
                strike_count += 1
                if strike_count >= 3:
                    game_over = True
                    won = False

    # Clear the screen
    screen.fill(black)

    # Top row (input circles)
    pygame.draw.circle(screen, red, (circle1_x, circle1_y), circle_radius)
    screen.blit(font.render("R", True, black), font.render("R", True, black).get_rect(center=(circle1_x, circle1_y)))

    pygame.draw.circle(screen, blue, (circle2_x, circle2_y), circle_radius)
    screen.blit(font.render("B", True, black), font.render("B", True, black).get_rect(center=(circle2_x, circle2_y)))

    pygame.draw.circle(screen, yellow, (circle3_x, circle3_y), circle_radius)
    screen.blit(font.render("Y", True, black), font.render("Y", True, black).get_rect(center=(circle3_x, circle3_y)))

    pygame.draw.circle(screen, green, (circle4_x, circle4_y), circle_radius)
    screen.blit(font.render("G", True, black), font.render("G", True, black).get_rect(center=(circle4_x, circle4_y)))

    # Bottom row (output circles)
    pygame.draw.circle(screen, red, (circle5_x, circle5_y), circle_radius)
    screen.blit(font.render("R", True, black), font.render("R", True, black).get_rect(center=(circle5_x, circle5_y)))

    pygame.draw.circle(screen, blue, (circle6_x, circle6_y), circle_radius)
    screen.blit(font.render("B", True, black), font.render("B", True, black).get_rect(center=(circle6_x, circle6_y)))

    pygame.draw.circle(screen, yellow, (circle7_x, circle7_y), circle_radius)
    screen.blit(font.render("Y", True, black), font.render("Y", True, black).get_rect(center=(circle7_x, circle7_y)))

    pygame.draw.circle(screen, green, (circle8_x, circle8_y), circle_radius)
    screen.blit(font.render("G", True, black), font.render("G", True, black).get_rect(center=(circle8_x, circle8_y)))

    # Draw connected wires
    if connected["red"]:
        red_wire.draw(screen)
    if connected["blue"]:
        blue_wire.draw(screen)
    if connected["yellow"]:
        yellow_wire.draw(screen)
    if connected["green"]:
        green_wire.draw(screen)

    # Strike counter
    strike_text = font.render(f"Strikes: {strike_count}", True, white)
    screen.blit(strike_text, (10, 10))

    # Next-wire prompt
    if not game_over:
        prompt = font.render(
            f"Connect wire {current_index + 1} \u2014 press {5 + current_index}",
            True, white,
        )
        screen.blit(prompt, (10, 50))

    # Win / lose overlay
    if game_over:
        msg = "YOU WIN!" if won else "BOOM \u2014 YOU LOSE"
        msg_color = green if won else red
        end_text = big_font.render(msg, True, msg_color)
        screen.blit(end_text, end_text.get_rect(center=(400, 400)))

    pygame.display.flip()
    clock.tick(60)



