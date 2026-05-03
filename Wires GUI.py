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
#random.seed(1)

import pygame
from pygame import *
from pygame.sprite import *
import sys
import numpy as np
from character_overlay import draw_character

MINIGAME_WINDOW_X = 300
MINIGAME_WINDOW_Y = 232
MINIGAME_WINDOW_W = 425
MINIGAME_WINDOW_H = 299

from bomb_configs import *


class WiresGUI(metaclass=abc.ABCMeta):
    """
    Represents a graphical wire component in a user interface.

    This class provides an abstraction for a visual wire element, including its
    attributes such as color, start position, and end position. It is designed
    to support both the retrieval and modification of these attributes and
    to offer methods for rendering the wire on a screen and validating its
    attachment to other wires.

    :ivar color: The color of the wire.
    :type color: Any
    :ivar end_position: The ending position of the wire represented in a coordinate
        system (e.g., tuple of x, y).
    :type end_position: Any
    :ivar start_position: The starting position of the wire represented in a
        coordinate system (e.g., tuple of x, y).
    :type start_position: Any
    """
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
    """
    Represents a red wire in the WiresGUI system.

    This class specifically handles the behavior and properties of a red wire,
    including its visual representation and interaction with user inputs.

    :ivar expected_key: The key expected to be pressed to attach this red wire.
    :type expected_key: int
    """

    def __init__(self, end_position, start_position):
        super().__init__("red", end_position, start_position)
        self.expected_key = K_5

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 0, 0), self.start_position, self.end_position, 5)

    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key


class BlueWire(WiresGUI):
    """
    Represents a blue wire in the Wires GUI.

    This class is responsible for rendering a blue wire and verifying
    whether the correct key is pressed based on the wire's expected key.
    It inherits from the `WiresGUI` class.

    :ivar expected_key: The key that is expected to be pressed for this
    wire to register correctly.
    :type expected_key: int
    :ivar start_position: The starting position of the wire on the screen.
    :type start_position: tuple[int, int]
    :ivar end_position: The ending position of the wire on the screen.
    :type end_position: tuple[int, int]
    """

    def __init__(self, end_position, start_position):
        super().__init__("blue", end_position, start_position)
        self.expected_key = K_6

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (0, 0, 255), self.start_position, self.end_position, 5)

    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key


class YellowWire(WiresGUI):
    """
    Represents a yellow wire in the Wires GUI component.

    This class is used to manage and render a yellow wire with specific
    visual characteristics and functionality. It provides methods to
    draw the wire and check if a specific key is attached to it.

    :ivar expected_key: The key that is expected to be pressed to attach to
    this wire.
    :type expected_key: int
    """

    def __init__(self, end_position, start_position):
        super().__init__("yellow", end_position, start_position)
        self.expected_key = K_7

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 255, 0), self.start_position, self.end_position, 5)

    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key


class GreenWire(WiresGUI):
    """
    Represents a green wire in the GUI.

    Provides functionality to draw the green wire on the screen and check
    if a specific key is associated with it.

    :ivar expected_key: The key expected to be associated with this wire.
    :type expected_key: int
    """

    def __init__(self, end_position, start_position):
        super().__init__("green", end_position, start_position)
        self.expected_key = K_8

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (0, 255, 0), self.start_position, self.end_position, 5)

    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key


class OrangeWire(WiresGUI):
    """
    Represents an orange wire in the GUI.

    :ivar expected_key: The key expected to be associated with this wire.
    :type expected_key: int
    """

    def __init__(self, end_position, start_position):
        super().__init__("orange", end_position, start_position)
        self.expected_key = K_9

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 165, 0), self.start_position, self.end_position, 5)

    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key

