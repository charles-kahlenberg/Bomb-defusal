import pygame

from character_overlay import draw_character

try:
    from bomb_configs import RPi, component_button_state
except ImportError:
    RPi = False
    component_button_state = None


GAME_W = 616
GAME_H = 342

KEY_W = 34
KEY_H = 144

TEXTBOX_X = 277
TEXTBOX_Y = 42
TEXTBOX_WIDTH = 471
TEXTBOX_HEIGHT = 132
TEXTBOX_ALPHA = 180
TEXT_PADDING_X = 18
TEXT_PADDING_Y = 16
PROMPT_OFFSET_Y = 90
TEXT_LINE_SPACING = 24

PANEL_X = 300
PANEL_Y = 232
PANEL_W = 425
PANEL_H = 299


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

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    created_display = screen is None
    if screen is None:
        screen = pygame.display.set_mode((1024, 576))

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Switch Intro")

    bg = pygame.image.load("img_keys/base.png").convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    switch_panel_surface = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)

    panel_bg = pygame.image.load("img_keys/SwitchesBg.png").convert()
    panel_bg = pygame.transform.scale(panel_bg, (GAME_W, GAME_H))

    door = pygame.image.load("img_keys/Door.png").convert_alpha()

    switch_image = pygame.image.load("img_keys/SwitchD.png").convert_alpha()
    switch_image = pygame.transform.scale(switch_image, (KEY_W, KEY_H))

    spacing = 30
    start_x = (820 - (4 * KEY_W + 3 * (spacing - KEY_W))) // 2
    switch_positions = [
        (start_x + 0 * spacing, 110),
        (start_x + 2 * spacing, 110),
        (start_x + 4 * spacing, 110),
        (start_x + 6 * spacing, 110),
    ]

    messages = [
        "The safe clicks open, and inside is a silver key.",
        "Charles takes the key and looks around the room.",
        "Charles notices the door which exits the room and heads over.",
        "Charles unlocks the door and heads down the hallway.",
        "He is faced with a large steel door, \nadjacent are an array of switches.",
        "Charles recognizes these as binary switches. \nHe needs to match the target number using the switches.",
        "It won't be as simple as normal binary though..."
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

        screen.blit(bg, (0, 0))
        draw_character(screen)

        switch_panel_surface.blit(panel_bg, (0, 0))
        switch_panel_surface.blit(door, (29, 16))

        for switch_pos in switch_positions:
            switch_panel_surface.blit(switch_image, switch_pos)

        panel = pygame.transform.smoothscale(switch_panel_surface, (PANEL_W, PANEL_H))
        screen.blit(panel, (PANEL_X, PANEL_Y))

        if counter < speed * len(message):
            counter += 1

            if tcounter == 0:
                c2t.play()

            tcounter += 1

            if tcounter > 20:
                tcounter = 0
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
            screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + PROMPT_OFFSET_Y))

        pygame.display.flip()
        clock.tick(24)

    if created_display:
        pygame.quit()

    return True


if __name__ == "__main__":
    raise SystemExit(main())