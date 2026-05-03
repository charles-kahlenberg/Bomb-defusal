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

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    created_display = screen is None
    if screen is None:
        screen = pygame.display.set_mode((1024, 576))

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Defuse the Bomb")

    bg = pygame.image.load("base.png").convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    screen_width, screen_height = screen.get_size()

    rect_pos = pygame.Rect(0, 0, screen_width, screen_height)
    rect_surf = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    rect_surf.fill((0, 0, 0, 0))

    messages = [
        "You have put our name to question for too long.....",
        "For this you shall die!",
        "There's a bomb strapped to your chair!",
        "MWAJAHAHAHAHAHAHA!",
        "Good luck getting out of this!",
    ]

    activem = 0
    message = messages[activem]

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)
    counter = 0
    done = False
    final_message_done_time = None

    pygame.mixer.music.load("intro.mp3")
    pygame.mixer.music.set_volume(10.00)
    started = False
    notplayed = True

    rect_color = (0, 0, 0)
    count = 0
    speed = 1
    doorup = False

    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done and activem < len(messages) - 1:
                    activem += 1
                    done = False
                    final_message_done_time = None
                    message = messages[activem]
                    counter = 0

        screen.fill((255, 255, 255))

        screen.blit(bg, (0, 0))
        screen.blit(rect_surf, (0, 0))
        pygame.draw.rect(screen, rect_color, rect_pos)

        if rect_pos.bottom > 0:
            rect_pos.move_ip(0, -2)
            started = True
        else:
            doorup = True

        if started and notplayed:
            notplayed = False
            pygame.mixer.music.play()

        if doorup:
            if counter < speed * len(message):
                counter += 1
            else:
                done = True

                if activem == len(messages) - 1:
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

            if done and activem < len(messages) - 1:
                prompt = font.render("Press Enter", True, (180, 180, 180))
                screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + PROMPT_OFFSET_Y))

        pygame.display.flip()
        clock.tick(24)

    if created_display:
        pygame.quit()

    return True


if __name__ == "__main__":
    raise SystemExit(main())