def create_game_state():
    """
    Creates and initializes the game state by setting up color configurations,
    circle locations, and other related variables.
    """
    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    orange = (255, 165, 0)

    # Variables
    circle_radius = 28

    circle_loc_top = [[112, 190], [312, 190], [512, 190], [712, 190], [912, 190]]
    circle_loc_bottom = [[112, 430], [312, 430], [512, 430], [712, 430], [912, 430]]

    # random.shuffle(circle_loc_bottom)

    # Top row (input wires)
    circle1_x, circle1_y = circle_loc_top[0]
    circle2_x, circle2_y = circle_loc_top[1]
    circle3_x, circle3_y = circle_loc_top[2]
    circle4_x, circle4_y = circle_loc_top[3]
    circle5_x, circle5_y = circle_loc_top[4]

    # Bottom row (output wires)
    circle6_x, circle6_y = circle_loc_bottom[0]
    circle7_x, circle7_y = circle_loc_bottom[1]
    circle8_x, circle8_y = circle_loc_bottom[2]
    circle9_x, circle9_y = circle_loc_bottom[3]
    circle10_x, circle10_y = circle_loc_bottom[4]

    return {
        "colors": {
            "white": white,
            "black": black,
            "red": red,
            "blue": blue,
            "yellow": yellow,
            "green": green,
            "orange": orange,
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
            "circle9": (circle9_x, circle9_y),
            "circle10": (circle10_x, circle10_y),
        },
    }


def draw_text_centered(surface, font, text, color, center):
    """
    Draws a given text string centered at the specified position on the given surface.

    This function uses the provided font and color to render the text, and it ensures
    the text is centered based on the given position. The rendered text is then drawn
    onto the provided surface.

    :param surface: The surface to draw the text on.
    :type surface: pygame.Surface
    :param font: The font used to render the text.
    :type font: pygame.font.Font
    :param text: The string of text to be rendered and drawn.
    :type text: str
    :param color: The color of the text in RGB format.
    :type color: tuple[int, int, int]
    :param center: The (x, y) coordinates to center the text on.
    :type center: tuple[int, int]
    :return: None
    """
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, text_surface.get_rect(center=center))


def get_current_wire_values():
    """
    Returns the current physical connected/disconnected state for each RPi wire.
    """
    if not RPi:
        return []

    return [pin.value for pin in component_wires]


def get_pressed_wire_from_rpi(previous_wire_values):
    """
    Returns the index of the newly connected RPi wire, or None if no new wire was connected.
    """
    if not RPi:
        return None

    for index, pin in enumerate(component_wires):
        current_value = pin.value

        if current_value and not previous_wire_values[index]:
            previous_wire_values[index] = current_value
            return index

        previous_wire_values[index] = current_value

    return None


