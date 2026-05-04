"""
outro.py

A simple ending/story sequence for the bomb defusal game.

How to edit this file:
1. Add or change dialogue in the MESSAGES list.
2. Adjust textbox position/size using the TEXTBOX constants.
3. Adjust typing speed using TYPE_SPEED.
4. Add extra images, sounds, or animations inside the main loop where marked.

This file is designed to be called from bomb.py using:

    module.main(screen, clock)

It can also be run directly for testing.
"""

import pygame

from character_overlay import draw_character
from display_utils import create_fullscreen_display

# Try to import Raspberry Pi controls.
# If the game is running on a normal computer, these will safely fall back.
try:
    from bomb_configs import RPi, component_button_state
except ImportError:
    RPi = False
    component_button_state = None


# ---------------------------------------------------------------------------
# TEXTBOX SETTINGS
# ---------------------------------------------------------------------------
# These control where the dialogue box appears and how it looks.
# Increase/decrease X and Y to move it around the screen.
TEXTBOX_X = 277
TEXTBOX_Y = 42
TEXTBOX_WIDTH = 471
TEXTBOX_HEIGHT = 132
TEXTBOX_ALPHA = 180

# Padding controls how far the text sits inside the box.
TEXT_PADDING_X = 18
TEXT_PADDING_Y = 16

# Where the "Press Enter" / "Press Button" prompt appears inside the textbox.
PROMPT_OFFSET_Y = 90

# Distance between wrapped text lines.
TEXT_LINE_SPACING = 24


# ---------------------------------------------------------------------------
# TIMING SETTINGS
# ---------------------------------------------------------------------------
# Lower TYPE_SPEED means faster typing.
# Current behavior:
#   TYPE_SPEED = 1 means 1 character appears per frame.
#
# If you want slower text, increase TYPE_SPEED and change the counter logic.
TYPE_SPEED = 1

# The outro runs at 24 FPS to match the intro-style sequences.
FPS = 24

# How long the final message stays onscreen before the outro ends.
FINAL_MESSAGE_WAIT_MS = 3000


# ---------------------------------------------------------------------------
# ASSET PATHS
# ---------------------------------------------------------------------------
# Change these if you want the outro to use a different background or font.
BACKGROUND_PATH = "img_keys/base.png"
FONT_PATH = "img_keys/Baskic8.otf"
WIRE_BACKGROUND_PATH = "img_keys/WireBG.png"


# ---------------------------------------------------------------------------
# WIRE BACKGROUND SETTINGS
# ---------------------------------------------------------------------------
# These control where the wire background appears during the outro.
# Change X/Y to move it. Change WIDTH/HEIGHT to resize it.
WIRE_BACKGROUND_X = 300
WIRE_BACKGROUND_Y = 232
WIRE_BACKGROUND_WIDTH = 425
WIRE_BACKGROUND_HEIGHT = 299


# ---------------------------------------------------------------------------
# OUTRO DIALOGUE
# ---------------------------------------------------------------------------
# Add, remove, or edit lines here to change the outro sequence.
#
# Each string is one message.
# The player must press Enter/Button to advance after each message finishes.
# The final message automatically exits after FINAL_MESSAGE_WAIT_MS.
#
# Use "\n" inside a string to force a line break.
MESSAGES = [
    "The final switch clicks into place.",
    "The bomb goes silent.",
    "Charles exhales, realizing he made it out alive.",
    "A light encapsulates his eyes....",
]


def draw_wrapped_text(surface, font, text, color, x, y, max_width):
    """
    Draws text onto the screen and wraps it so it stays inside the textbox.

    Args:
        surface: The pygame Surface to draw on.
        font: The pygame Font used for rendering.
        text: The text to draw.
        color: Text color, such as "white" or (255, 255, 255).
        x: Starting x-position.
        y: Starting y-position.
        max_width: Maximum line width before wrapping.

    Notes:
        This supports manual line breaks using "\\n".
    """
    lines = []

    # Split into paragraphs first so "\n" creates intentional line breaks.
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current_line = ""

        for word in words:
            test_line = word if current_line == "" else current_line + " " + word

            # If the test line fits, keep building it.
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                # If it does not fit, save the current line and start a new one.
                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

    # Draw every wrapped line.
    for index, line in enumerate(lines):
        rendered_line = font.render(line, True, color)
        surface.blit(
            rendered_line,
            (
                x,
                y + index * TEXT_LINE_SPACING
            )
        )


