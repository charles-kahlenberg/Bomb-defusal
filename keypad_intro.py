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
LONG_MESSAGE_PROMPT_OFFSET_Y = 90
TEXT_LINE_SPACING = 24

WIRE_BG_X = 300
WIRE_BG_Y = 232
WIRE_BG_WIDTH = 425
WIRE_BG_HEIGHT = 299

KEYPAD_X = 409
KEYPAD_Y = 249
KEYPAD_W = 200
KEYPAD_H = 268

KEYPAD_SOURCE_W = 200
KEYPAD_SOURCE_H = 300

KEYPAD_GRID_COLS = 3
KEYPAD_GRID_ROWS = 4
KEYPAD_BUTTON_W = 50
KEYPAD_BUTTON_H = 50
KEYPAD_BUTTON_GAP_X = 3
KEYPAD_BUTTON_GAP_Y = 2
KEYPAD_BUTTON_OFFSET_Y = 71


def make_keypad_surface():
    keypad_surface = pygame.Surface((KEYPAD_SOURCE_W, KEYPAD_SOURCE_H), pygame.SRCALPHA)

    keypad_bg = pygame.image.load("img_keys/KeypadFull.png").convert_alpha()
    keypad_bg.set_colorkey((0, 0, 0))
    keypad_bg = pygame.transform.scale(keypad_bg, (KEYPAD_SOURCE_W, KEYPAD_SOURCE_H))
    keypad_surface.blit(keypad_bg, (0, 0))

    white_img = pygame.image.load("img_keys/white_key.png").convert_alpha()
    black_img = pygame.image.load("img_keys/black_key.png").convert_alpha()

    white_img.set_alpha(0)
    black_img.set_alpha(0)

    white_button = pygame.transform.scale(white_img, (KEYPAD_BUTTON_W, KEYPAD_BUTTON_H))
    black_button = pygame.transform.scale(black_img, (KEYPAD_BUTTON_W, KEYPAD_BUTTON_H))

    grid_total_w = KEYPAD_GRID_COLS * KEYPAD_BUTTON_W + (KEYPAD_GRID_COLS - 1) * KEYPAD_BUTTON_GAP_X
    grid_origin_x = (KEYPAD_SOURCE_W - grid_total_w) // 2
    grid_origin_y = KEYPAD_BUTTON_OFFSET_Y

    for row in range(KEYPAD_GRID_ROWS):
        for col in range(KEYPAD_GRID_COLS):
            button_image = white_button if (row + col) % 2 == 0 else black_button
            button_x = grid_origin_x + col * (KEYPAD_BUTTON_W + KEYPAD_BUTTON_GAP_X)
            button_y = grid_origin_y + row * (KEYPAD_BUTTON_H + KEYPAD_BUTTON_GAP_Y)
            keypad_surface.blit(button_image, (button_x, button_y))

    return keypad_surface


def draw_wrapped_text(surface, font, text, color, x, y, max_width):
    lines = []

    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current_line = ""

        for word in words:
            test_line = word if current_line == "" else current_line + " " + word

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

    for index, line in enumerate(lines):
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y + index * TEXT_LINE_SPACING))


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None
    if screen is None:
        screen = create_fullscreen_display("Keypad Intro")

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Keypad Intro")

    bg = pygame.image.load("img_keys/base.png").convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    wire_bg = pygame.image.load("img_keys/WireBG.png").convert()
    wire_bg = pygame.transform.smoothscale(
        wire_bg,
        (WIRE_BG_WIDTH, WIRE_BG_HEIGHT)
    )

    keypad_surface = make_keypad_surface()

    messages = [
        "Charles is freed from the chair... ",
        "He notices a safe in the corner of the room.",
        "On the safe is a keypad. But it's a strange model.",
        "In order to get the pin code,\nyou must repeat the patterns displayed.",
        "Repeat the pattern correctly to continue.",
        "But be sure to remember the first number from the pattern.\n",
        "Make too many mistakes and the bomb wins.",
    ]

    active_message = 0
    message = messages[active_message]

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)
    counter = 0
    speed = 1
    done = False
    final_message_done_time = None
    prev_btn = False
    tcounter = 0
    c2t = pygame.mixer.Sound("img_keys/C2Talking.mp3")
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
                if created_display:
                    pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not RPi:
                    advance_message()

        if RPi and component_button_state is not None:
            btn = component_button_state.value

            if btn and not prev_btn:
                advance_message()

            prev_btn = btn

        # Draw background, character, wire panel
        screen.blit(bg, (0, 0))
        draw_character(screen)
        screen.blit(wire_bg, (WIRE_BG_X, WIRE_BG_Y))

        # Draw keypad (scaled)
        scaled_keypad = pygame.transform.smoothscale(keypad_surface, (KEYPAD_W, KEYPAD_H))
        screen.blit(scaled_keypad, (KEYPAD_X, KEYPAD_Y))

        if counter < speed * len(message):
            counter += 1
            if tcounter == 0:
                c2t.play()
            tcounter += 1
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

        typed_text = message[0:counter // speed]
        draw_wrapped_text(
            screen,
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

            prompt_offset_y = LONG_MESSAGE_PROMPT_OFFSET_Y if active_message == 3 else PROMPT_OFFSET_Y
            screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + prompt_offset_y))

        pygame.display.flip()
        clock.tick(24)

    if created_display:
        pygame.quit()

    return True


if __name__ == "__main__":
    raise SystemExit(main())