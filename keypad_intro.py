import pygame


TEXTBOX_X = 205
TEXTBOX_Y = 25
TEXTBOX_WIDTH = 610
TEXTBOX_HEIGHT = 70
TEXTBOX_ALPHA = 180
TEXT_PADDING_X = 18
TEXT_PADDING_Y = 16
PROMPT_OFFSET_Y = 45


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None
    if screen is None:
        screen = pygame.display.set_mode((1024, 576))

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Keypad Intro")

    bg = pygame.image.load("base.png").convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    messages = [
        "Charles is freed from the chair... ",
        "He notices a safe in the corner of the room.",
        "On the safe is a keypad. But it's a strange model.",
        "In order to get the pin code, you must repeat the patterns displayed.",
        "Repeat the pattern correctly to continue.",
        "But be sure to remember the first number from the pattern",
        "Make too many mistakes and the bomb wins.",
    ]

    active_message = 0
    message = messages[active_message]

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)
    counter = 0
    speed = 1
    done = False
    final_message_done_time = None

    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done:
                    if active_message < len(messages) - 1:
                        active_message += 1
                        message = messages[active_message]
                        counter = 0
                        done = False
                        final_message_done_time = None
                    else:
                        running = False

        screen.blit(bg, (0, 0))

        if counter < speed * len(message):
            counter += 1
        else:
            done = True

            if active_message == len(messages) - 1:
                if final_message_done_time is None:
                    final_message_done_time = now
                elif now - final_message_done_time >= 3000:
                    running = False

        text_box = pygame.Surface((610, 70), pygame.SRCALPHA)
        text_box.fill((0, 0, 0, 180))
        screen.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

        border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

        snip = font.render(message[0:counter // speed], True, "white")
        screen.blit(snip, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + TEXT_PADDING_Y))

        if done and active_message < len(messages) - 1:
            prompt = font.render("Press Enter", True, (180, 180, 180))
            screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + PROMPT_OFFSET_Y))

        pygame.display.flip()
        clock.tick(24)

    if created_display:
        pygame.quit()

    return True


if __name__ == "__main__":
    raise SystemExit(main())