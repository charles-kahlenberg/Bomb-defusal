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

    def __init__(self, end_position, start_position, pin=None):
        super().__init__("red", end_position, start_position)
        self.pin = pin
        self.expected_key = K_5

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 255, 255), self.start_position, self.end_position, 5)

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

    def __init__(self, end_position, start_position, pin=None):
        super().__init__("blue", end_position, start_position)
        self.pin = pin
        self.expected_key = K_6

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 255, 255), self.start_position, self.end_position, 5)

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

    def __init__(self, end_position, start_position, pin=None):
        super().__init__("yellow", end_position, start_position)
        self.pin = pin
        self.expected_key = K_7

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 255, 255), self.start_position, self.end_position, 5)

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

    def __init__(self, end_position, start_position, pin=None):
        super().__init__("green", end_position, start_position)
        self.pin = pin
        self.expected_key = K_8

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 255, 255), self.start_position, self.end_position, 5)

    def check_attached(self, pressed_key):
        return pressed_key == self.expected_key


class PurpleWire(WiresGUI):
    """
    Represents a purple wire in the GUI.

    :ivar expected_key: The key expected to be associated with this wire.
    :type expected_key: int
    """

    def __init__(self, end_position, start_position, pin=None):
        super().__init__("purple", end_position, start_position)
        self.pin = pin
        self.expected_key = K_9

    def get_expected_key(self):
        return self.expected_key

    def set_expected_key(self, expected_key):
        self.expected_key = expected_key

    def draw(self, screen):
        draw.line(screen, (255, 255, 255), self.start_position, self.end_position, 5)

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
    purple = (128, 0, 128)

    # Variables
    circle_radius = 30

    circle_loc_top = [[80, 250], [240, 250], [400, 250], [560, 250], [720, 250]]
    circle_loc_bottom = [[80, 550], [240, 550], [400, 550], [560, 550], [720, 550]]

    random.shuffle(circle_loc_bottom)

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
            "purple": purple,
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

    print("Watch the wires! Press 1-5 to select top wires, 6-9 to connect to bottom wires.")

    # pull jumper-wire pins from bomb_configs when running on the Pi.
    # component_wires order: D14, D15, D18, D23, D24 -> blue, red, yellow, green, purple
    wire_pins = component_wires if RPi else [None] * 5

    # wire objects (created once; drawn each frame when connected)
    blue_wire = BlueWire(points["circle6"], points["circle1"], pin=wire_pins[0])
    red_wire = RedWire(points["circle7"], points["circle2"], pin=wire_pins[1])
    yellow_wire = YellowWire(points["circle8"], points["circle3"], pin=wire_pins[2])
    green_wire = GreenWire(points["circle9"], points["circle4"], pin=wire_pins[3])
    purple_wire = PurpleWire(points["circle10"], points["circle5"], pin=wire_pins[4])

    connected = {
        "red": False,
        "blue": False,
        "yellow": False,
        "green": False,
        "purple": False,
    }

    wire_order = [blue_wire, red_wire, yellow_wire, green_wire, purple_wire]

    bottom_row_keys = []
    bottom_row_pos = [
        points["circle6"][0],
        points["circle7"][0],
        points["circle8"][0],
        points["circle9"][0],
        points["circle10"][0],
    ]
    bottom_row_pos.sort()

    for circle in ["circle6", "circle7", "circle8", "circle9", "circle10"]:
        if bottom_row_pos[0] == points[circle][0]:
            bottom_row_keys.append(K_6)
        elif bottom_row_pos[1] == points[circle][0]:
            bottom_row_keys.append(K_7)
        elif bottom_row_pos[2] == points[circle][0]:
            bottom_row_keys.append(K_8)
        elif bottom_row_pos[3] == points[circle][0]:
            bottom_row_keys.append(K_9)
        elif bottom_row_pos[4] == points[circle][0]:
            bottom_row_keys.append(K_0)

    wire_map = {
        K_1: {"wire": wire_order[0], "circle": "circle1", "type": "start"},
        K_2: {"wire": wire_order[1], "circle": "circle2", "type": "start"},
        K_3: {"wire": wire_order[2], "circle": "circle3", "type": "start"},
        K_4: {"wire": wire_order[3], "circle": "circle4", "type": "start"},
        K_5: {"wire": wire_order[4], "circle": "circle5", "type": "start"},
        bottom_row_keys[0]: {"wire": wire_order[0], "circle": "circle6", "type": "end"},
        bottom_row_keys[1]: {"wire": wire_order[1], "circle": "circle7", "type": "end"},
        bottom_row_keys[2]: {"wire": wire_order[2], "circle": "circle8", "type": "end"},
        bottom_row_keys[3]: {"wire": wire_order[3], "circle": "circle9", "type": "end"},
        bottom_row_keys[4]: {"wire": wire_order[4], "circle": "circle10", "type": "end"},
    }

    selected_wire = None
    selected_start = None
    selected_end = None
    game_over = False
    won = False

    # track physical wire pin states so we only fire on True->False (cut) transitions.
    # pulled-down inputs read True when the jumper bridges to 3V3, False when cut.
    all_wires = [blue_wire, red_wire, yellow_wire, green_wire, purple_wire]
    prev_pin_state = {w.color: (bool(w.pin.value) if w.pin is not None else None) for w in all_wires}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not game_over:
                # Check if the key is valid
                if event.key in wire_map:
                    mapping = wire_map[event.key]

                    # If no wire is selected, select a start wire (keys 1-5) (Claude generated this block)
                    if selected_wire is None and mapping["type"] == "start":
                        selected_wire = mapping["wire"]
                        selected_start = mapping["circle"]
                        # Find the corresponding end circle for this wire
                        for key, val in wire_map.items():
                            if val["type"] == "end" and val["wire"] == selected_wire:
                                selected_end = val["circle"]
                                break

                    # If a wire is selected, try to connect it (keys 6-0)
                    elif selected_wire is not None and mapping["type"] == "end":
                        # Check if this is the correct endpoint for the selected wire
                        if mapping["wire"] == selected_wire:
                            # Correct connection!
                            connected[selected_wire.color] = True
                            selected_wire = None
                            selected_start = None
                            selected_end = None

                            # Check if all wires are connected
                            if all(connected.values()):
                                game_over = True
                                won = True
                        else:
                            # Wrong connection - strike!
                            strike_count += 1
                            selected_wire = None
                            selected_start = None
                            selected_end = None

                            if strike_count >= 3:
                                game_over = True
                                won = False

        # hardware poll: plugging a wire into its top pin (False->True) selects that wire,
        # exactly like pressing K_1..K_5 on the keyboard. The user still confirms the
        # randomized bottom slot with keyboard 6-0; a wrong slot is handled above as a strike.
        if not game_over and selected_wire is None:
            for w in all_wires:
                if w.pin is None:
                    continue
                current = bool(w.pin.value)
                if prev_pin_state[w.color] is False and current is True and not connected[w.color]:
                    selected_wire = w
                    # find this wire's start and (randomized) end circles
                    for _val in wire_map.values():
                        if _val["wire"] is w and _val["type"] == "start":
                            selected_start = _val["circle"]
                        elif _val["wire"] is w and _val["type"] == "end":
                            selected_end = _val["circle"]
                prev_pin_state[w.color] = current
        else:
            # keep prev state in sync even when we are not acting on it
            for w in all_wires:
                if w.pin is None:
                    continue
                prev_pin_state[w.color] = bool(w.pin.value)

        screen.fill(colors["black"])

        # Top row (input circles) with highlighting and color change
        for i, (circle_name, label) in enumerate([
            ("circle1", ""),
            ("circle2", ""),
            ("circle3", ""),
            ("circle4", ""),
            ("circle5", ""),
        ]):
            # Determine the color: show wire color if selected, otherwise white
            color_name = "white"
            if selected_start == circle_name and selected_wire is not None:
                color_name = selected_wire.color

            radius = circle_radius + 10 if selected_start == circle_name else circle_radius
            pygame.draw.circle(screen, colors[color_name], points[circle_name], radius)
            draw_text_centered(screen, font, label, colors["black"], points[circle_name])

        # Bottom row (output circles) with color change when top wire is selected
        for circle_name in ["circle6", "circle7", "circle8", "circle9", "circle10"]:
            # Determine the color: show wire color if this is the selected wire's end, otherwise white
            color_name = "white"
            if selected_end == circle_name and selected_wire is not None:
                color_name = selected_wire.color

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
        if connected["purple"]:
            purple_wire.draw(screen)

        # Strike counter
        strike_text = font.render(f"Strikes: {strike_count}/3", True, colors["white"])
        screen.blit(strike_text, (10, 10))

        # Wire selection prompt
        if not game_over:
            if selected_wire is None:
                prompt = font.render("Select a wire (1-5)", True, colors["white"])
            else:
                prompt = font.render(f"Connect {selected_wire.color} wire (6-0)", True, colors["white"])
            screen.blit(prompt, (10, 50))

        # Win / lose overlay
        if game_over:
            msg = "YOU WIN!" if won else "BOOM — YOU LOSE"
            msg_color = colors["green"] if won else colors["red"]
            end_text = big_font.render(msg, True, msg_color)
            screen.blit(end_text, end_text.get_rect(center=(400, 400)))
            return won

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return won


if __name__ == "__main__":
    raise SystemExit(main())
