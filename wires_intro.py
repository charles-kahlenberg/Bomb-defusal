"""
wires_intro.py

Story/instruction sequence before the wires minigame.

Responsibilities:
- Displays the wire panel background and wire endpoint art.
- Shows dialogue explaining the wires challenge.
- Uses a threaded typewriter effect for dialogue.
- Supports Enter input on PC and button input on RPi.

Main classes:
- WiresIntroTextState: Stores dialogue state.
- WiresIntroTextThread: Updates dialogue reveal timing.

Returns:
- True when the intro finishes normally.
- False when the player closes the window.
"""


import pygame
import threading
import time

from character_overlay import draw_character
from display_utils import create_fullscreen_display

try:
    from bomb_configs import RPi, component_button_state
except ImportError:
    RPi = False
    component_button_state = None


GAME_W = 1024
GAME_H = 576

MINIGAME_WINDOW_X = 300
MINIGAME_WINDOW_Y = 232
MINIGAME_WINDOW_W = 425
MINIGAME_WINDOW_H = 299

TEXTBOX_X = 277
TEXTBOX_Y = 42
TEXTBOX_WIDTH = 471
TEXTBOX_HEIGHT = 132
TEXTBOX_ALPHA = 180
TEXT_PADDING_X = 18
TEXT_PADDING_Y = 16
PROMPT_OFFSET_Y = 90
TEXT_LINE_SPACING = 24


def draw_wrapped_text(surface, font, text, color, x, y, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = word if current_line == "" else current_line + " " + word

        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    for index, line in enumerate(lines):
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y + index * TEXT_LINE_SPACING))


class WiresIntroTextState:
    def __init__(self, messages):
        self.lock = threading.Lock()
        self.running = True
        self.result = True

        self.messages = messages
        self.active_message = 0
        self.message = messages[0]
        self.counter = 0
        self.speed = 1
        self.done = False
        self.final_message_done_time = None
        self.advance_requested = False
        self.talking_counter = 0