def main(screen=None, clock=None):
    """
    The `main` function initializes and runs a Pygame application for a wires-based GUI game.
    The game requires players to select and connect wires to their correct endpoints.
    Players win by successfully connecting all wires correctly, and lose if
    too many incorrect connection attempts (strikes) are made.
    """
    if not pygame.get_init():
        pygame.init()
    pygame.font.init()

    created_display = screen is None
    if screen is None:
        screen = display.set_mode((1024, 576))

    display.set_caption("Wires GUI")

    main_screen = screen
    game_surface = pygame.Surface((1024, 576), pygame.SRCALPHA)
    screen = game_surface

    intro_bg = pygame.image.load("base.png").convert()
    intro_bg = pygame.transform.scale(intro_bg, main_screen.get_size())
    minigame_rect = pygame.Rect(
        MINIGAME_WINDOW_X,
        MINIGAME_WINDOW_Y,
        MINIGAME_WINDOW_W,
        MINIGAME_WINDOW_H
    )

    def show_frame():
        main_screen.blit(intro_bg, (0, 0))
        draw_character(main_screen)
        scaled_game = pygame.transform.smoothscale(game_surface, minigame_rect.size)
        main_screen.blit(scaled_game, minigame_rect)
        pygame.display.flip()

    all_sprites_list = pygame.sprite.Group()
    strike_count = 0
    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 72)

    if clock is None:
        clock = pygame.time.Clock()

    state = create_game_state()
    colors = state["colors"]
    points = state["points"]
    circle_radius = state["circle_radius"]

    print("Watch the wires! Press 1-5 or connect a wire on the RPi.")

    # Wire objects (created once; drawn each frame when connected)
    blue_wire = BlueWire(points["circle6"], points["circle1"])
    red_wire = RedWire(points["circle7"], points["circle2"])
    yellow_wire = YellowWire(points["circle8"], points["circle3"])
    green_wire = GreenWire(points["circle9"], points["circle4"])
    orange_wire = OrangeWire(points["circle10"], points["circle5"])

    connected = {
        "red": False,
        "blue": False,
        "yellow": False,
        "green": False,
        "orange": False,
    }

    wire_order = [blue_wire, red_wire, yellow_wire, green_wire, orange_wire]
    current_target_wire = random.choice(wire_order)

    key_to_wire_index = {
        K_1: 0,
        K_2: 1,
        K_3: 2,
        K_4: 3,
        K_5: 4,
    }

    previous_wire_values = [False for _ in component_wires]

    game_over = False
    won = False

    running = True
    while running:
        current_wire_values = get_current_wire_values()

        if RPi and not game_over:
            for index, wire in enumerate(wire_order):
                if connected[wire.color] and not current_wire_values[index]:
                    connected[wire.color] = False
                    current_target_wire = wire

        pressed_wire_index = get_pressed_wire_from_rpi(previous_wire_values)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if created_display:
                    pygame.quit()
                return False

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key in key_to_wire_index:
                    pressed_wire_index = key_to_wire_index[event.key]

        if pressed_wire_index is not None and not game_over:
            pressed_wire = wire_order[pressed_wire_index]

            if pressed_wire == current_target_wire and not connected[pressed_wire.color]:
                connected[pressed_wire.color] = True

                if all(connected.values()):
                    game_over = True
                    won = True
                else:
                    remaining_wires = [
                        wire for wire in wire_order
                        if not connected[wire.color]
                    ]
                    current_target_wire = random.choice(remaining_wires)
            else:
                strike_count += 1

                if strike_count >= 3:
                    game_over = True
                    won = False

        screen.fill(colors["black"])

        # Top row input circles
        for circle_name, wire in [
            ("circle1", blue_wire),
            ("circle2", red_wire),
            ("circle3", yellow_wire),
            ("circle4", green_wire),
            ("circle5", orange_wire),
        ]:
            if connected[wire.color] or wire == current_target_wire:
                color_name = wire.color
            else:
                color_name = "white"

            pygame.draw.circle(screen, colors[color_name], points[circle_name], circle_radius)
            draw_text_centered(screen, font, "", colors["black"], points[circle_name])

        # Bottom row output circles
        for circle_name, wire in [
            ("circle6", blue_wire),
            ("circle7", red_wire),
            ("circle8", yellow_wire),
            ("circle9", green_wire),
            ("circle10", orange_wire),
        ]:
            if connected[wire.color] or wire == current_target_wire:
                color_name = wire.color
            else:
                color_name = "white"

            pygame.draw.circle(screen, colors[color_name], points[circle_name], circle_radius)
            draw_text_centered(screen, font, "", colors["black"], points[circle_name])

        # Draw connected wires
        if connected["red"]:
            red_wire.draw(screen)
        if connected["blue"]:
            blue_wire.draw(screen)
        if connected["yellow"]:
            yellow_wire.draw(screen)
        if connected["green"]:
            green_wire.draw(screen)
        if connected["orange"]:
            orange_wire.draw(screen)

        # Strike counter
        strike_text = font.render(f"Strikes: {strike_count}/3", True, colors["white"])
        screen.blit(strike_text, (10, 10))

        # Wire prompt
        if not game_over:
            prompt = font.render(
                f"Connect the {current_target_wire.color} wire",
                True,
                colors["white"]
            )
            screen.blit(prompt, (10, 50))

        # Win / lose overlay
        if game_over:
            msg = "YOU WIN!" if won else "BOOM — YOU LOSE"
            msg_color = colors["green"] if won else colors["red"]
            end_text = big_font.render(msg, True, msg_color)
            screen.blit(end_text, end_text.get_rect(center=(512, 288)))
            show_frame()
            pygame.time.wait(1500)

            if created_display:
                pygame.quit()

            return won

        show_frame()
        clock.tick(60)

    if created_display:
        pygame.quit()

    return won


if __name__ == "__main__":
    raise SystemExit(main())
