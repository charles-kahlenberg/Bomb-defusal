import pygame
from character_overlay import draw_character


GAME_W = 1024
GAME_H = 576

MINIGAME_WINDOW_X = -195
MINIGAME_WINDOW_Y = -40
MINIGAME_WINDOW_W = 1300
MINIGAME_WINDOW_H = 702


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None
    if screen is None:
        screen = pygame.display.set_mode((1024, 576))

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Vent Minigame")

    main_screen = screen
    game_surface = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
    screen = game_surface

    intro_bg = pygame.image.load("img_keys/base.png").convert()
    intro_bg = pygame.transform.scale(intro_bg, main_screen.get_size())

    minigame_rect = pygame.Rect(
        MINIGAME_WINDOW_X,
        MINIGAME_WINDOW_Y,
        MINIGAME_WINDOW_W,
        MINIGAME_WINDOW_H
    )

    def show_frame():
        main_screen.blit(intro_bg, (0, 0))
        draw_character(main_screen)

        scaled_game = pygame.transform.smoothscale(game_surface, minigame_rect.size)
        main_screen.blit(scaled_game, minigame_rect)

        pygame.display.flip()

    vent = pygame.image.load("img_keys/vent.png").convert_alpha()

    angle = 0
    pressed = []

    rx = 390
    ry = 220
    count = 0

    fling = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if created_display:
                    pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4:
                    pressed.append(4)
                elif event.key == pygame.K_3:
                    pressed.append(3)
                elif event.key == pygame.K_2:
                    pressed.append(2)
                elif event.key == pygame.K_1:
                    pressed.append(1)

        screen.fill((0, 0, 0, 0))

        if pressed == [4, 1, 2, 3]:
            fling = True
        elif len(pressed) > 3:
            pressed = []

        if fling:
            count += 1
            angle += 20
            rx -= 40
            ry -= 40

            if count >= 35:
                return True

        fvent = pygame.transform.rotate(vent, angle)
        screen.blit(fvent, (rx, ry))

        show_frame()
        clock.tick(60)

    if created_display:
        pygame.quit()

    return False


if __name__ == "__main__":
    raise SystemExit(main())