class WiresIntroTextThread(threading.Thread):
    def __init__(self, state):
        super().__init__(daemon=True)
        self.state = state

    def run(self):
        while True:
            with self.state.lock:
                if not self.state.running:
                    break

                now = pygame.time.get_ticks()

                if self.state.advance_requested and self.state.done:
                    self.state.advance_requested = False

                    if self.state.active_message < len(self.state.messages) - 1:
                        self.state.active_message += 1
                        self.state.message = self.state.messages[self.state.active_message]
                        self.state.counter = 0
                        self.state.done = False
                        self.state.final_message_done_time = None
                        self.state.talking_counter = 0
                    else:
                        self.state.running = False
                        break

                if self.state.counter < self.state.speed * len(self.state.message):
                    self.state.counter += 1
                    self.state.talking_counter += 1

                    if self.state.talking_counter > 20:
                        self.state.talking_counter = 0
                else:
                    self.state.done = True
                    self.state.talking_counter = 0

                    if self.state.active_message == len(self.state.messages) - 1:
                        if self.state.final_message_done_time is None:
                            self.state.final_message_done_time = now
                        elif now - self.state.final_message_done_time >= 3000:
                            self.state.running = False
                            break

            time.sleep(1 / 24)


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    created_display = screen is None
    if screen is None:
        screen = create_fullscreen_display("Wires Intro")

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Wires Intro")

    main_screen = screen
    game_surface = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
    screen = game_surface

    bg = pygame.image.load("img_keys/base.png").convert()
    bg = pygame.transform.scale(bg, main_screen.get_size())

    wire_bg = pygame.image.load("img_keys/WireBG.png").convert()
    wire_bg = pygame.transform.scale(wire_bg, game_surface.get_size())

    def load_intro_image(path, scale):
        image = pygame.image.load(path).convert_alpha()
        new_size = (
            int(image.get_width() * scale),
            int(image.get_height() * scale)
        )
        return pygame.transform.smoothscale(image, new_size)

    def draw_image_centered(surface, image, center):
        surface.blit(image, image.get_rect(center=center))

    wire_circle_images = {
        "circle1": load_intro_image("img_keys/W1T.png", 2.25),
        "circle2": load_intro_image("img_keys/W2T.png", 2.25),
        "circle3": load_intro_image("img_keys/W3T.png", 2.25),
        "circle4": load_intro_image("img_keys/W4T.png", 2.25),
        "circle5": load_intro_image("img_keys/W5T.png", 2.25),
        "circle6": load_intro_image("img_keys/W1B.png", 2.25),
        "circle7": load_intro_image("img_keys/W2B.png", 2.25),
        "circle8": load_intro_image("img_keys/W3B.png", 2.25),
        "circle9": load_intro_image("img_keys/W4B.png", 2.25),
        "circle10": load_intro_image("img_keys/W5B.png", 2.25),
    }

    connected_wire_images = {
        "blue": load_intro_image("img_keys/Wire1.png", 2.2),
        "red": load_intro_image("img_keys/Wire2.png", 2.4),
        "yellow": load_intro_image("img_keys/Wire3.png", 2.2),
        "green": load_intro_image("img_keys/Wire4.png", 2.4),
        "orange": load_intro_image("img_keys/Wire5.png", 2.0),
    }

    circle_positions = {
        "circle1": (112, 184),
        "circle2": (312, 143),
        "circle3": (512, 152),
        "circle4": (712, 168),
        "circle5": (912, 114),
        "circle6": (112, 450),
        "circle7": (312, 416),
        "circle8": (512, 430),
        "circle9": (712, 428),
        "circle10": (912, 418),
    }

    minigame_rect = pygame.Rect(
        MINIGAME_WINDOW_X,
        MINIGAME_WINDOW_Y,
        MINIGAME_WINDOW_W,
        MINIGAME_WINDOW_H
    )

    messages = [
        "The vent cover crashes open, revealing the bomb's wire panel.",
        "These wires are still live. Touching the wrong one will count against you.",
        "The display will tell you which wire needs to be connected next.",
        "Pay attention, move carefully.",
    ]

    text_state = WiresIntroTextState(messages)
    text_thread = WiresIntroTextThread(text_state)
    text_thread.start()

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)
    talking_sound = pygame.mixer.Sound("img_keys/C2Talking.mp3")

    prev_btn = False

    def show_frame():
        with text_state.lock:
            typed_text = text_state.message[0:text_state.counter // text_state.speed]
            done = text_state.done
            active_message = text_state.active_message

        main_screen.blit(bg, (0, 0))
        draw_character(main_screen)

        text_box = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
        text_box.fill((0, 0, 0, TEXTBOX_ALPHA))
        main_screen.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

        border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        pygame.draw.rect(main_screen, (255, 255, 255), border_rect, 2)

        draw_wrapped_text(
            main_screen,
            font,
            typed_text,
            "white",
            TEXTBOX_X + TEXT_PADDING_X,
            TEXTBOX_Y + TEXT_PADDING_Y,
            TEXTBOX_WIDTH - TEXT_PADDING_X * 2
        )

        if done and active_message < len(messages) - 1:
            prompt_text = "Press Button" if RPi else "Press Enter"
            prompt = font.render(prompt_text, True, (180, 180, 180))
            main_screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + PROMPT_OFFSET_Y))

        scaled_game = pygame.transform.smoothscale(game_surface, minigame_rect.size)
        main_screen.blit(scaled_game, minigame_rect)

        pygame.display.flip()

    while True:
        with text_state.lock:
            running = text_state.running
            should_play_talking = text_state.talking_counter == 1 and not text_state.done

        if not running:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with text_state.lock:
                    text_state.running = False
                    text_state.result = False

                if created_display:
                    pygame.quit()

                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not RPi:
                    with text_state.lock:
                        text_state.advance_requested = True

        if RPi and component_button_state is not None:
            btn = component_button_state.value

            if btn and not prev_btn:
                with text_state.lock:
                    text_state.advance_requested = True

            prev_btn = btn

        screen.blit(wire_bg, (0, 0))

        for circle_name, position in circle_positions.items():
            draw_image_centered(screen, wire_circle_images[circle_name], position)

        if should_play_talking:
            talking_sound.play()

        with text_state.lock:
            if text_state.done:
                pygame.mixer.stop()

        show_frame()
        clock.tick(24)

    with text_state.lock:
        text_state.running = False
        result = text_state.result

    text_thread.join(timeout=0.5)

    if created_display:
        pygame.quit()

    return result


if __name__ == "__main__":
    raise SystemExit(main())