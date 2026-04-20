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
#If button is pressed and gave is not over, check if the button pressed corresponds with correct place
#else, add to strike counter
#If all buttons are in the correct place, print win statement
#If strike counter >= 3, print lose statement and quit game





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


def create_game_state():
    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)

    # Variables
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

    return {
        "colors": {
            "white": white,
            "black": black,
            "red": red,
            "blue": blue,
            "yellow": yellow,
            "green": green,
        },
        "circle_radius": circle_radius,
        "points": {
            "circle1": (circle1_x, circle1_y),
            "circle2": (circle2_x, circle2_y),
            "circle3": (circle3_x, circle3_y),
            "circle4": (circle4_x, circle4_y),
            "circle5": (circle5_x, circle5_y),
            "circle6": (circle6_x, circle6_y),
            "circle7": (circle7_x, circle7_y),
            "circle8": (circle8_x, circle8_y),
        },
    }


def draw_text_centered(surface, font, text, color, center):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, text_surface.get_rect(center=center))


def main():
    pygame.init()
    pygame.font.init()

    screen = display.set_mode((800, 800))
    display.set_caption("Wires GUI")

    strike_count = 0
    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 72)
    clock = pygame.time.Clock()

    state = create_game_state()
    colors = state["colors"]
    points = state["points"]
    circle_radius = state["circle_radius"]

    print("Watch the wires! Pressed the designate key that corresponds to the wire color to cut it. Red = R, Green = G, Blue = B, Yellow = Y")

    # Wire objects (created once; drawn each frame when connected)
    red_wire = RedWire(points["circle6"], points["circle2"])
    blue_wire = BlueWire(points["circle5"], points["circle1"])
    yellow_wire = YellowWire(points["circle7"], points["circle3"])
    green_wire = GreenWire(points["circle8"], points["circle4"])

    # Which wires have been connected
    connected = {"red": False, "blue": False, "yellow": False, "green": False}

    # Sequential order: player must connect these wires one at a time, in order.
    wires_in_order = [red_wire, blue_wire, yellow_wire, green_wire]
    current_index = 0
    game_over = False
    won = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        screen.fill(colors["black"])

        # Top row (input circles)
        pygame.draw.circle(screen, colors["red"], points["circle1"], circle_radius)
        draw_text_centered(screen, font, "R", colors["black"], points["circle1"])

        pygame.draw.circle(screen, colors["blue"], points["circle2"], circle_radius)
        draw_text_centered(screen, font, "B", colors["black"], points["circle2"])

        pygame.draw.circle(screen, colors["yellow"], points["circle3"], circle_radius)
        draw_text_centered(screen, font, "Y", colors["black"], points["circle3"])

        pygame.draw.circle(screen, colors["green"], points["circle4"], circle_radius)
        draw_text_centered(screen, font, "G", colors["black"], points["circle4"])

        # Bottom row (output circles)
        pygame.draw.circle(screen, colors["red"], points["circle5"], circle_radius)
        draw_text_centered(screen, font, "R", colors["black"], points["circle5"])

        pygame.draw.circle(screen, colors["blue"], points["circle6"], circle_radius)
        draw_text_centered(screen, font, "B", colors["black"], points["circle6"])

        pygame.draw.circle(screen, colors["yellow"], points["circle7"], circle_radius)
        draw_text_centered(screen, font, "Y", colors["black"], points["circle7"])

        pygame.draw.circle(screen, colors["green"], points["circle8"], circle_radius)
        draw_text_centered(screen, font, "G", colors["black"], points["circle8"])

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
        strike_text = font.render(f"Strikes: {strike_count}", True, colors["white"])
        screen.blit(strike_text, (10, 10))

        # Next-wire prompt
        if not game_over:
            prompt = font.render(
                f"Connect wire {current_index + 1} — press {5 + current_index}",
                True,
                colors["white"],
            )
            screen.blit(prompt, (10, 50))

        # Win / lose overlay
        if game_over:
            msg = "YOU WIN!" if won else "BOOM — YOU LOSE"
            msg_color = colors["green"] if won else colors["red"]
            end_text = big_font.render(msg, True, msg_color)
            screen.blit(end_text, end_text.get_rect(center=(400, 400)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
