"""
ventintro.py

Story sequence before the vent/keypad minigame.

Responsibilities:
- Shows the player the vent panel.
- Displays instructions for entering the vent sequence.
- Uses a typewriter-style dialogue effect.
- Supports Enter input on PC and button input on RPi.

Returns:
- True when the intro completes normally.
- False when the player closes the window.

Notes:
- This file is intended to be called by bomb.py as part of the full game sequence.
- It can also be run directly for testing.
"""


import pygame

from character_overlay import draw_character
from display_utils import create_fullscreen_display

try:
    from bomb_configs import RPi, component_button_state
except ImportError:
    RPi = False
    component_button_state = None


TEXTBOX_X = 277
TEXTBOX_Y = 42
TEXTBOX_WIDTH = 471
TEXTBOX_HEIGHT = 132
TEXTBOX_ALPHA = 180
TEXT_PADDING_X = 18
TEXT_PADDING_Y = 16
PROMPT_OFFSET_Y = 45

PANEL_X = 300
PANEL_Y = 232
PANEL_W = 425
PANEL_H = 299


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None
    if screen is None:
        screen = create_fullscreen_display("Wires Intro")

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Wires Intro")

    bg = pygame.image.load("img_keys/base.png").convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    panel = pygame.image.load("img_keys/vent.png").convert_alpha()
    panel = pygame.transform.smoothscale(panel, (PANEL_W, PANEL_H))

    messages = [
        "Charles looks around and notices a panel on his restraints.",
        "(input the numbers from the vent on the keypad)",
        "(make sure to go in a clockwise order)"
    ]

    active_message = 0
    message = messages[active_message]

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)
    counter = 0
    speed = 1
    done = False
    final_message_done_time = None
    c2t = pygame.mixer.Sound("img_keys/C2Talking.mp3")
    prev_btn = False
    tcounter = 0

    running = True

    while running:
        now = pygame.time.get_ticks()

        def advance_message():
            nonlocal active_message, message, counter, done, final_message_done_time, running

            if done:
                if active_message < len(messages) - 1:
                    active_message += 1
                    message = messages[active_message]
                    counter = 0
                    done = False
                    final_message_done_time = None
                else:
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not RPi:
                    advance_message()

        if RPi and component_button_state is not None:
            btn = component_button_state.value

            if btn and not prev_btn:
                advance_message()

            prev_btn = btn

        screen.blit(bg, (0, 0))
        draw_character(screen)
        screen.blit(panel, (PANEL_X, PANEL_Y))

        if counter < speed * len(message):
            counter += 1
            if tcounter == 0:
                c2t.play()
            tcounter +=1
            if tcounter > 20:
                tcounter == 0
        else:
            done = True
            tcounter = 0
            pygame.mixer.stop()

            if active_message == len(messages) - 1:
                if final_message_done_time is None:
                    final_message_done_time = now
                elif now - final_message_done_time >= 3000:
                    running = False

        text_box = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
        text_box.fill((0, 0, 0, TEXTBOX_ALPHA))
        screen.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

        border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

        snip = font.render(message[0:counter // speed], True, "white")
        screen.blit(snip, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + TEXT_PADDING_Y))

        if done and active_message < len(messages) - 1:
            prompt_text = "Press Button" if RPi else "Press Enter"
            prompt = font.render(prompt_text, True, (180, 180, 180))
            screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + PROMPT_OFFSET_Y))

        pygame.display.flip()
        clock.tick(24)

    if created_display:
        pygame.quit()

    return True


if __name__ == "__main__":
    raise SystemExit(main())