def draw_textbox(surface, font, typed_text, done, active_message):
    """
    Draws the dialogue textbox, the current typed text, and the advance prompt.

    Args:
        surface: The pygame Surface to draw on.
        font: The pygame Font used for rendering.
        typed_text: The portion of the message currently visible.
        done: True when the current message is fully typed.
        active_message: Index of the current message in MESSAGES.
    """
    # Create a transparent textbox surface.
    text_box = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
    text_box.fill((0, 0, 0, TEXTBOX_ALPHA))
    surface.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

    # Draw the white border around the textbox.
    border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
    pygame.draw.rect(surface, (255, 255, 255), border_rect, 2)

    # Draw the dialogue text inside the box.
    draw_wrapped_text(
        surface,
        font,
        typed_text,
        "white",
        TEXTBOX_X + TEXT_PADDING_X,
        TEXTBOX_Y + TEXT_PADDING_Y,
        TEXTBOX_WIDTH - TEXT_PADDING_X * 2
    )

    # Show a prompt only after the text finishes, and only if more messages remain.
    if done and active_message < len(MESSAGES) - 1:
        prompt_text = "Press Button" if RPi else "Press Enter"
        prompt = font.render(prompt_text, True, (180, 180, 180))
        surface.blit(
            prompt,
            (
                TEXTBOX_X + TEXT_PADDING_X,
                TEXTBOX_Y + PROMPT_OFFSET_Y
            )
        )


