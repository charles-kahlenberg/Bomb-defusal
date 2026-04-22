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

def create_game_state():
    """
    Creates and initializes the game state by setting up color configurations,
    circle locations, and other related variables. The circle coordinates are
    randomized to introduce variability in their placement.

    :return: A dictionary containing the game state information, including color
             mappings, circle radius, and randomized coordinates for input and
             output wire points.
    :rtype: dict
    """
    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)

    # Variables
    circle_radius = 30

    circle_loc_top = [[150, 250], [310, 250], [470, 250], [630, 250]]
    circle_loc_bottom = [[150, 550], [310, 550], [470, 550], [630, 550]]

    random.shuffle(circle_loc_bottom)

    # Top row (input wires) - 4 columns evenly spaced
    circle1_x, circle1_y = circle_loc_top[0]   # Red input
    circle2_x, circle2_y = circle_loc_top[1]   # Blue input
    circle3_x, circle3_y = circle_loc_top[2]   # Yellow input
    circle4_x, circle4_y = circle_loc_top[3]   # Green input

    # Bottom row (output wires) - 4 columns evenly spaced
    circle5_x, circle5_y = circle_loc_bottom[0]   # Red output
    circle6_x, circle6_y = circle_loc_bottom[1]   # Blue output
    circle7_x, circle7_y = circle_loc_bottom[2]   # Yellow output
    circle8_x, circle8_y = circle_loc_bottom[3]   # Green output

    return {
        "colors": {
            "white": white,
            "black": black,
            "red": blue, # for some reason blue and red are swapped, so I swapped them here. good fix!
            "blue": red,
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


def main():
    """
    The `main` function initializes and runs a Pygame application for a wires-based GUI game.
    The game requires players to select and connect wires to their correct endpoints.
    Players win by successfully connecting all wires correctly, and lose if
    too many incorrect connection attempts (strikes) are made.

    :raises SystemExit: When the game is exited.
    :raises pygame.error: If Pygame initialization fails.
    :return: 0 upon successful game termination.

    Variables:
        **screen** (*Surface*): The main Pygame display surface for the game window.
        **strike_count** (*int*): Tracks the number of incorrect wire connection attempts.
        **font** (*Font*): Font object for rendering small-sized text.
        **big_font** (*Font*): Font object for rendering large-sized text.
        **clock** (*Clock*): Pygame clock object used to control the game's framerate.
        **state** (*dict*): A dictionary holding initial game state configuration.
        **colors** (*dict*): A mapping of color keys to RGB color values.
        **points** (*dict*): A mapping of circular input and output point identifiers to their positions.
        **circle_radius** (*int*): The radius for the input and output circle graphics.
        **red_wire** (*RedWire*): Instance of a wire connecting specific input and output points for red.
        **blue_wire** (*BlueWire*): Instance of a wire connecting specific input and output points for blue.
        **yellow_wire** (*YellowWire*): Instance of a wire connecting specific input and output points for yellow.
        **green_wire** (*GreenWire*): Instance of a wire connecting specific input and output points for green.
        **connected** (*dict*): A dictionary tracking which wires have been successfully connected.
        **wire_map** (*dict*): Maps number keys 1-8 to their corresponding wire objects and circle names.
        **selected_wire** (*WiresGUI or None*): The currently selected wire awaiting connection.
        **selected_start** (*str or None*): The circle name of the selected wire's start point.
        **game_over** (*bool*): Indicates whether the game has ended.
        **won** (*bool*): Tracks whether the player has won the game.
        **running** (*bool*): Controls whether the game loop continues execution.
    """
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

    print("Watch the wires! Press 1-4 to select top wires, 5-8 to connect to bottom wires.")

    # Wire objects (created once; drawn each frame when connected)
    blue_wire = BlueWire(points["circle5"], points["circle1"])
    red_wire = RedWire(points["circle6"], points["circle2"])
    yellow_wire = YellowWire(points["circle7"], points["circle3"])
    green_wire = GreenWire(points["circle8"], points["circle4"])

    # Which wires have been connected
    connected = {"red": False, "blue": False, "yellow": False, "green": False}

    # this stays the same
    wire_order = [blue_wire, red_wire, yellow_wire, green_wire]

    bottom_row_keys = []

    bottom_row_pos = [points["circle5"][0], points["circle6"][0], points["circle7"][0], points["circle8"][0]]
    bottom_row_pos.sort()

    for circle in ["circle5", "circle6", "circle7", "circle8"]:
        if bottom_row_pos[0] == points[circle][0]:
            bottom_row_keys.append(K_5)
        elif bottom_row_pos[1] == points[circle][0]:
            bottom_row_keys.append(K_6)
        elif bottom_row_pos[2] == points[circle][0]:
            bottom_row_keys.append(K_7)
        elif bottom_row_pos[3] == points[circle][0]:
            bottom_row_keys.append(K_8)

    # Map keys to wires and circles
    wire_map = {
        K_1: {"wire": wire_order[0], "circle": "circle1", "type": "start"},
        K_2: {"wire": wire_order[1], "circle": "circle2", "type": "start"},
        K_3: {"wire": wire_order[2], "circle": "circle3", "type": "start"},
        K_4: {"wire": wire_order[3], "circle": "circle4", "type": "start"},
        bottom_row_keys[0]: {"wire": wire_order[0], "circle": "circle5", "type": "end"},
        bottom_row_keys[1]: {"wire": wire_order[1], "circle": "circle6", "type": "end"},
        bottom_row_keys[2]: {"wire": wire_order[2], "circle": "circle7", "type": "end"},
        bottom_row_keys[3]: {"wire": wire_order[3], "circle": "circle8", "type": "end"},
    }

    selected_wire = None
    selected_start = None
    game_over = False
    won = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not game_over:
                # Check if the key is valid
                if event.key in wire_map:
                    mapping = wire_map[event.key]

                    # If no wire is selected, select a start wire (keys 1-4)
                    if selected_wire is None and mapping["type"] == "start":
                        selected_wire = mapping["wire"]
                        selected_start = mapping["circle"]

                    # If a wire is selected, try to connect it (keys 5-8)
                    elif selected_wire is not None and mapping["type"] == "end":
                        # Check if this is the correct endpoint for the selected wire
                        if mapping["wire"] == selected_wire:
                            # Correct connection!
                            connected[selected_wire.color] = True
                            selected_wire = None
                            selected_start = None

                            # Check if all wires are connected
                            if all(connected.values()):
                                game_over = True
                                won = True
                        else:
                            # Wrong connection - strike!
                            strike_count += 1
                            selected_wire = None
                            selected_start = None

                            if strike_count >= 3:
                                game_over = True
                                won = False

        screen.fill(colors["black"])

        # Top row (input circles) with highlighting
        for i, (circle_name, label, color_name) in enumerate([
            ("circle1", "B", "red"),
            ("circle2", "R", "blue"),
            ("circle3", "Y", "yellow"),
            ("circle4", "G", "green")
        ]):
            # Highlight if this circle is selected
            radius = circle_radius + 10 if selected_start == circle_name else circle_radius
            pygame.draw.circle(screen, colors[color_name], points[circle_name], radius)
            draw_text_centered(screen, font, label, colors["black"], points[circle_name])

        # Bottom row (output circles)
        pygame.draw.circle(screen, colors["red"], points["circle5"], circle_radius)
        draw_text_centered(screen, font, "B", colors["black"], points["circle5"])

        pygame.draw.circle(screen, colors["blue"], points["circle6"], circle_radius)
        draw_text_centered(screen, font, "R", colors["black"], points["circle6"])

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
        strike_text = font.render(f"Strikes: {strike_count}/3", True, colors["white"])
        screen.blit(strike_text, (10, 10))

        # Wire selection prompt
        if not game_over:
            if selected_wire is None:
                prompt = font.render("Select a wire (1-4)", True, colors["white"])
            else:
                prompt = font.render(f"Connect {selected_wire.color} wire (5-8)", True, colors["white"])
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
