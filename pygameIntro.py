import pygame


def main():
    pygame.mixer.init()
    pygame.init()

    screen = pygame.display.set_mode((800, 480))
    pygame.display.set_caption("Rectangle Test")

    bg = pygame.image.load("base.png").convert()

    rect_pos = pygame.Rect(0, 0, 800, 480)
    rect_surf = pygame.Surface((800, 480), pygame.SRCALPHA)
    rect_surf.fill((0, 0, 0, 160))

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
    started = False
    notplayed = True

    rect_color = (0, 0, 0)
    count = 0
    speed = 1
    doorup = False

    clock = pygame.time.Clock()
    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        if count < 250:
            rect_pos.move_ip(0, -2)
            count += 1
            started = True

        if started and notplayed:
            notplayed = False
            pygame.mixer.music.play()

        if count == 249:
            doorup = True

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

        snip = font.render(message[0:counter // speed], True, "white")
        screen.blit(snip, (223, 41))

        pygame.display.flip()
        clock.tick(24)

    pygame.quit()
    return True


if __name__ == "__main__":
    raise SystemExit(main())