def main(screen=None, clock=None):
    """
    Runs the outro sequence.

    Args:
        screen: Optional shared pygame display Surface.
                bomb.py passes this in so all programs use the same window.
        clock: Optional shared pygame Clock.
               bomb.py passes this in for consistent frame timing.

    Returns:
        True if the outro completes normally.
        False if the player closes the window.
    """
    # Initialize pygame if this file is run directly.
    if not pygame.get_init():
        pygame.init()

    # Initialize audio in case sounds/music are added later.
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # If no screen was passed in, create one.
    # This makes outro.py easy to test by itself.
    created_display = screen is None

    if screen is None:
        screen = create_fullscreen_display("Outro")

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Outro")

    # Load shared background.
    background = pygame.image.load(BACKGROUND_PATH).convert()
    background = pygame.transform.scale(background, screen.get_size())

    

    # Load the wire background/panel image.
    # Its position and size are controlled by the WIRE_BACKGROUND constants above.
    wire_background = pygame.image.load(WIRE_BACKGROUND_PATH).convert()
    wire_background = pygame.transform.smoothscale(
        wire_background,
        (
            WIRE_BACKGROUND_WIDTH,
            WIRE_BACKGROUND_HEIGHT
        )
    )

    rect_surf = pygame.Surface((1200,1200), pygame.SRCALPHA)
    transp = 0
    rect_surf2 = pygame.Surface((1200,1200), pygame.SRCALPHA)
    transp2 = 0

    # Load font used for dialogue.
    font = pygame.font.Font(FONT_PATH, 16)

    # -----------------------------------------------------------------------
    # SEQUENCE STATE
    # -----------------------------------------------------------------------
    # active_message: which message in MESSAGES is currently showing.
    # counter: controls the typing effect.
    # done: True when the current message has finished typing.
    # final_message_done_time: used to auto-exit after the final message.
    # prev_btn: used to detect a fresh RPi button press instead of holding.
    # running: controls the main loop.
    # result: returned to bomb.py.
    active_message = 0
    counter = 0
    done = False
    final_message_done_time = None
    prev_btn = False
    running = True
    result = True
    tcounter = 0
    endscreen = False
    escount = 0

    steps1 = pygame.mixer.Sound("img_keys/Steps1.mp3")
    steps2 = pygame.mixer.Sound("img_keys/Steps2.mp3")
    vro = pygame.mixer.Sound("img_keys/realendmus.mp3")
    endmus = pygame.mixer.Sound("img_keys/Watashino Uso.mp3")
    talking_sound = pygame.mixer.Sound("img_keys/C2Talking.mp3")
    talking_channel = pygame.mixer.Channel(0)
    effects_channel = pygame.mixer.Channel(1)

  

    stepped = False
    stepped2 = False
    vroa = False
    final = False
    screenfu = False
    
    while running:
        now = pygame.time.get_ticks()
        message = MESSAGES[active_message]

        def advance_message():
            """
            Moves to the next message, but only after the current text is done.

            This prevents accidentally skipping text before it finishes typing.
            """
            nonlocal active_message
            nonlocal counter
            nonlocal done
            nonlocal final_message_done_time
            nonlocal running
            nonlocal endscreen

            # Do not advance until the full message is visible.
            if not done:
                return

            # Move to the next message if one exists.
            if active_message < len(MESSAGES) - 1:
                active_message += 1
                counter = 0
                done = False
                final_message_done_time = None
            else:
                # If this was the final message, end the outro.
                endscreen = True

        # -------------------------------------------------------------------
        # INPUT HANDLING
        # -------------------------------------------------------------------
        # PC: Enter advances dialogue.
        # RPi: physical button advances dialogue.
        # Closing the window exits and returns False.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                result = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not RPi:
                    advance_message()

            if endscreen:
                if escount > 300:
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN and not RPi:
                                running = False
                                result = False

        # Raspberry Pi button support.
        if RPi and component_button_state is not None:
            btn = component_button_state.value

            # Only advance on a new press, not while holding the button down.
            if btn and not prev_btn:
                advance_message()
            prev_btn = btn


        if endscreen:
            escount += 1
            if escount > 3 and vroa == False:
                effects_channel.play(vro)
                vroa = True
            if escount <= 85:
                transp += 3
            rect_surf.fill((255, 255, 255, transp))
           
            if escount > 90 and stepped == False:
                effects_channel.play(steps1)
                stepped = True
            if escount > 150 and stepped2 == False:
                effects_channel.play(steps1)
                stepped2 = True
            if escount > 240 and escount <= 325:
                transp2 += 3  
            rect_surf2.fill((255, 255, 255, transp2))
            if escount > 280 and final == False:
                 effects_channel.play(endmus) 
                 final = True  
                 screenfu = True

        # -------------------------------------------------------------------
        # TEXT TYPING LOGIC
        # -------------------------------------------------------------------
        # The message reveals one character at a time.
        if counter < TYPE_SPEED * len(message):
            counter += 1
            if tcounter == 0:
                talking_channel.play(talking_sound)
            tcounter += 1
        else:
            done = True
            tcounter = 0
            talking_channel.stop()

            # The final message automatically ends after a short wait.
            if active_message == len(MESSAGES) - 1:
                if final_message_done_time is None:
                    final_message_done_time = now
                elif now - final_message_done_time >= FINAL_MESSAGE_WAIT_MS:
                    endscreen = True

        typed_text = message[0:counter // TYPE_SPEED]

        # -------------------------------------------------------------------
        # DRAWING
        # -------------------------------------------------------------------
        # Basic draw order:
        # 1. Background
        # 2. Characters
        # 3. Optional future outro objects/effects
        # 4. Textbox

        if screenfu == False:
            screen.blit(background, (0, 0))
            screen.blit(wire_background, (WIRE_BACKGROUND_X, WIRE_BACKGROUND_Y))
            draw_character(screen)
            draw_textbox(screen, font, typed_text, done, active_message)
        screen.blit(rect_surf, (0,0))
        screen.blit(rect_surf2, (0,0))
        pygame.display.flip()
        clock.tick(FPS)

    # Only quit pygame if this file created its own display.
    # If bomb.py passed in the display, bomb.py handles quitting later.
    if created_display:
        pygame.quit()

    return result


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)