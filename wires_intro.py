import pygame

from character_overlay import draw_character

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


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None
    if screen is None:
        screen = pygame.display.set_mode((1024, 576))

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
        "Pay attention, move carefully, and do not guess.",
    ]

    active_message = 0
    message = messages[active_message]

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)
    counter = 0
    speed = 1
    done = False
    final_message_done_time = None
    prev_btn = False

    def show_frame():
        main_screen.blit(bg, (0, 0))
        draw_character(main_screen)

        text_box = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
        text_box.fill((0, 0, 0, TEXTBOX_ALPHA))
        main_screen.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

        border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        pygame.draw.rect(main_screen, (255, 255, 255), border_rect, 2)

        typed_text = message[0:counter // speed]
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

        screen.blit(wire_bg, (0, 0))

        if counter < speed * len(message):
            counter += 1
        else:
            done = True

            if active_message == len(messages) - 1:
                if final_message_done_time is None:
                    final_message_done_time = now
                elif now - final_message_done_time >= 3000:
                    running = False

        show_frame()
        clock.tick(24)

    if created_display:
        pygame.quit()

    return True


if __name__ == "__main__":
    raise SystemExit(main())